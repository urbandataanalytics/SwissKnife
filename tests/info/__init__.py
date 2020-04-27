import os
import imp
import SwissKnife

def set_env_variable(env: str, value: str):
    """Sets a new value for an environmental variable

    :param env: Environmental variable to be set
    :type env: str
    :param value: Value to be set
    :type value: str
    """
    os.environ[env] = value
    imp.reload(SwissKnife.info)
    
    
def delete_env_variable(env: str):
    """Delete an existing environmental variable

    :param env: Name of variable to delete
    :type env: str
    """
    if env in os.environ:
        del os.environ[env]
        imp.reload(SwissKnife.info)