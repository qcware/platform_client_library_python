import ast
import json
import pickle
import requests
import aiohttp

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


async def async_post(client, api_endpoint_url, param_dictionary, endpoint_type):
    pbuffed_params = param_utils.convert(param_dictionary, endpoint_type)

    async with client.post(
            api_endpoint_url,
            data=pbuffed_params.SerializeToString()) as r:

        print(r.status)
        text = await r.text()
        print(text)

        r = json.loads(text)
        if r.get('solution') and endpoint_type == 'solve_binary':
            r['solution'] = ast.literal_eval(r['solution'])

        return r
