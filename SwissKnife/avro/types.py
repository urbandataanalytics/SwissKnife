from typing import Dict

# The type of each record file.
Record = Dict[str, object]

class NoDefault(object):
    """
    Class to model a not specified default value. In this case, a value is consider as required.
    """
    pass

class Variables:
    """
    Static values of certain fields in Avro Schema to reference in other parts of the code
    """
    FIELDS = "fields"
    NAME = "name"
    ALIASES = "aliases"
    TRANSFORM = "transform"
    TYPE = "type"
    DEFAULT = "default"
