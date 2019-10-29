import unittest
import os

from SwissKnife.info import current_env, EXECUTION_ENVIROMENT

class TestEnvMethods(unittest.TestCase):

    def _only_is_pro(self):
        
        self.assertTrue(current_env.is_pro())
        self.assertFalse(current_env.is_pre())
        self.assertFalse(current_env.is_dev())

        self.assertEqual(current_env.get_value() == EXECUTION_ENVIROMENT.PRO)

    def _only_is_pre(self):
        
        self.assertFalse(current_env.is_pro())
        self.assertTrue(current_env.is_pre())
        self.assertFalse(current_env.is_dev())

        self.assertEqual(current_env.get_value() == EXECUTION_ENVIROMENT.PRE)

    def _only_is_dev(self):

        self.assertFalse(current_env.is_pro())
        self.assertTrue(current_env.is_pre())
        self.assertTrue(current_env.is_dev())

        self.assertEqual(current_env.get_value() == EXECUTION_ENVIROMENT.DEV)

    def test_is_pro(self):

        for env_value in ["PRO", "pro", "pRo"]:
            os.environ["ENV"]=env_value
            self._only_is_pro()

    def test_is_pre(self):

        for env_value in ["PRE", "pre", "pRe"]:
            os.environ["ENV"]=env_value
            self._only_is_pre()

    def test_is_dev(self):

        for env_value in ["DEV", "dev", "dEv"]:
            os.environ["ENV"]=env_value
            self._only_is_dev()

    def test_set_pre_with_invalid_env_value(self):

        for env_value in ["asdfasdf", "PRU", "Der","",None]:
            os.environ["ENV"]=env_value
            self._only_is_pre()
