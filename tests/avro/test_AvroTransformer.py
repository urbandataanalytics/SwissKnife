import unittest

from SwissKnife.avro.AvroTransformer import AvroTransformer, NoDefault
from SwissKnife.avro.appliers import CastApplier
from SwissKnife.avro.appliers import DefaultsApplier
from SwissKnife.avro.appliers import RenameApplier
from SwissKnife.avro.appliers import TransformApplier


class AvroTransformerTest(unittest.TestCase):

    example_avro_schema = {
        "type": "record",
        "name": "example_record",
        "fields": [
            {
                "name": "url",
                "type": ["string"]
            },
            {
                "name": "code",
                "aliases": ["id"],
                "type": ["null", "string"],
                "default": None
            },
            {
                "name": "date",
                "aliases": ["lastupdate", "reg_date"],
                "type": ["null", "string"]
            },
            {
                "name": "startDate",
                "type": ["null", "string"],
                "transform": "copyFrom(date)",
                "default": None
            },
            {
                "name": "isReady",
                "type": ["boolean"],
                "transform": "int2boolean",
                "default": False
            }
        ]
    }

    def test__create_rename_dict(self):
        rename_dict = RenameApplier(self.example_avro_schema).rename_dict
        self.assertDictEqual(rename_dict, {
            "url": "url",
            "code": "code",
            "id": "code",
            "date": "date",
            "lastupdate": "date",
            "reg_date": "date",
            "startDate": "startDate",
            "isReady": "isReady"
        })

    def test__create_transform_dict(self):
        # It is complicated to test the values (functions) of the dict
        transform_dict = TransformApplier(self.example_avro_schema).transform_dict
        self.assertListEqual(list(transform_dict.keys()), ["startDate", "isReady"])

    def test__create_defaults_dict(self):
        defaults_dict = DefaultsApplier(self.example_avro_schema).defaults_dict
        self.assertDictEqual(defaults_dict, {
            "url": NoDefault,
            "code": None,
            "date": NoDefault,
            "startDate": None,
            "isReady": False
        })

    def test_transform_function_int2boolean(self):
        int2boolean = TransformApplier(self.example_avro_schema).get_transform_function("int2boolean")
        self.assertEqual(int2boolean(0, {}), False)
        self.assertEqual(int2boolean(-1, {}), False)
        self.assertEqual(int2boolean(-30, {}), False)
        self.assertEqual(int2boolean(1, {}), True)
        self.assertEqual(int2boolean(2, {}), True)
        self.assertEqual(int2boolean(30, {}), True)

    def test_transform_function_copyFrom(self):
        example_record_1 = {"word": "hola", "date": "yesterday", "num": 5}
        example_record_2 = {"word": "hola", "num": 5}
        copy_from_date = TransformApplier(self.example_avro_schema).get_transform_function("copyFrom(date)")
        self.assertEqual(copy_from_date("aux", example_record_1), "yesterday")
        with self.assertRaises(RuntimeError) as context:
            copy_from_date("aux", example_record_2)

    def test_get_transformed_record(self):
        example_record = {
            "url": "http://google.com",
            "code": "123456",
            "date": "123456789",
            "startDate": None,
            "isReady": 1
        }
        transform_applier = TransformApplier(self.example_avro_schema)
        self.assertDictEqual(
            transform_applier.apply(example_record),
            {
                "url": "http://google.com",
                "code": "123456",
                "date": "123456789",
                "startDate": "123456789",
                "isReady": True
            }
        )

    def test_get_renamed_record_and_remove_invalid_fields(self):
        example_record = {
            "url": "http://google.com",
            "id": "123456",
            "invalidField": ":-)",
            "lastupdate": "123456789",
            "isReady": 1
        }
        rename_applier = RenameApplier(self.example_avro_schema)
        self.assertDictEqual(
            rename_applier.apply(example_record),
            {
                "url": "http://google.com",
                "code": "123456",
                "date": "123456789",
                "isReady": 1
            }
        )

    def test_get_record_with_defaults(self):
        example_record_1 = {
            "url": "http://google.com",
            "date": "123456789"
        }

        example_record_default = {
            "url": "http://google.com",
            "code": None,
            "isReady": False,
            "startDate": None
        }

        defaults_applier = DefaultsApplier(self.example_avro_schema)
        self.assertDictEqual(
            defaults_applier.apply(example_record_1),
            {
                "url": "http://google.com",
                "code": None,
                "date": "123456789",
                "isReady": False,
                "startDate": None
            }
        )
        with self.assertRaises(RuntimeError):
            defaults_applier.apply(example_record_default)

    def test_apply_all_transforms(self):
        example_record = {
            "url": "http://udarealestate.com",
            "previous_url": "http://urbandataanalytics.com",
            "id": "IdRealState",
            "date": "1234567",
            "startDate": None
        }
        avro_transformer = AvroTransformer(self.example_avro_schema)
        self.assertDictEqual(avro_transformer.apply_all_transforms(example_record),
                             {
                                 "url": "http://udarealestate.com",
                                 "code": "IdRealState",
                                 "date": "1234567",
                                 "startDate": "1234567",
                                 "isReady": False
                             }
                             )
