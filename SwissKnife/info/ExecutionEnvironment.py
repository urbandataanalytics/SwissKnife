from enum import Enum


class ExecutionEnvironment(Enum):
    """
        Execution environment

        Devuelve pro y esas cosas
    """

    PRO = "pro"
    PRE = "pre"
    DEV = "dev"

    @staticmethod
    def create(env_str: str) -> "ExecutionEnvironment":

        # Is none or other invalid type.
        if type(env_str) is not str:
            return ExecutionEnvironment("pre")

        try:
            return ExecutionEnvironment(env_str.lower())
        except ValueError:
            return ExecutionEnvironment("pre")

    def is_pro(self):
        """
            Return if the current execution environment is PRO.

            Returns
            -------
            bool
                True is this execution environment is PRO, False otherwise.
        """

        return self == ExecutionEnvironment.PRO

    def is_pre(self):

        return self == ExecutionEnvironment.PRE

    def is_dev(self):

        return self == ExecutionEnvironment.DEV


if __name__ == "__main__":
    help(ExecutionEnvironment.is_pro)