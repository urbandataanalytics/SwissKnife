import os

# With this, we can import directly the class without importing the module.
from SwissKnife.info.ExecutionEnvironment import ExecutionEnvironment

CURRENT_ENVIRONMENT = ExecutionEnvironment.create(os.environ.get('ENV', None))
BUCKET_PATH = os.environ.get('BUCKET_PATH', None)