import ast
import json
import pickle
import requests
from . import param_utils


def pickle_json(json_object):
    if isinstance(json_object, dict):
        r = {}
        for k, v in json_object.items():
            if k != 'Q':
                r[k] = pickle_json(v)
            else:
                r['Q'] = pickle.dumps(v, protocol=0)
        return r
    elif isinstance(json_object, list):
        return [pickle_json(elem) for elem in json_object]
    else:
        return pickle.dumps(json_object, protocol=0)


def post(api_endpoint_url, param_dictionary, endpoint_type):
    pbuffed_params = param_utils.convert(param_dictionary, endpoint_type)
    r = requests.post(api_endpoint_url,
                      data=pbuffed_params.SerializeToString())

    r = json.loads(r.text)
    if r.get('solution') and endpoint_type == 'solve_binary':
        r['solution'] = ast.literal_eval(r['solution'])

    return r

def post_json(endpoint_url, param_dictionary):
    # just a straightforward no-frills JSON call to an endpoint without
    # any checking, for illustrative purposes
    data = json.dumps(param_dictionary)
    response = requests.post(endpoint_url, data=data)
    result = json.loads(response.text)
    return result
