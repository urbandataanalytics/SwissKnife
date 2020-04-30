import unittest
import os
import imp

import SwissKnife
import SwissKnife.info
import tests.test_utils as test_utils

class Test_BUCKET_PATH(unittest.TestCase):
    
    def test_is_defined_with_preffix(self):
        """
        Check if the environment variable is retrieved when it's defined
        """
        full_bucket_path = "gs://bucket-name/some/random/route"
        bucket_name = "bucket-name"
        path_preffix = "some/random/route"
        
        test_utils.set_env_variable("BUCKET_PATH", full_bucket_path)
        
        self.assertEqual(bucket_name, SwissKnife.info.BUCKET_NAME)
        self.assertEqual(path_preffix, SwissKnife.info.BUCKET_PATH_PREFIX)


    def test_is_defined_without_preffix(self):
        """
        Check if the environment variable is retrieved when it's defined
        """
        full_bucket_path = "gs://bucket-name"
        bucket_name = "bucket-name"
        path_preffix = ""
        
        test_utils.set_env_variable("BUCKET_PATH", full_bucket_path)
        
        self.assertEqual(bucket_name, SwissKnife.info.BUCKET_NAME)
        self.assertEqual(path_preffix, SwissKnife.info.BUCKET_PATH_PREFIX)


    def test_not_defined(self):
        """
        Check the value when the variable is not defined
        """
        test_utils.delete_env_variable("BUCKET_PATH")
        self.assertEqual("", SwissKnife.info.BUCKET_NAME)
        self.assertEqual("", SwissKnife.info.BUCKET_PATH_PREFIX)