import sys

try:
    import fastavro
except ModuleNotFoundError:
    print("ERROR: You need install SwissKnife with 'avro' tag.")
    sys.exit(-1)

from .AvroWriter import AvroWriter
 