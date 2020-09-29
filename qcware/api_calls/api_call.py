from typing import Optional, Dict
from urllib.parse import urljoin
import backoff
from ..request import post
from ..exceptions import ApiCallExecutionError, ApiTimeoutError
from ..util.transforms import client_result_from_wire
from ..config import (qcware_api_key, qcware_host, client_timeout,
                      server_timeout, do_client_api_compatibility_check_once,
                      current_context, ApiCallContext)
import logging


def post_call(endpoint: str, data: dict):
    """
    Centralizes the post for the API call.  Assumes the data dict
    contains an entry with key 'api_key'; if this is missing or set to
    the default of None, uses the configured API key and augments
    the data dictionary with whatever key is configured.
    """
    api_call_context = data.get('api_call_context', None)
    if api_call_context is None:
        api_call_context = current_context()
    host = api_call_context.qcware_host
    # replace the ApiCallContext class with a jsonable dict
    data['api_call_context'] = api_call_context.dict()
    url = urljoin(host, endpoint)
    return post(url, data)


def api_call(api_call_context: ApiCallContext, call_token: str):
    api_call_context = current_context(
    ) if api_call_context is None else api_call_context
    api_call_context = api_call_context.dict()
    do_client_api_compatibility_check_once()
    return post(f'{api_call_context["qcware_host"]}/api_calls', locals())


def _print_waiting_handler(details: Dict):
    pass


# we pass the function max_poll_period for max_time rather than
# evaluating it; see backoff docs
@backoff.on_predicate(backoff.constant,
                      interval=1,
                      predicate=lambda a: a.get('state') == 'open',
                      max_time=client_timeout,
                      on_backoff=_print_waiting_handler)
def wait_for_call(call_token: str, api_call_context=None):
    api_call_context = current_context(
    ) if api_call_context is None else api_call_context
    # backoff.on_predicate is mildly problematic.
    return api_call(api_call_context, call_token)


def handle_result(api_call):
    if api_call['state'] == 'error':
        raise ApiCallExecutionError(api_call['result']['error'],
                                    traceback=api_call.get('data', {}).get(
                                        'stack_trace', 'no traceback'))
    # if we've got to this point, we either have a result (state == 'success') or we have
    # some other result (state == error, open, new).  If that's the case, we've likely
    # timed out
    if api_call['state'] in ['error', 'open', 'new']:

        api_call_info = {
            k: api_call.get(k, None)
            for k in ['method', 'time_created', 'state', 'uid']
        }
        raise ApiTimeoutError(
            f"Api call timed out; can retrieve with qcware.api_calls.retrieve_result(call_token=\"{api_call_info['uid']}\")",
            api_call_info)
    else:
        return client_result_from_wire(api_call['method'], api_call['result'])


def retrieve_result(call_token: str, api_call_context: ApiCallContext = None):
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
    api_call_context = current_context(
    ) if api_call_context is None else api_call_context
    call = api_call(api_call_context, call_token=call_token)
    return handle_result(call)
