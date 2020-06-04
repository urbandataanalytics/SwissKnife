



def chain_functions(*functions_list):

    def wrapper_function(*input_args):

        res = input_args
        print("input:", input_args)

        for single_function in functions_list:
            args_as_list = object_as_tuple(res)
            print("args:", args_as_list)
            res = single_function(*args_as_list) 

        return res
    
    return wrapper_function


def object_as_tuple(obj):

    if isinstance(obj, tuple):
        return obj
    else:
        return (obj,)