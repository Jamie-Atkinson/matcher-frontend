# coding: utf-8
def output_keys(json, unwanted):
    """
    Extract only the values from the keys in the json that we are interested in 
    """
    values = json.values()
    keys = json.keys()
    return values, keys
