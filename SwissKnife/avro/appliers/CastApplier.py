
from SwissKnife.avro.types import Record, Variables, NoDefault


class CastApplier(object):

    def __init__(self, schema: dict):

        self.cast_dict = self.create_cast_dict(schema)

    def apply(self, record: Record) -> Record:
        """
        Gets a new record with its values casted to the appropriate types
        :param record: a record with transformation and default values applied
        :return: a new record with casted values
        """
        new_record = {}
        for key, value in record.items():
            try:
                types_list = self.cast_dict[key]
                casted_value = CastApplier.get_casted_value(value, types_list)
            except Exception as ex:
                raise ValueError(f"Error {ex} casting the field '{key}' with value '{value}' in the record {record}."
                                 f"Available cast values: {types_list}")
            new_record[key] = casted_value
        return new_record

    @staticmethod
    def create_cast_dict(schema: dict) -> dict:
        """
        Creates a dict that maps a field with its proper type to cast it, according to the provided avro schema.
        :param schema: The provided avro schema
        :return: A dict that maps field with its type
        :rtype: dict
        """
        cast_dict = {}
        for field in schema[Variables.FIELDS]:
            field_name = field[Variables.NAME]
            types_list = field[Variables.TYPE]
            cast_dict[field_name] = types_list
        return cast_dict

    @staticmethod
    def get_casted_value(value: object, types_to_cast_list: list) -> object:
        """
        Helper function to cast a value according to the casting dictionary for that value
        :param value: field value
        :param types_to_cast_list: list with cast values
        :return: a casted value
        """
        for type_to_cast in types_to_cast_list:
            if type_to_cast == "null" and value is None:
                return None
            elif type_to_cast in ["int", "long"]:
                # if empty string
                if type(value) is str and len(value) == 0:
                    return None
                else:
                    return int(value)
            elif type_to_cast == "boolean":
                return bool(value)
            elif type_to_cast in ["double", "float"]:
                if type(value) is str:
                    # if empty string
                    if len(value) == 0:
                        return None
                    # Str value can contains "comma" instead of "dot"
                    else:
                        return float(value.replace(",", "."))
                else:
                    return float(value)
            elif type_to_cast in ["string"]:
                return str(value)
        # If the iteration over types list ends, the value is not valid. So, it raises an exception.
        raise ValueError(f"The value {value} can not be cast to any type of {types_to_cast_list}")

