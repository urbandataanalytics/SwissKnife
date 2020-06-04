import re
from SwissKnife.avro.types import Record, Variables, NoDefault
from SwissKnife.avro.appliers import DefaultsApplier
from SwissKnife.avro.appliers import RenameApplier
from SwissKnife.avro.appliers import TransformApplier
from SwissKnife.avro.appliers import CastApplier



class AvroTransformer(object):
    """
    Avrotransformer provides some useful methods to
    transform a data list (List[dict]) into another one
    using an avro schema as a reference to do transformations.

    This avro schema will have some custom fields:
        - transform: Indicates a transform function that will be applied
          to input value to get the correct one. This transform can be a
          type conversion, scaling, a threshold, etc.
        - comment: Some info of the field.
    """

    def __init__(self, avro_schema: dict):
        """
        AvroTransformer constructor. It use an avro schema
        as a reference to rename and transform records.
        :param avro_schema: The provided schema.
        :type avro_schema: dict
        """
        self.original_schema = avro_schema
        self.rename_applier = RenameApplier(avro_schema)
        self.defaults_applier = DefaultsApplier(avro_schema)
        self.transform_applier = TransformApplier(avro_schema)
        self.cast_applier = CastApplier(avro_schema)

    def get_original_schema(self) -> dict:
        """Returns the original provided schema.
        :return: An avro schema.
        :rtype: dict
        """
        return self.original_schema

    def apply_all_transforms(self, record: Record) -> Record:
        """
        This function applies all the object transformations to an input record.
           Steps will be:
            - get_renamed_record_an_remove_invalid_fields
            - get_transformed_record
            - get_record_with_defaults
        :param record: The input record.
        :type record: Record
        :return: A record with all transformations applied.
        :rtype: Record
        """
        renamed_record = self.rename_applier.apply(record)
        transformed_record = self.transform_applier.apply(renamed_record)
        record_with_defaults = self.defaults_applier.apply(transformed_record)
        return self.cast_applier.apply(record_with_defaults)

    