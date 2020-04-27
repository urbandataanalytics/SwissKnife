import unittest
import os
import imp

import SwissKnife
import SwissKnife.info
import tests.info as test_utils

class Test_BUCKET_PATH(unittest.TestCase):
    
    def test_is_defined(self):
        """
        Check if the environment variable is retrieved when it's defined
        """
        correct_values = ["gs://bucket", "bucket", "_", " "]
        for val in correct_values:
            test_utils.set_env_variable("BUCKET_PATH", val)
            self.assertEqual(val, SwissKnife.info.BUCKET_PATH)


    def test_not_defined(self):
        """
        Check the value when the variable is not defined
        """
        test_utils.delete_env_variable("BUCKET_PATH")
        self.assertIsNone(SwissKnife.info.BUCKET_PATH)
