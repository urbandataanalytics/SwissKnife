import os
import imp
import unittest
import SwissKnife
import tests.test_utils as test_utils

from unittest import mock
from SwissKnife.gcloud.GCloudStorage import GCloudStorage


class test_GCloudStorage(unittest.TestCase):
    
    def setUp(self):
        self.bucket_path_env_value = 'gs://fancy-bucket/files-should/have-this-prefix'
        self.bucket_name = 'fancy-bucket'
        self.bucket_path_prefix = 'files-should/have-this-prefix'
        
        test_utils.set_env_variable('BUCKET_PATH', self.bucket_path_env_value)
        imp.reload(SwissKnife.gcloud.GCloudStorage) # needed to reload BUCKET_PATH
        
    def test_path_complete_without_bucket_with_prefix(self):      
        file_path = 'random/path'
        file_name = 'blah.gif'
        expected = f'gs://{self.bucket_path_prefix}/{file_path}/{file_name}'
                
        result = GCloudStorage.get_storage_complete_file_path(file_name, file_path)
        
        self.assertEqual(expected, result)
        
    def test_path_complete_with_bucket_with_prefix(self):      
        file_path = 'random/path'
        file_name = 'blah.gif'
        expected = f'gs://fancy-bucket/{self.bucket_path_prefix}/{file_path}/{file_name}'
                
        result = GCloudStorage.get_storage_complete_file_path(file_name, file_path, with_bucket=True)
        
        self.assertEqual(expected, result)
        
    def test_path_complete_with_bucket_without_prefix(self):      
        file_path = 'random/path'
        file_name = 'blah.gif'
        expected = f'gs://fancy-bucket/{file_path}/{file_name}'
                
        result = GCloudStorage.get_storage_complete_file_path(file_name,
                                                              file_path,
                                                              with_bucket=True,
                                                              with_prefix=False)
        
        self.assertEqual(expected, result)
    
    @mock.patch('SwissKnife.gcloud.GCloudStorage.gcloud')
    def test_correct_data_type_to_upload(self, mock_gcloud):
        gc = GCloudStorage()
        file_path = 'random/path'
        file_name = 'blah.gif'
        expected = f'gs://fancy-bucket/{self.bucket_path_prefix}/{file_path}/{file_name}'
        
        data_types = ["str", "file"]
        for dt in data_types:
            self.assertEqual(expected, gc.save_to_storage("data",
                                                          None,
                                                          dt,
                                                          file_path,
                                                          file_name))
        
        
    @mock.patch('SwissKnife.gcloud.GCloudStorage.gcloud')
    def test_incorrect_data_type_to_upload(self, mock_gcloud):
        gc = GCloudStorage()
        file_path = 'random/path'
        file_name = 'blah.gif'
        expected = f'gs://fancy-bucket/{self.bucket_path_prefix}/{file_path}/{file_name}'
        
        wrong_data_types = ["string", "files", None, "gzip", "image"]
        with self.assertRaises(NotImplementedError):
            for dt in wrong_data_types:
                gc.save_to_storage("data",
                                    None,
                                    dt,
                                    file_path,
                                    file_name)
    
    """
        The rest of methods are not tested in this class, as they are mere
        rewrittings of code provided by Google. This tests would require, 
        as well, to have a working internet connection and a configured SA.
    """