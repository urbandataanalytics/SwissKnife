import os

# With this, we can import directly the class without importing the module.
from SwissKnife.info.ExecutionEnvironment import ExecutionEnvironment

CURRENT_ENVIRONMENT = ExecutionEnvironment.create(os.environ.get('ENV', None))