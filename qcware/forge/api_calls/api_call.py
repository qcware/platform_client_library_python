import asyncio
import json
from typing import Dict
from urllib.parse import urljoin

import backoff
from qcware.forge.async_request import post as async_post
from qcware.forge.config import (
    ApiCallContext,
    async_interval_between_tries,
    client_timeout,
    current_context,
    do_client_api_compatibility_check_once,
)
from qcware.forge.exceptions import ApiCallExecutionError, ApiTimeoutError
from qcware.forge.request import get, post
from qcware.serialization.transforms import (
    client_result_from_wire,
    server_args_from_wire,
)


def post_call(endpoint: str, data: dict):
    api_call_context = data.get("api_call_context", None)
    if api_call_context is None:
        api_call_context = current_context()
    host = api_call_context.qcware_host
    # replace the ApiCallContext class with a jsonable dict
    data["api_call_context"] = api_call_context.dict()
    url = urljoin(host, endpoint)
    return post(url, data)


async def async_post_call(endpoint: str, data: dict):
    """
    Centralizes the post for the API call.  Assumes the data dict
    contains an entry with key 'api_key'; if this is missing or set to
    the default of None, uses the configured API key and augments
    the data dictionary with whatever key is configured.
    """
    api_call_context = data.get("api_call_context", None)
    if api_call_context is None:
        api_call_context = current_context()
    host = api_call_context.qcware_host
    # replace the ApiCallContext class with a jsonable dict
    data["api_call_context"] = api_call_context.dict()
    url = urljoin(host, endpoint)
    return await async_post(url, data)


def api_call(api_call_context: ApiCallContext, call_token: str):
    api_call_context = (
        current_context() if api_call_context is None else api_call_context
    )
    do_client_api_compatibility_check_once()
    return post(
        f"{api_call_context.qcware_host}/api_calls",
        dict(api_call_context=api_call_context.dict(), call_token=call_token),
    )


async def async_api_call(api_call_context: ApiCallContext, call_token: str):
    api_call_context = (
        current_context() if api_call_context is None else api_call_context
    )
    do_client_api_compatibility_check_once()
    return await async_post(
        f"{api_call_context.qcware_host}/api_calls",
        dict(api_call_context=api_call_context.dict(), call_token=call_token),
    )


def status(call_token: str):
    api_call_context = current_context()
    do_client_api_compatibility_check_once()
    return post(
        f"{api_call_context.qcware_host}/api_calls/status",
        dict(api_call_context=api_call_context.dict(), call_token=call_token),
    )


def cancel(call_token: str):
    api_call_context = current_context()
    do_client_api_compatibility_check_once()
    return post(
        f"{api_call_context.qcware_host}/api_calls/cancel",
        dict(api_call_context=api_call_context.dict(), call_token=call_token),
    )


def _print_waiting_handler(details: Dict):
    pass


# we pass the function max_poll_period for max_time rather than
# evaluating it; see backoff docs
@backoff.on_predicate(
    backoff.constant,
    interval=1,
    predicate=lambda a: a.get("state") == "open",
    max_time=client_timeout,
    on_backoff=_print_waiting_handler,
)
def wait_for_call(call_token: str, api_call_context=None):
    api_call_context = (
        current_context() if api_call_context is None else api_call_context
    )
    # backoff.on_predicate is mildly problematic.
    return api_call(api_call_context, call_token)


@backoff.on_predicate(
    backoff.constant,
    interval=1,
    predicate=lambda a: a.get("state") == "open",
    max_time=client_timeout,
    on_backoff=_print_waiting_handler,
)
async def async_wait_for_call(call_token: str, api_call_context=None):
    api_call_context = (
        current_context() if api_call_context is None else api_call_context
    )
    # backoff.on_predicate is mildly problematic.
    return await async_api_call(api_call_context, call_token)


