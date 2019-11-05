import unittest
import os
import imp

import SwissKnife
import SwissKnife.info

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


    
    def _set_current_env(self, env_str: str):
        """
            We have to set the variable and reimport the module
            to set the CURRENT_ENVIRONMENT variable.
        """
        os.environ["ENV"] = env_str
        imp.reload(SwissKnife.info)