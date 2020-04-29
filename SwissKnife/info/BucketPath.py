from os import environ
    
def split_bucket_env() -> (str, str):
    """Basic function to extract the name of the bucket
    and the folder structure behind it. As several Google
    Storage libraries need to know just the name of the 
    bucket, it's needed to make this division. This 
    function returns a tuple in which the first element
    is the bucket name and the second one is a fixed
    path inside the bucket.

    :return: Bucket name, bucket path prefix
    :rtype: (str, str)
    """
    env_var = environ.get('BUCKET_PATH', "")
    splitted_env_var = env_var.replace("gs://", "").split("/")
    
    base_bucket = splitted_env_var[0]
    path_preffix = "" if len(splitted_env_var) == 1 else "/".join(splitted_env_var[1:])
    
    return base_bucket, path_preffix        
        