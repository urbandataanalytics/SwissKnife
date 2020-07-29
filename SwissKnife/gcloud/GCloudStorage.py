import os
import logging
import google.cloud.storage as gcloud
from google.cloud.storage.blob import Blob
from SwissKnife.info.BucketPath import split_bucket


from SwissKnife.info import BUCKET_NAME, BUCKET_PATH_PREFIX


class GCloudStorage:

    def __init__(self,
                 logger: logging.Logger = logging.getLogger("GCloudStorage"),
                 bucket: str = None):
        """Creates a new GCloudStorage object. To do so, it's needed
        to have an environmental variable GOOGLE_APPLICATION_CREDENTIALS
        which contains the path of the SA that will be used for authentication.
        It's also a must to have an active Internet connection, otherwise the
        connection with the gcloud servers can not be performed.
        Also, this object use the environment variable "BUCKET_PATH" if bucket_name parameter is ignored (None).
        It will extract the BUCKET_NAME and the BUCKET_PATH_PREFIX using the "info" module. If BUCKET_PATH is not
        defined, an exception will be raised.

        :param logger: Logger object to use, defaults to logging.getLogger("GCloudStorage")
        :type logger: logging.Logger, optional
        :param bucket: bucket name to use. Bucket string is splitted in two parts: the name of the bucket
        and the folder structure behind it (bucket prefix path). If it is not set, then environment variable
        "BUCKET_PATH" is used.
        :type bucket: str, optional
        """

        if bucket:
            self.bucket_name, self.bucket_path_prefix = split_bucket(bucket)
        elif BUCKET_NAME:
            self.bucket_name = BUCKET_NAME
            self.bucket_path_prefix = BUCKET_PATH_PREFIX
        else:
            raise RuntimeError("bucket param or BUCKET_PATH environment variable not available.")

        self.storage_client = gcloud.Client()
        self.bucket = self.storage_client.get_bucket(self.bucket_name)
        self.logger = logger
        self.logger.info(f"Building a new gcloud Storage client for bucket {self.bucket_name}")

    def download_to_local_file(self,
                               gs_path: str,
                               local_path: str,
                               use_bucket_path_prefix: bool = True,
                               is_binary: bool = False):
        """This method downloads a file from the bucket to a local file. If the 'gs_path' is complete, it will be used.
        But, if it is only a subpath, it will be concatenated with the values BUCKET_NAME and BUCKET_PREFIX_PATH.

        :param gs_path: The path of the Google Storage file. It can be complete or only a subpath. 
        :type gs_path: str
        :param local_path: The path where the data will be writed 
        :type local_path: str
        :param use_bucket_path_prefix: Add the BUCKET_PATH_PREFIX to the gs_path if it is a subpath. Defaults to True
        :type use_bucket_path_prefix: bool, optional
        :param is_binary: A flag that indicates if it is a binary file, defaults to False
        :type is_binary: bool, optional
        :raises RuntimeError: Raises a RuntimeError if the download process fails. 
        """

        if gs_path.startswith("gs://"):
            # It is a complete path. so, it will use a custom bucket
            gs_length = len("gs://")
            parts = gs_path[gs_length:].split("/")
            bucket_name = parts[0]
            file_path = "/".join(parts[1:])
            bucket = self.storage_client.get_bucket(bucket_name)
        else:
            # It is not a complete path. So, it will use the bucket configuration defined in constructor
            bucket = self.bucket
            file_path = os.path.join(self.bucket_path_prefix if use_bucket_path_prefix else '', gs_path)

        # The file cloud be binary
        write_opts = "wb" if is_binary else "w"
        try:
            self.logger.info(f"Downloading file '{file_path}' into file '{local_path}'")

            blob_from = bucket.blob(file_path)

            with open(local_path, write_opts) as f:
                blob_from.download_to_file(f)

        except Exception as e:
            self.logger.exception("Error downloading file from gcloud", exc_info=True)
            raise RuntimeError(f"Error downloading file from gcloud : {e}")

    def save_file(self,
                  origin_local_path: str,
                  destination_file_name: str,
                  destination_storage_path: str,
                  encoding: str = None,
                  metadata: dict = None) -> str:
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
        :param metadata: Key value metadata that will be associated to the file
        :type metadata: dict
        :return: Storage path were the file has been uploaded
        :rtype: str
        """
        return self.save_to_storage(data=origin_local_path,
                                    data_encoding=encoding,
                                    data_type='file',
                                    destination_storage_path=destination_storage_path,
                                    destination_file_name=destination_file_name,
                                    metadata=metadata)

    def save_string(self,
                    origin_data_str: str,
                    destination_file_name: str,
                    destination_storage_path: str,
                    encoding: str = None,
                    metadata: dict = None
                    ) -> str:
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
        :param metadata: Key value metadata that will be associated to the file
        :type metadata: dict
        :return: Storage path were the file has been uploaded
        :rtype: str
        """
        return self.save_to_storage(data=origin_data_str,
                                    data_encoding=encoding,
                                    data_type='str',
                                    destination_storage_path=destination_storage_path,
                                    destination_file_name=destination_file_name,
                                    metadata=metadata)

    def save_to_storage(self,
                        data,
                        data_encoding: str,
                        data_type: str,
                        destination_storage_path: str,
                        destination_file_name: str,
                        metadata: dict = None) -> str:
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
        :param metadata: Key value metadata that will be associated to the file
        :type metadata: dict
        :raises NotImplementedError: When the data type provided is not implemented
        :return: gcloud storage of the uploaded file
        :rtype: str
        """
        blob = self.__generate_blob(destination_storage_path, destination_file_name, data_encoding, metadata)

        if data_type == 'str':
            blob.upload_from_string(data)
        elif data_type == 'file':
            blob.upload_from_filename(data)
        else:
            raise NotImplementedError

        file_path = self.get_storage_complete_file_path(destination_file_name, destination_storage_path,
                                                        with_bucket=True)

        self.logger.info(f"Uploaded file to gcloud path {file_path}")
        return file_path

    def __generate_blob(self,
                        file_path: str,
                        file_name: str,
                        encoding: str,
                        metadata: dict = None) -> gcloud.blob.Blob:
        """Creates a new Blob with the specified path and name.
        Before uploading a file to gcloud it is needed to first
        generate a Blob containing basic info such as name and encoding.

        :param file_path: Gcloud Storage path of the blob
        :type file_path: str
        :param file_name: Name of the blob in Storage
        :type file_name: str
        :param encoding: Encoding of the file
        :type encoding: str
        :param metadata: Key value metadata that will be associated to the file
        :type metadata: dict
        :return: Blob object with updated metadata
        :rtype: google.cloud.storage.blob.Blob
        """
        blob_name = self.get_storage_complete_file_path(file_name, file_path, with_gs=False)
        blob = self.bucket.blob(blob_name)
        blob.metadata = metadata

        if encoding:
            blob.content_encoding = encoding

        return blob

    def get_storage_complete_file_path(self,
                                       file_name: str = None,
                                       file_path: str = None,
                                       with_bucket: bool = False,
                                       with_prefix: bool = True,
                                       with_gs: bool = True) -> str:
        """Returns the complete path of a file stored in gcloud.

        :param file_path: Path of the file, without bucket
        :type file_path: str
        :param file_name: Name of the file
        :type file_name: str
        :param with_bucket: Whether bucket will be returned or not, defaults to False
        :type with_bucket: bool, optional
        :param with_prefix: If with_prefix is set, bucket path prefix is used. Defaults to True
        :type with_prefix: bool, optional
        :param with_gs: If the string gs:// should be added to the path or not
        :type with_gs: bool, optional, True by default
        :return: Complete path of a file stored in gcloud
        :rtype: str
        """
        bucket_name = self.bucket_name if with_bucket else ''
        file_prefix = self.bucket_path_prefix if with_prefix and self.bucket_path_prefix else ''
        final_file_path = file_path if file_path else ''
        gs_prefix = 'gs://' if with_gs else ''
        final_file_name = file_name if file_name else ''

        return os.path.join(gs_prefix, bucket_name, file_prefix, final_file_path, final_file_name)

    def list_blobs(self,
                   storage_path: str,
                   with_prefix: bool = True) -> "Iterator":
        """Lists all the files that exists in the specified path.
        This is similar to GNU's `ls` command. Returns an iterator
        that should be treated later on.

        :param storage_path: Parent path from which files will be listed(without slash at the end)
        :type storage_path: str
        :param with_prefix: this adds or not the BUCKET_PREFIX_PATH to the resulting path
        :type with_prefix: bool
        :return: Iterator with blobs contained in the parent path
        :rtype: "Iterator"
        """

        list_prefix = self.get_storage_complete_file_path(file_path=storage_path,
                                                          with_prefix=with_prefix,
                                                          with_gs=False)
        return self.bucket.list_blobs(prefix=list_prefix)

    def copy_blob(self, src_blob: Blob, dst_storage: "GCloudStorage", dst_file_name: str) -> Blob:
        """Copy a file to a new location (in the same or in another bucket) with a new name
        using the google cloud api directly.

        :param src_blob: The blob to copy. 
        :type src_blob: Blob
        :param dst_storage: The destination bucket.
        :type dst_storage: GCloudStorage
        :param dst_file_name: The new file name. 
        :type dst_file_name: str
        :return: The resulting blob.
        :rtype: Blob
        """

        destination_bucket = dst_storage.bucket 
        dst_path = dst_storage.get_storage_complete_file_path(file_name=dst_file_name, with_prefix=True, with_bucket=False, with_gs=False)

        dst_blob = self.bucket.copy_blob(src_blob, destination_bucket, dst_path)

        # Log complete paths
        complete_src_path = self.get_storage_complete_file_path(file_name=src_blob.name, with_bucket=True, with_prefix=True, with_gs=True)
        complete_dst_path = dst_storage.get_storage_complete_file_path(file_name=dst_blob.name, with_bucket=True, with_prefix=True, with_gs=True) 
        self.logger.info(f"Blob {complete_src_path} copied to blob {complete_dst_path}")

        return dst_blob


