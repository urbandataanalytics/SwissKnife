import os
import imp
import json
import unittest

import SwissKnife
import SwissKnife.info
import tests.test_utils as test_utils

class Test_CURRENT_ENVIRONMENT(unittest.TestCase):

    def test_is_pro(self):

        for env_value in ["pro", "PRO", "pRo", "prO"]:
            self._set_current_env(env_value)
            self.assertTrue(SwissKnife.info.CURRENT_ENVIRONMENT.is_pro())


    def test_is_pre(self):

        for env_value in ["pre", "PRE", "pRe", "prE"]:
            self._set_current_env(env_value)
            self.assertTrue(SwissKnife.info.CURRENT_ENVIRONMENT.is_pre())


    def test_is_dev(self):

        for env_value in ["dev", "DEV", "Dev", "DEv"]:
            self._set_current_env(env_value)
            self.assertTrue(SwissKnife.info.CURRENT_ENVIRONMENT.is_dev())


    def test_is_test(self):

        for env_value in ["test", "TEST", "TeSt", "TEst"]:
            self._set_current_env(env_value)
            self.assertTrue(SwissKnife.info.CURRENT_ENVIRONMENT.is_test())


    def test_invalid_values(self):

        for env_value in ["prU", "PRA", "asdfsdf", "unknown"]:
            self._set_current_env(env_value)
            self.assertTrue(SwissKnife.info.CURRENT_ENVIRONMENT.is_dev())
            
    def test_is_json_serializable(self):
        self._set_current_env('TEST')
        expected = '"test"'
        actual = json.dumps(SwissKnife.info.CURRENT_ENVIRONMENT)
        self.assertEqual(expected, actual)


    def _set_current_env(self, env_str: str):
        test_utils.set_env_variable("ENV", env_str)