import unittest
from SwissKnife.avro.utils import chain_functions, object_as_tuple


class test_utils(unittest.TestCase):

    def test_two_functions_with_different_parameters(self):

        expected_res = 42

        def first_function(param_1, param_2):
            return (param_1, param_2, param_2+2)

        def second_function(param_1, param_2, param_3):
            return param_1 + param_2 + param_3

        chained_functions = chain_functions(first_function, second_function)

        self.assertEquals(chained_functions(20, 10), expected_res)

    def test_two_function_with_one_parameter(self):

        expected_res = 20

        def dummy_function(param_1):
            return param_1*2

        chained_functions = chain_functions(dummy_function, dummy_function)

        self.assertEquals(chained_functions(5), expected_res)

    def test_with_one_dict(self):

        expected_res = {"a": 20, "b": 50}

        def dummy_function(param_1):
            res = dict(param_1)
            res["a"] += 10
            return res

        chained_functions = chain_functions(dummy_function, dummy_function)

        self.assertEquals(chained_functions({"a": 0, "b": 50}), expected_res)

    def test_object_as_tuple(self):

        input_1 = 67
        input_2 = (76, 32)

        self.assertEqual(object_as_tuple(input_1), (67,)) 
        self.assertEqual(object_as_tuple(input_2), (76, 32)) 