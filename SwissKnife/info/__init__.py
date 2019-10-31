import os

# With this, we can import directly the class without importing the module.
from SwissKnife.info.ExecutionEnvironment import ExecutionEnvironment


if "ENV" in os.environ:
    CURRENT_ENVIRONMENT = ExecutionEnvironment.create(os.environ["ENV"])
else:
    CURRENT_ENVIRONMENT = ExecutionEnvironment.create(None)