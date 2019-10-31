from enum import Enum


class ExecutionEnvironment(Enum):
    """ExutionEnvironment is a Enum that represents a possible ExecutionEnvironment.
    Valid values are PRO, PRE and DEV. PRE is the default value.
    The static method "create" is the preferred method to create and ExecutionEnvironment because
    it transform the input to an standard form (lower case) and return the default value (PRE)
    if a invalid value (or a null value) is provided. 
    """

    PRO = "pro"
    PRE = "pre"
    DEV = "dev"
    
    @staticmethod
    def create(env_str: str) -> "ExecutionEnvironment":
        """Create an ExecutionEnvironment from the provided text. Convert it
        convert it to "lower case" and match the result with one of the possibilities.
        If there is not a match, PRE value will be the final result.
        
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
        """Return if the value of this ExecutionEnvironment is PRO.
        
        :return: True if this ExecutionEnvironment is PRO.
        :rtype: bool
        """
        return self == ExecutionEnvironment.PRO

    def is_pre(self):
        """Return if the value of this ExecutionEnvironment is PRE.
        
        :return: True if this ExecutionEnvironment is PRE.
        :rtype: bool
        """

        return self == ExecutionEnvironment.PRE

    def is_dev(self):
        """Return if the value of this ExecutionEnvironment is DEV.
        
        :return: True if this ExecutionEnvironment is DEV.
        :rtype: bool
        """

        return self == ExecutionEnvironment.DEV