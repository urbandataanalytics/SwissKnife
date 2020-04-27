import unittest

from SwissKnife.info import ExecutionEnvironment

class TestExecutionEnvironment(unittest.TestCase):

    def test_is_pro(self):

        for env_value in ["PRO", "pro", "pRo"]:
            execution_environment = ExecutionEnvironment.create(env_value)
            self._only_is_pro(execution_environment)


    def test_is_pre(self):

        for env_value in ["PRE", "pre", "pRe"]:
            execution_environment = ExecutionEnvironment.create(env_value)
            self._only_is_pre(execution_environment)


    def test_is_dev(self):

        for env_value in ["DEV", "dev", "dEv"]:
            execution_environment = ExecutionEnvironment.create(env_value)
            self._only_is_dev(execution_environment)


    def test_is_test(self):

        for env_value in ["TEST", "test", "TeST"]:
            execution_environment = ExecutionEnvironment.create(env_value)
            self._only_is_test(execution_environment)


    def test_set_pre_with_invalid_env_value(self):

        for env_value in ["asdfasdf", "PRU", "Der","",None]:
            execution_environment = ExecutionEnvironment.create(env_value)
            self._only_is_dev(execution_environment)


    def _only_is_pro(self, execution_environment: ExecutionEnvironment):
        
        self.assertTrue(execution_environment.is_pro())
        self.assertFalse(execution_environment.is_pre())
        self.assertFalse(execution_environment.is_dev())
        self.assertFalse(execution_environment.is_test())

        self.assertEqual(execution_environment, ExecutionEnvironment.PRO)


    def _only_is_pre(self, execution_environment: ExecutionEnvironment):
        
        self.assertFalse(execution_environment.is_pro())
        self.assertTrue(execution_environment.is_pre())
        self.assertFalse(execution_environment.is_dev())
        self.assertFalse(execution_environment.is_test())

        self.assertEqual(execution_environment, ExecutionEnvironment.PRE)


    def _only_is_dev(self, execution_environment: ExecutionEnvironment):

        self.assertFalse(execution_environment.is_pro())
        self.assertFalse(execution_environment.is_pre())
        self.assertTrue(execution_environment.is_dev())
        self.assertFalse(execution_environment.is_test())

        self.assertEqual(execution_environment, ExecutionEnvironment.DEV)


    def _only_is_test(self, execution_environment: ExecutionEnvironment):

        self.assertFalse(execution_environment.is_pro())
        self.assertFalse(execution_environment.is_pre())
        self.assertFalse(execution_environment.is_dev())
        self.assertTrue(execution_environment.is_test())

        self.assertEqual(execution_environment, ExecutionEnvironment.TEST)