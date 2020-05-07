from typing import Dict

# The type of each record file.
Record = Dict[str, object]


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
