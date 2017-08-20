import ast
import json
import pickle
import requests
import param_utils


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


def post(api_endpoint_url, param_dictionary):
    pbuffed_params = param_utils.convert(param_dictionary)
    r = requests.post(api_endpoint_url,
                      data=pbuffed_params.SerializeToString())

    r = json.loads(r.text)
    if r.get('solution'):
        r['solution'] = ast.literal_eval(r['solution'])

    return r
