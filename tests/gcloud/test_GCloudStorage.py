import os
import imp
import unittest
import SwissKnife
import tests.test_utils as test_utils
from unittest.mock import MagicMock

from unittest import mock
from SwissKnife.gcloud.GCloudStorage import GCloudStorage


class TestGCloudStorage(unittest.TestCase):

    def setUp(self):
        self.bucket_path_env_value = 'gs://fancy-bucket/files-should/have-this-prefix'
        self.bucket_name = 'fancy-bucket'
        self.bucket_path_prefix = 'files-should/have-this-prefix'

        self.bucket_path_param = 'gs://not-so-fancy-bucket/path/prefix-param'
        self.bucket_name_param = 'not-so-fancy-bucket'
        self.bucket_path_prefix_param = 'path/prefix-param'

        test_utils.set_env_variable('BUCKET_PATH', self.bucket_path_env_value)
        imp.reload(SwissKnife.gcloud.GCloudStorage)  # needed to reload BUCKET_PATH

    def GCloudStorage_raises_an_exception_when_bucket_path_is_not_defined(self):

        test_utils.set_env_variable('BUCKET_PATH', None)
        imp.reload(SwissKnife.gcloud.GCloudStorage)  # needed to reload BUCKET_PATH

        with self.assertRaises(RuntimeError) as ex:
            gcs = GCloudStorage()

        self.assertTrue("invalid BUCKET PATH" in str(ex.exception))

    @mock.patch('SwissKnife.gcloud.GCloudStorage.gcloud')
    def test_path_complete_without_bucket_with_prefix(self, mock_gcloud):
        file_path = 'random/path'
        file_name = 'blah.gif'
        expected = f'gs://{self.bucket_path_prefix}/{file_path}/{file_name}'
        gcs = GCloudStorage()
        result = gcs.get_storage_complete_file_path(file_name, file_path)
        self.assertEqual(expected, result)

    @mock.patch('SwissKnife.gcloud.GCloudStorage.gcloud')
    def test_path_complete_with_bucket_with_prefix(self, mock_gcloud):
        file_path = 'random/path'
        file_name = 'blah.gif'
        expected = f'gs://fancy-bucket/{self.bucket_path_prefix}/{file_path}/{file_name}'
        gcs = GCloudStorage()
        result = gcs.get_storage_complete_file_path(file_name, file_path, with_bucket=True)
        self.assertEqual(expected, result)

    @mock.patch('SwissKnife.gcloud.GCloudStorage.gcloud')
    def test_path_complete_with_bucket_without_prefix(self, mock_gcloud):
        file_path = 'random/path'
        file_name = 'blah.gif'
        expected = f'gs://fancy-bucket/{file_path}/{file_name}'
        gcs = GCloudStorage()
        result = gcs.get_storage_complete_file_path(file_name,
                                                    file_path,
                                                    with_bucket=True,
                                                    with_prefix=False)
        self.assertEqual(expected, result)

    @mock.patch('SwissKnife.gcloud.GCloudStorage.gcloud')
    def test_path_without_file_name(self, mock_gcloud):
        file_path = 'random/path'
        expected = f'gs://fancy-bucket/{file_path}/'
        gcs = GCloudStorage()
        result = gcs.get_storage_complete_file_path(
            file_path=file_path,
            with_bucket=True,
            with_prefix=False
        )
        self.assertEqual(expected, result)

    @mock.patch('SwissKnife.gcloud.GCloudStorage.gcloud')
    def test_correct_data_type_to_upload(self, mock_gcloud):
        gc = GCloudStorage()
        file_path = 'random/path'
        file_name = 'blah.gif'
        expected = f'gs://fancy-bucket/{self.bucket_path_prefix}/{file_path}/{file_name}'

        data_types = ["str", "file"]
        metadata = {'key': 'test'}
        for dt in data_types:
            self.assertEqual(expected, gc.save_to_storage("data",
                                                          None,
                                                          dt,
                                                          file_path,
                                                          file_name,
                                                          metadata=metadata))
            self.assertEqual(metadata, mock_gcloud.Client().get_bucket().blob().metadata)

    @mock.patch('SwissKnife.gcloud.GCloudStorage.gcloud')
    def test_correct_data_type_to_upload_with_bucket_param(self, mock_gcloud):
        gc = GCloudStorage(bucket=self.bucket_path_param)
        file_path = 'random/path'
        file_name = 'blah.gif'
        expected = f'gs://{self.bucket_name_param}/{self.bucket_path_prefix_param}/{file_path}/{file_name}'

        data_types = ["str", "file"]
        metadata = {'key': 'test'}
        for dt in data_types:
            self.assertEqual(expected, gc.save_to_storage("data",
                                                          None,
                                                          dt,
                                                          file_path,
                                                          file_name,
                                                          metadata=metadata))
            self.assertEqual(metadata, mock_gcloud.Client().get_bucket().blob().metadata)

    @mock.patch('SwissKnife.gcloud.GCloudStorage.gcloud')
    def test_incorrect_data_type_to_upload(self, mock_gcloud):
        gc = GCloudStorage()
        file_path = 'random/path'
        file_name = 'blah.gif'

        wrong_data_types = ["string", "files", None, "gzip", "image"]
        with self.assertRaises(NotImplementedError):
            for dt in wrong_data_types:
                gc.save_to_storage("data",
                                   None,
                                   dt,
                                   file_path,
                                   file_name)

    @mock.patch('SwissKnife.gcloud.GCloudStorage.gcloud')
    def test_incorrect_data_type_to_upload_with_bucket_param(self, mock_gcloud):
        gc = GCloudStorage(bucket=self.bucket_path_param)
        file_path = 'random/path'
        file_name = 'blah.gif'

        wrong_data_types = ["string", "files", None, "gzip", "image"]
        with self.assertRaises(NotImplementedError):
            for dt in wrong_data_types:
                gc.save_to_storage("data",
                                   None,
                                   dt,
                                   file_path,
                                   file_name)

    @mock.patch('SwissKnife.gcloud.GCloudStorage.gcloud')
    def test_valid_path_in_list_blobs_with_prefix(self, mock_gcloud):

        storage_path = 'random_path'
        expected = f'{self.bucket_path_prefix}/{storage_path}/'

        def assert_path_in_list_blobs(prefix):
            self.assertEqual(prefix, expected)

        mocked_bucket = MagicMock()
        mocked_bucket.list_blobs = assert_path_in_list_blobs

        gc = GCloudStorage()
        gc.bucket = mocked_bucket

        gc.list_blobs(storage_path)

    @mock.patch('SwissKnife.gcloud.GCloudStorage.gcloud')
    def test_valid_path_in_list_blobs_with_prefix_with_bucket_param(self, mock_gcloud):

        storage_path = 'random_path'
        expected = f'{self.bucket_path_prefix_param}/{storage_path}/'

        def assert_path_in_list_blobs(prefix):
            self.assertEqual(prefix, expected)

        mocked_bucket = MagicMock()
        mocked_bucket.list_blobs = assert_path_in_list_blobs

        gc = GCloudStorage(bucket=self.bucket_path_param)
        gc.bucket = mocked_bucket

        gc.list_blobs(storage_path)

    @mock.patch('SwissKnife.gcloud.GCloudStorage.gcloud')
    def test_valid_path_in_list_blobs_without_prefix(self, mock_gcloud):

        storage_path = 'random_path'
        expected = f'{storage_path}/'

        def assert_path_in_list_blobs(prefix):
            self.assertEqual(prefix, expected)

        mocked_bucket = MagicMock()
        mocked_bucket.list_blobs = assert_path_in_list_blobs

        gc = GCloudStorage()
        gc.bucket = mocked_bucket

        gc.list_blobs(storage_path, with_prefix=False)

    @mock.patch('SwissKnife.gcloud.GCloudStorage.gcloud')
    def test_valid_path_in_list_blobs_without_prefix_with_bucket_param(self, mock_gcloud):

        storage_path = 'random_path'
        expected = f'{storage_path}/'

        def assert_path_in_list_blobs(prefix):
            self.assertEqual(prefix, expected)

        mocked_bucket = MagicMock()
        mocked_bucket.list_blobs = assert_path_in_list_blobs

        gc = GCloudStorage(bucket=self.bucket_path_param)
        gc.bucket = mocked_bucket

        gc.list_blobs(storage_path, with_prefix=False)

    """
        The rest of methods are not tested in this class, as they are mere
        rewrittings of code provided by Google. This tests would require, 
        as well, to have a working internet connection and a configured SA.
    """
