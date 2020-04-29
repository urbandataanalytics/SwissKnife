import os

from SwissKnife.info.BucketPath import split_bucket_env
from SwissKnife.info.ExecutionEnvironment import ExecutionEnvironment

CURRENT_ENVIRONMENT = ExecutionEnvironment.create(os.environ.get('ENV', None))
BUCKET_NAME, BUCKET_PATH_PREFIX = split_bucket_env()