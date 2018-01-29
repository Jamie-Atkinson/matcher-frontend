# coding: utf-8
def output_keys(json, unwanted):
    """
    Extract values from the json that we are interested in 

    :param json: <dict>
    :param unwanted: <list>
    """
    wanted = [i for i in json.keys() if i not in unwanted] 
    out = dict((k, json[k]) for k in wanted if k in json)
    return out
