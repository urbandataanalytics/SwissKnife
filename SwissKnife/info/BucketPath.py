from os import environ
    
def split_bucket_env() -> (str, str):
    """Basic function to extract the name of the bucket
    and the folder structure behind it. As several Google
    Storage libraries need to know just the name of the 
    bucket, it's needed to make this division. This 
    function returns a tuple in which the first element
    is the bucket name and the second one is a fixed
    path inside the bucket.
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

        splitted_env_var = env_var.replace("gs://", "").split("/")
        base_bucket = splitted_env_var[0]
        print("env_var:", env_var)
        path_prefix = "/".join(splitted_env_var[1:])
        print("path_prefix:", path_prefix)
        
        if base_bucket == "":
            raise RuntimeError(f"Invalid BUCKET_PATH -> {env_var}")

        return base_bucket, path_prefix        
        