def handle_result(api_call):
    if api_call["state"] == "error":
        if "result_url" in api_call:
            result = json.loads(get(api_call["result_url"]))
        else:
            result = api_call["result"]
        raise ApiCallExecutionError(
            result["error"],
            traceback=api_call.get("data", {}).get("stack_trace", "no traceback"),
        )
    elif api_call["state"] == "scheduled":
        # if it's scheduled, try to raise a nice rescheduled ApiCallExecutionError
        schedule_at_str = api_call.get("schedule_at_str", "unscheduled")
        api_call_info = {
            k: api_call.get(k, None) for k in ["method", "time_created", "state", "uid"]
        }
        raise ApiCallExecutionError(
            f"API Call {api_call.get('uid', 'ERROR')} rescheduled for {schedule_at_str}",
            traceback="",
            api_call_info=api_call_info,
        )
    # if we've got to this point, we either have a result (state == 'success') or we have
    # some other result (state == error, open, new).  If that's the case, we've likely
    # timed out
    if api_call["state"] in ["open", "new"]:

        api_call_info = {
            k: api_call.get(k, None) for k in ["method", "time_created", "state", "uid"]
        }
        raise ApiTimeoutError(api_call_info)
    else:
        if "result_url" in api_call:
            result = json.loads(get(api_call["result_url"]))
        else:
            result = api_call["result"]
        return client_result_from_wire(api_call["method"], result)


def handle_params(params_data):
    method = params_data["method"]
    raw_params = json.loads(get(params_data["params_url"]))
    params = server_args_from_wire(method, **raw_params)
    del params["api_call_context"]
    return params


def retrieve_result(call_token: str, api_call_context: ApiCallContext = None):
    """
    Retrieves the result of a call or an error object if the call is not complete

    :param call_token: The token of the API call; can be
    retrieved from last_x_calls or the web interface
    :type call_token: str

    :param api_call_context: API Call context; default context used if none provided
    :type api_call_context: ApiCallContext

    :return Either the processed result in the type expected, or an error object
    showing the state of the call
    """
    api_call_context = (
        current_context() if api_call_context is None else api_call_context
    )
    call = api_call(api_call_context, call_token=call_token)
    return handle_result(call)


async def async_retrieve_result(
    call_token: str, api_call_context: ApiCallContext = None
):
    """
    Retrieves the result of a call; if the call is incomplete, waits for it to be complete.
    :param call_token: The token of the API call; can be
    retrieved from last_x_calls or the web interface
    :type call_token: str

    :param api_call_context: API Call context; default context used if none provided
    :type api_call_context: ApiCallContext


    :return Either the processed result in the type expected, or an error object
    showing the state of the call
    """
    while True:
        try:
            return handle_result(await async_wait_for_call(call_token))
        except ApiTimeoutError as e:
            await asyncio.sleep(async_interval_between_tries())


def retrieve_parameters(call_token: str, api_call_context: ApiCallContext = None):
    """
    Retrieves the parameters of an API call.
    :param call_token: The token of the API call; can be
    retrieved from last_x_calls or the web interface
    :type call_token: str

    :param api_call_context: API Call context; default context used if none provided
    :type api_call_context: ApiCallContext

    :return: The parameters passed to the API call
    """
    api_call_context = (
        current_context() if api_call_context is None else api_call_context
    )
    return handle_params(
        post(
            f"{api_call_context.qcware_host}/api_calls/params",
            dict(api_call_context=api_call_context.dict(), call_token=call_token),
        )
    )


async def async_retrieve_parameters(
    call_token: str, api_call_context: ApiCallContext = None
):
    """
    Retrieves the parameters of an API call asynchronously.
    :param call_token: The token of the API call; can be
    retrieved from last_x_calls or the web interface
    :type call_token: str

    :param api_call_context: API Call context; default context used if none provided
    :type api_call_context: ApiCallContext

    :return: The parameters passed to the API call
    """
    api_call_context = (
        current_context() if api_call_context is None else api_call_context
    )
    return handle_params(
        await async_post(
            f"{api_call_context.qcware_host}/api_calls/params",
            dict(api_call_context=api_call_context.dict(), call_token=call_token),
        )
    )
