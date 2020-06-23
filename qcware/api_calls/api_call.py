from typing import Optional, Dict
from urllib.parse import urljoin
import backoff
from ..request import post
from ..exceptions import ApiCallExecutionError, ApiTimeoutError
from ..util.transforms import client_result_from_wire
from ..config import qcware_api_key, qcware_host, max_poll_period, do_client_api_compatibility_check_once, max_long_poll
import logging


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
    max_wait_for_closure_in_sec = max_long_poll()
    do_client_api_compatibility_check_once()
    return post(f'{host}/api_calls', locals())


def _print_waiting_handler(details: Dict):
    pass


# we pass the function max_poll_period for max_time rather than
# evaluating it; see backoff docs
@backoff.on_predicate(backoff.constant,
                      interval=1,
                      predicate=lambda a: a.get('state') == 'open',
                      max_time=max_poll_period,
                      on_backoff=_print_waiting_handler)
def wait_for_call(api_key=None, host=None, call_token=None):
    # backoff.on_predicate is mildly problematic.
    return api_call(api_key=api_key, host=host, call_token=call_token)


def handle_result(api_call):
    if api_call['state'] == 'error':
        raise ApiCallExecutionError(api_call['result']['error'],
                                    traceback=api_call.get(
                                        'additional_data',
                                        {}).get('stack_trace', ''))
    api_call_info = {
        k: api_call[k]
        for k in ['method', 'time_created', 'state', 'uid']
    }
    # if we've got to this point, we either have a result (state == 'success') or we have
    # some other result (state == error, open, new).  If that's the case, we've likely
    # timed out
    if api_call['state'] in ['error', 'open', 'new']:
        raise ApiTimeoutError(
            f"Api call timed out; can retrieve with qcware.api_call.retrieve_result(call_token=\"{api_call_info['uid']}\")",
            api_call_info)
    else:
        return client_result_from_wire(api_call['method'], api_call['result'])


def retrieve_result(call_token: str,
                    api_key: Optional[str] = None,
                    host: Optional[str] = None):
    """
    Retrieves the result of a call or an error object if the call is not complete

    :param call_token: The token of the API call; can be 
    retrieved from last_x_calls or the web interface
    :type call_token: str

    :param api_key: API key; by default taken from config
    :type api_key: str

    :param host: Forge host to use; by default taken from config
    :type host: str

    :return Either the processed result in the type expected, or an error object
    showing the state of the call
    """
    api_key = qcware_api_key(api_key)
    host = qcware_host(host)
    call = api_call(api_key=api_key, host=host, call_token=call_token)
    return handle_result(call)
