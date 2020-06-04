from SwissKnife.avro.types import Record, Variables, NoDefault


class DefaultsApplier(object):

    def __init__(self, schema: dict):

        self.defaults_dict = self.create_defaults_dict(schema)

    @staticmethod
    def create_defaults_dict(schema: dict) -> dict:
        """
        Creates a dict that maps a field with its default value.
        :param schema: The provided avro schema
        :type schema: dict
        :return: A dict that maps field with its default value.
        :rtype: dict
        """
        defaults_dict = {}
        for field in schema[Variables.FIELDS]:
            field_name = field[Variables.NAME]
            if Variables.DEFAULT in field:
                defaults_value = field[Variables.DEFAULT]
                defaults_dict[field_name] = defaults_value
            else:
                defaults_dict[field_name] = NoDefault
        return defaults_dict

    def apply(self, record: Record) -> Record:
        """
        Creates a new record from an existing one. Empty fields are filled with its default value,
        defined in the loaded schema. If an empty field does not have a default value, the function will rise
        an exception.
        :param record: The input record.
        :type record: Record
        :raises RuntimeError: When an empty field has not default value.
        :return: A new record with default values applied.
        :rtype: Record
        """
        new_record = {}
        for key, defaults_value in self.defaults_dict.items():
            if key not in record and defaults_value is NoDefault:
                raise RuntimeError(f"Required {key} not in record {record}")
            elif key not in record and defaults_value is not NoDefault:
                new_record[key] = defaults_value
            else:
                new_record[key] = record[key]
        return new_record
