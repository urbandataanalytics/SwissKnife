import re
from typing import Callable
from SwissKnife.avro.types import Record, Variables


class NoDefault(object):
    """
    Class to model a not specified default value. In this case, a value is consider as required.
    """
    pass


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
        self.rename_dict = AvroTransformer._create_rename_dict(avro_schema)
        self.defaults_dict = AvroTransformer._create_defaults_dict(avro_schema)
        self.transform_dict = AvroTransformer._create_transform_dict(avro_schema)
        self.cast_dict = AvroTransformer._create_cast_dict(avro_schema)

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
        renamed_record = self.get_renamed_record_and_remove_invalid_fields(record)
        transformed_record = self.get_transformed_record(renamed_record)
        record_with_defaults = self.get_record_with_defaults(transformed_record)
        return self.get_record_with_casted_values(record_with_defaults)

    def get_renamed_record_and_remove_invalid_fields(self, record: Record) -> Record:
        """
        Transforms a record to another one with correct names: If a record field
        uses an alias, it will be changed to the correct name using the avro schema as reference.
        Also, a field that is not in the avro schema will be removed.
        :param record: The input record.
        :type record: Record
        :return: A record with the correct field names and without invalid fields.
        :rtype: Record
        """
        new_record = {}
        for key, value in record.items():
            # Remove not existing keys
            if key not in self.rename_dict:
                continue
            new_key = self.rename_dict[key]
            new_record[new_key] = value
        return new_record

    def get_record_with_defaults(self, record: Record) -> Record:
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

    def get_transformed_record(self, record: Record) -> Record:
        """
        Applies the transformations in a record using the avro schema as a reference.
        :param record: The input record.
        :type record: Record
        :return: A new record with transformations applied.
        :rtype: Record
        """
        new_record = {}
        for key, value in record.items():
            if key in self.transform_dict:
                transform_function = self.transform_dict[key]
                new_record[key] = transform_function(value, record)
            else:
                new_record[key] = value
        return new_record

    @staticmethod
    def _create_rename_dict(schema: dict) -> dict:
        """
        Creates a dict that maps a name with the correct one.
        :param schema: The provided schema.
        :type schema: dict
        :return: A dict with the map "name -> correct_name". It maps
        either a "name -> name" or an "alias -> name" pair.
        :rtype: dict
        """
        rename_dict = {}
        for field in schema[Variables.FIELDS]:
            field_name = field[Variables.NAME]
            # Rename field_name to itself
            rename_dict[field_name] = field_name
            # rename aliases
            if Variables.ALIASES in field:
                for alias in field[Variables.ALIASES]:
                    rename_dict[alias] = field_name
        return rename_dict

    @staticmethod
    def _create_transform_dict(schema: dict) -> dict:
        """
        Creates a dict that maps a field with a transform function.
        :param schema: The provided schema.
        :type schema: dict
        :return: A dict that maps a field with a transform function.
        It can be an empty dict if there are not fields with transform functions to apply.
        :rtype: dict
        """
        transform_dict = {}
        for field in schema[Variables.FIELDS]:
            if Variables.TRANSFORM in field:
                field_name = field[Variables.NAME]
                transform_name = field[Variables.TRANSFORM]
                transform_dict[field_name] = AvroTransformer._get_transform_function(transform_name)
        return transform_dict

    @staticmethod
    def _create_cast_dict(schema: dict) -> dict:
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
    def _create_defaults_dict(schema: dict) -> dict:
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

    @staticmethod
    def _get_transform_function(transform_name: str) -> Callable[[object, dict], object]:
        """
        Gets a transform function from a transform_name. The purpose of this function
        is to transform the current value of a field to another one (for example, an available
        value for the field type).
        transform_name could be a function name or an expression, so the result will always be a closure.
        For example, "copyFrom(date)" refers to function "copyFrom" with the parameter "date".
        The returned function has two parameters:
            - value: The current value of the field.
            - record: The entire record.

        Available functions:
            - int2boolean: Transform an int to a boolean. True if x > 0, otherwise False.
            - copyFrom(y): Return the value of field Y. The current value of the
                           target field is ignored.

        :param transform_name: The transform name.
        :type transform_name: str
        :raises RuntimeError: Raises a exception if transform_name is invalid.
        :raises RuntimeError: copyFrom function raises exception if the provided field is invalid when it is executed.
        :return: A transform function.
        :rtype: Callable[[object, dict], object]
        """
        selected_function = None
        if transform_name == "int2boolean":
            def int2boolean(value: int, record: dict) -> bool:
                if value is None:
                    return None
                else:
                    return int(value) > 0
            selected_function = int2boolean
        elif re.match("copyFrom\(\w+\)", transform_name):
            copied_field = re.match("copyFrom\((\w+)\)", transform_name)[1]

            def copyFrom(value: int, record: dict) -> bool:
                if copied_field in record:
                    return record[copied_field]
                else:
                    raise RuntimeError("Invalid field in copyFrom")

            selected_function = copyFrom
        # If there is not an available function, raise Exception
        if selected_function is None:
            raise RuntimeError(f"Invalid or unsupported name for a transform function: '{transform_name}'")
        return selected_function

    def get_record_with_casted_values(self, record: Record) -> Record:
        """
        Gets a new record with its values casted to the appropriate types
        :param record: a record with transformation and default values applied
        :return: a new record with casted values
        """
        new_record = {}
        for key, value in record.items():
            try:
                types_list = self.cast_dict[key]
                casted_value = self._get_casted_value(value, types_list)
            except Exception as ex:
                raise ValueError(f"Error {ex} casting the field '{key}' with value '{value}' in the record {record}."
                                 f"Available cast values: {types_list}")
            new_record[key] = casted_value
        return new_record

    @staticmethod
    def _get_casted_value(value: object, types_to_cast_list: list) -> object:
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

