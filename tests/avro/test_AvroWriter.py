import fastavro
import unittest
import io

from SwissKnife.avro import AvroWriter
from SwissKnife.avro.AvroWriter import AvroMatchingException


# How to test this?
class test_AvroWriter(unittest.TestCase):
    

    example_schema = {
        "type" : "record",
        "name" : "Employee",
        "fields" : [
            { "name" : "Name" , "type" : "string" },
            { "name" : "Age" , "type" : "int" }
        ]
    }

    example_records = [
        {"Name": "John Doe", "Age": 22},
        {"Name": "Jane Doe", "Age": 27}
    ]

    def test_write_records(self):

        # Arrange
        dummy_file = io.BytesIO()

        avro_writer = AvroWriter(dummy_file, self.example_schema)

        # Act
        for record in self.example_records:

            avro_writer.write(record)

        avro_writer.close()

        dummy_file.seek(0)
        
        # Assert

        readed_records = [record for record in fastavro.reader(dummy_file)]

        sorted_expected = sorted(self.example_records, key=lambda x: x["Name"])
        sorted_result = sorted(readed_records, key=lambda x: x["Name"])

        for expected_record, result_record in zip(sorted_expected, sorted_result):

            self.assertDictEqual(expected_record, result_record)

    def test_catch_exception_on_invalid_record(self):

        # Arrange
        dummy_file = io.BytesIO()

        avro_writer = AvroWriter(dummy_file, self.example_schema)

        # Act and assert
        with self.assertRaises(AvroMatchingException) as context:
            avro_writer.write({"Age": 21})
