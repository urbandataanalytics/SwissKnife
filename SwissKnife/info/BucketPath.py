from os import environ
    

def split_bucket(bucket_path: str) -> (str, str):
    """Function to extract the name of the bucket
    and the folder structure behind it. As several Google
    Storage libraries need to know just the name of the
    bucket, it's needed to make this division. This
    function returns a tuple in which the first element
    is the bucket name and the second one is a fixed
    path inside the bucket.
    :return: Bucket name, bucket path prefix
    :rtype: (str, str)
    """
    if "gs://" not in bucket_path:
        raise RuntimeError(f"Invalid BUCKET_PATH -> {bucket_path}")
    else:
        splitted_bucket = bucket_path.replace("gs://", "").split("/")
        base_bucket = splitted_bucket[0]
        path_prefix = "/".join(splitted_bucket[1:])
        if base_bucket == "":
            raise RuntimeError(f"Invalid BUCKET_PATH -> {bucket_path}")

        return base_bucket, path_prefix


def split_bucket_env() -> (str, str):
    """Basic function to extract the name of the bucket and the folder structure behind it.
    Bucket is taken from BUCKET_PATH environment variable.
    If the BUCKET_PATH is not defined, it will return (None, None)

    :return: Bucket name, bucket path prefix
    :rtype: (str, str)
    """
    env_var = environ.get('BUCKET_PATH', None)

    if env_var is None:
        return (None, None)
    elif "gs://" not in env_var:
        raise RuntimeError(f"Invalid BUCKET_PATH -> {env_var}")
    else:
        return split_bucket(env_var)
