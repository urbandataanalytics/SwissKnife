import re
from typing import Callable

from SwissKnife.avro.types import Record, Variables, NoDefault

class TransformApplier(object):

    def __init__(self, schema: dict):

        self.transform_dict = self.create_transform_dict(schema)

    def apply(self, record: Record) -> Record:
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
    def create_transform_dict(schema: dict) -> dict:
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
                transform_dict[field_name] = TransformApplier.get_transform_function(transform_name)
        return transform_dict

    @staticmethod
    def get_transform_function(transform_name: str) -> Callable[[object, dict], object]:
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