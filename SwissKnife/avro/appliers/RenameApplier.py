
from SwissKnife.avro.types import Record, Variables, NoDefault

class RenameApplier(object):

    def __init__(self, schema: dict):

        self.rename_dict = self.create_rename_dict(schema)

    @staticmethod
    def create_rename_dict(schema: dict) -> dict:
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

    def apply(self, record: Record) -> Record:
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
