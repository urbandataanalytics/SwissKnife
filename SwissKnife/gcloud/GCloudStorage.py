import sys
import logging
import google.cloud.storage as gcloud

from SwissKnife.info import BUCKET_NAME, BUCKET_PATH_PREFIX


class GCloudStorage:

    def __init__(self, logger: logging.Logger = logging.getLogger("GCloudStorage")):
        """Creates a new GCloudStorage object. To do so, it's needed
        to have an environmental variable GOOGLE_APPLICATION_CREDENTIALS
        which contains the path of the SA that will be used for authentication.
        It's also a must to have an active Internet connection, otherwise the
        connection with the gcloud servers can not be performed.

        :param logger: Logger object to use, defaults to logging.getLogger("GCloudStorage")
        :type logger: logging.Logger, optional
        """
        self.logger = logger
        self.logger.info(f"Building a new gcloud Storage client for bucket {BUCKET_NAME}")
        self.storage_client = gcloud.Client()
        self.bucket = self.storage_client.get_bucket(BUCKET_NAME)
        
    def save_file(self,
                  origin_local_path: str,
                  destination_file_name: str,
                  destination_storage_path: str,
                  encoding: str=None) -> str:
        """Uploads a file from a local path to a destination
        located in a gcloud bucket.

        :param origin_local_path: Local path of the file to upload
        :type origin_local_path: str
        :param destination_file_name: Name that it will have in Storage
        :type destination_file_name: str
        :param destination_storage_path: Storage path were it'll be stored
        :type destination_storage_path: str
        :param encoding: Specific encoding of the file, defaults to None
        :type encoding: str, optional
        :return: Storage path were the file has been uploaded
        :rtype: str
        """
        return self.save_to_storage(data=origin_local_path,
                                    data_encoding=encoding,
                                    data_type='file',
                                    destination_storage_path=destination_storage_path,
                                    destination_file_name=destination_file_name
                                    )

    def save_string(self,
                    origin_data_str: str,
                    destination_file_name: str,
                    destination_storage_path: str,
                    encoding: str=None) -> str:
        """Transforms a string to a text file and uploads it to
        gcloud Storage.

        :param origin_data_str: String to save in a file
        :type origin_data_str: str
        :param destination_file_name: Name that it will have in Storage
        :type destination_file_name: str
        :param destination_storage_path: Storage path were it'll be stored
        :type destination_storage_path: str
        :param encoding: Specific encoding of the file, defaults to None
        :type encoding: str, optional
        :return: Storage path were the file has been uploaded
        :rtype: str
        """
        return self.save_to_storage(data=origin_data_str,
                                    data_encoding=encoding,
                                    data_type='str',
                                    destination_storage_path=destination_storage_path,
                                    destination_file_name=destination_file_name
                                    )
    
    def save_to_storage(self,
                        data,
                        data_encoding: str,
                        data_type: str,
                        destination_storage_path: str,
                        destination_file_name: str) -> str:
        """Uploads data, which may come in several formats, to
        Storage. Accepted data types are 'file' and 'str', matching
        methods save_file and save_string of this same class.

        :param data: Data file or string that will be uploaded
        :type data: [type]
        :param data_encoding: Specific encoding of the file
        :type data_encoding: str
        :param data_type: Type of data to upload: file or string
        :type data_type: str
        :param destination_storage_path: Storage path were it'll be stored
        :type destination_storage_path: str
        :param destination_file_name: Name that it will have in Storage
        :type destination_file_name: str
        :raises NotImplementedError: When the data type provided is not implemented
        :return: gcloud storage of the uploaded file
        :rtype: str
        """
        blob = self.__generate_blob(destination_storage_path, destination_file_name, data_encoding)
        
        if data_type == 'str':
            blob.upload_from_string(data)
        elif data_type == 'file':
            blob.upload_from_filename(data)
        else:
            raise NotImplementedError
        
        file_path = self.get_storage_complete_file_path(destination_file_name, destination_storage_path, with_bucket=True)
        
        self.logger.info(f"Uploaded file to gcloud path {file_path}")
        return file_path
        
    def __generate_blob(self, 
                        file_path: str,
                        file_name: str,
                        encoding: str) -> gcloud.blob.Blob:
        """Creates a new Blob with the specified path and name.
        Before uploading a file to gcloud it is needed to first
        generate a Blob containing basic info such as name and encoding.

        :param file_path: Gcloud Storage path of the blob
        :type file_path: str
        :param file_name: Name of the blob in Storage
        :type file_name: str
        :param encoding: Encoding of the file
        :type encoding: str
        :return: Blob object with updated metadata
        :rtype: google.cloud.storage.blob.Blob
        """
        blob_name = self.get_storage_complete_file_path(file_name, file_path, with_gs=False)
        blob = self.bucket.blob(blob_name)
        
        if encoding:
            blob.content_encoding = encoding
            
        return blob
    
    @staticmethod
    def get_storage_complete_file_path(file_name: str,
                                       file_path: str=None,
                                       with_bucket: bool=False,
                                       with_prefix: bool=True,
                                       with_gs: bool=True) -> str:
        """Returns the complete path of a file stored in gcloud.

        :param file_path: Path of the file, without bucket
        :type file_path: str
        :param file_name: Name of the file
        :type file_name: str
        :param with_bucket: If the bucket will be returned, defaults to False
        :type with_bucket: bool, optional
        :param with_prefix: If prefix set by BUCKET_PATH_PREFIX is used, defaults to True
        :type with_prefix: bool, optional
        :param with_gs: If the string gs:// should be added to the path or not
        :type with_gs: bool, optional, True by default
        :return: Complete path of a file stored in gcloud
        :rtype: str
        """
        bucket_name = f'{BUCKET_NAME}/' if with_bucket else ''
        file_prefix = f'{BUCKET_PATH_PREFIX}/' if with_prefix and BUCKET_PATH_PREFIX else ''
        path = f'{file_path}/' if file_path else ''
        gs_prefix = 'gs://' if with_gs else ''
        
        return f'{gs_prefix}{bucket_name}{file_prefix}{path}{file_name}'

    def list_blobs(self, storage_path: str) -> "Iterator":
        """Lists all the files that exists in the specified path.
        This is similar to GNU's `ls` command. Returns an iterator
        that should be treated later on.

        :param storage_path: Parent path from which files will be listed
        :type storage_path: str
        :return: Iterator with blobs contained in the parent path
        :rtype: "Iterator"
        """
        return self.bucket.list_blobs(prefix=storage_path)