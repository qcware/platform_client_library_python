from typing import Optional
from urllib.parse import urljoin
import backoff
from ..request import post
from ..exceptions import ApiCallExecutionError
from ..util.transforms import client_result_from_wire
from ..config import qcware_api_key, qcware_host


def post_call(endpoint: str, data: dict, host: Optional[str] = None):
    """
    Centralizes the post for the API call.  Assumes the data dict
    contains an entry with key 'api_key'; if this is missing or set to
    the default of None, uses the configured API key and augments
    the data dictionary with whatever key is configured.
    """
    host = qcware_host(host)
    api_key = qcware_api_key(data.get('api_key', None))
    data['api_key'] = api_key
    url = urljoin(host, endpoint)
    return post(url, data)


def api_call(api_key: Optional[str] = None,
             host: Optional[str] = None,
             call_token=None):
    api_key = qcware_api_key(api_key)
    host = qcware_host(host)
    return post(f'{host}/api_calls', locals())


@backoff.on_predicate(backoff.expo,
                      lambda a: a.get('state') == 'open',
                      max_time=200)
def wait_for_call(api_key=None, host=None, call_token=None):
    return api_call(api_key=api_key, host=host, call_token=call_token)


def handle_result(api_call):
    if api_call['state'] == 'error':
        raise ApiCallExecutionError(api_call['result']['error'])
    return client_result_from_wire(api_call['method'], api_call['result'])
