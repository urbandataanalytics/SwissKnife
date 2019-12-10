from typing import BinaryIO

import fastavro


class AvroMatchingException(Exception):
    """
        Exception when a row is writed to an avro file and it doesn't match with the schema.
    """
    pass


class AvroWriter(object):
    """This object create a writer that writes avro data into a file-like object.
    """

    def __init__(self, output_stream: BinaryIO, avro_schema: dict):
        """AvroWriter constructor
        
        :param output_stream: The file-like object where data will be writed.
        :type output_stream: file
        :param avro_schema: A valid avro schema as a dict.
        :type avro_schema: dict
        """

        parsed_schema = fastavro.parse_schema(avro_schema)
        # IMPORTANT: I use the private module because the public API hasn't the
        # the required features.
        self.writer = fastavro._write.Writer(output_stream, parsed_schema)

    def write(self, row: dict):
        """A method to write an Avro row to the output_stream.
        
        :param row: A row of data that matchs with the current schema.
        :type row: dict
        :raises AvroMatchingException: When the provided row doesn't match with the current schema.
        """

        try:
            self.writer.write(row)
        except ValueError as ex:
            raise AvroMatchingException(f"Exception: {ex} for row -> {row}")

    def close(self):
        """Sends the buffer reamining data and closes the output stream
        """

        self.writer.flush()