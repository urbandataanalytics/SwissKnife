import logging

from google.cloud import storage
from SwissKnife.info import BUCKET_NAME
from google.resumable_media import requests, common
from google.auth.transport.requests import AuthorizedSession
from SwissKnife.gcloud.GCloudStorage import GCloudStorage


class GCloudStreaming(object):
    """
    This class provide a file-like object that can upload very large files
    in a streaming way.

    Upload using a classic "write" function:
    
        with GCloudStreaming(blob_name='blob') as s:
            s.write(<DATOS>)
    """
    def __init__(
            self,
            blob_name: str,
            chunk_size: int=256 * 1024, # 256 Kb Todo To Be Tuned
            logger: logging.Logger=logging.getLogger("GCloudStreaming"),
            bucket_name: str = None
        ):
        """The constructor of a GCloudStreaming object
        
        :param blob_name: The blob path inside the bucket in Google Storage.
        :type blob_name: str
        :param chunk_size: The size of each chunk of data, defaults to 256*1024
        :type chunk_size: int, optional,
        :param logger: A custom logger.
        :type logger: logging.Logger
        :param bucket_name: If it's not desired to use BUCKET_PATH to determine the
                            bucket name, then set the bucket name using this variable.
        :type bucket_name: str
        """

        self.bucket_name = bucket_name if bucket_name else BUCKET_NAME
        self.blob_name = GCloudStorage.get_storage_complete_file_path(blob_name, with_gs=False)
        self.chunk_size = chunk_size

        self._client = None
        self._bucket = None
        self._blob = None

        self._transport = None

        self._buffer = b''
        self._buffer_size = 0
        self._read = 0

        self.logger = logger

        self._request = None  # type: requests.ResumableUpload

    def __enter__(self):
        """This method is executed at the "enter" of a "with" block.
        
        :return: Return itself.
        :rtype: GCloudStreaming
        """
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """This method is executed at the "exit" of a "with" block.
        The parameters can be None (no exception occurs) or not (there is an exception)
        
        :param exc_type: Type of the exception (if it exists). 
        :param exc_val: Value of the exception (if it exists).
        :param exc_tb: Traceback of the exception (if it exists).
        """
        if exc_type is None: # No hay excepcion
            self.stop()

    def start(self):
        """Start of the object (it connects to Google Storage).
        """
        full_path = GCloudStorage.get_storage_complete_file_path(self.blob_name, with_bucket=True, with_gs=True, with_prefix=False)
        self.logger.info(f'Uploaded file to gcloud (streaming) path {full_path}')

        self._client = storage.Client()
        self._bucket = self._client.bucket(self.bucket_name)
        self._blob = self._bucket.blob(self.blob_name)

        self._transport = AuthorizedSession(
            credentials=self._client._credentials
        )

        url = (
            'https://www.googleapis.com/upload/storage/v1/b/'
            '{0}/o?uploadType=resumable'.format(self._bucket.name)
        )
        self._request = requests.ResumableUpload(
            upload_url=url, chunk_size=self.chunk_size
        )
        self._request.initiate(
            transport=self._transport,
            content_type='application/octet-stream',
            stream=self,
            stream_final=False,
            metadata={'name': self._blob.name},
        )

    def flush(self):
        """For compatability purposes. Its is like "stop".
        """
        self.stop()

    def stop(self):
        """Ends the connection with Google Storage, seding the remaining data in the buffer.
        """
        self.logger.info("Upload process is finished!")
        self._request.transmit_next_chunk(self._transport)

    def seekable(self) -> bool:
        """A function that indicated if a stream is seekable
        (Someone can execute a "seek" method, avaiable in some file-like objects).
        For GCloudStreaming, this fuction always return False.
        
        :return: False, because GCloudStraming is not seekable.
        :rtype: bool
        """
        return False

    def write(self, data: str) -> int:
        """Write data to the buffer. If the buffer exceeds the maximum size,
        its content will be send to Google Storage and it will be refreshed.
        
        :param data: The input data.
        :type data: str
        :return: The length of the size of the data.
        :rtype: int
        """

        # Pasar el string a bytes
        if type(data) is str:
            data = str.encode(data)
        data_len = len(data)

        # Asignar tamaño de buffer y bytes con datos
        self._buffer_size += data_len
        self._buffer += data
        del data

        # Enviar datos mientras
        while self._buffer_size >= self.chunk_size:
            try:
                self._request.transmit_next_chunk(self._transport)
            except common.InvalidResponse: # Error de red
                self._request.recover(self._transport)

        return data_len

    def read(self, chunk_size: int) -> bytes:
        """
        Read the data of the buffer (all the buffer if the chunk_size is bigger than the total size)
        :param chunk_size: The desired size of data.
        :type chunk_size: int
        :return: The readed bytes.
        :rtype: bytes
        """
        to_read = min(chunk_size, self._buffer_size)
        memview = memoryview(self._buffer)
        self._buffer = memview[to_read:].tobytes()
        self._read += to_read
        self._buffer_size -= to_read
        return memview[:to_read].tobytes()

    def tell(self) -> int:
        return self._read