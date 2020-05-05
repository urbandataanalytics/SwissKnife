from enum import Enum


class ExecutionEnvironment(str, Enum):
    """ExutionEnvironment is an Enum that represents a possible ExecutionEnvironment.
    Valid values are PRO, PRE, DEV and TEST. DEV is the default value.
    The static method "create" is the preferred method to create an ExecutionEnvironment because
    it transforms the input to a standard form (lower case). It will return the default value (DEV)
    if an invalid value (or a null value) is provided. 
    
    By inhereting both str and Enum we automatically make our enumeration
    JSON serlizable. It's also needed to annotate the type of the enum
    values.
    """

    PRO: str = "pro"
    PRE: str = "pre"
    DEV: str = "dev"
    TEST: str = "test"
    
    @staticmethod
    def create(env_str: str) -> "ExecutionEnvironment":
        """Create an ExecutionEnvironment from the provided text. Converts it
        to "lower case" and matches the result with one of the possibilities.
        If there is not a match, the default value will be returned (DEV).
        
        :param env_str: Environment value in text format.
        :type env_str: str
        :return: An ExecutionEnvironment based on the previous value.
        :rtype: ExecutionEnvironment
        """
        default_env = ExecutionEnvironment.DEV

        # Is none or other invalid type.
        if type(env_str) is not str:
            return default_env

        try:
            return ExecutionEnvironment(env_str.lower())
        except ValueError:
            return default_env

    def is_pro(self):
        """Indicates if the value of this ExecutionEnvironment is PRO.
        
        :return: True if this ExecutionEnvironment is PRO.
        :rtype: bool
        """
        return self == ExecutionEnvironment.PRO

    def is_pre(self):
        """Indicates if the value of this ExecutionEnvironment is PRE.
        
        :return: True if this ExecutionEnvironment is PRE.
        :rtype: bool
        """

        return self == ExecutionEnvironment.PRE

    def is_dev(self):
        """Indicates if the value of this ExecutionEnvironment is DEV.
        
        :return: True if this ExecutionEnvironment is DEV.
        :rtype: bool
        """

        return self == ExecutionEnvironment.DEV

    def is_test(self):
        """Indicates if the value of this ExecutionEnvironment is TEST.
        
        :return: True if this ExecutionEnvironment is TEST.
        :rtype: bool
        """

        return self == ExecutionEnvironment.TEST