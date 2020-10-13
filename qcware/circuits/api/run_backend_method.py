#  AUTO-GENERATED FILE - MODIFY AT OWN RISK
#  Project: qcware
#  Copyright (c) 2019 QC Ware Corp - All Rights Reserved

import asyncio
from ... import logger
from ...api_calls import post_call, wait_for_call, handle_result, async_retrieve_result
from ...util.transforms import client_args_to_wire
from ...exceptions import ApiTimeoutError
from ...config import (ApiCallContext, client_timeout,
                       async_interval_between_tries)


def submit_run_backend_method(backend: str, method: str, kwargs: dict) -> str:
    r"""Runs an arbitrary backend method.  This API call is not intended to be used directly by users; rather, it is meant to be called by the QuasarBackend class to transparently delegate class method calls to Forge API endpoints.

Arguments:

:param backend: string representing the backend
:type backend: str

:param method: name of the method to be called
:type method: str

:param kwargs: Keyword args passed to the method.  Positional args should be converted to kwargs
:type kwargs: dict


:return: An API call UID string
:rtype: str
    """
    data = client_args_to_wire('circuits.run_backend_method', **locals())
    api_call = post_call('circuits/run_backend_method', data)
    return api_call['uid']


def run_backend_method(backend: str, method: str, kwargs: dict):
    r"""Runs an arbitrary backend method.  This API call is not intended to be used directly by users; rather, it is meant to be called by the QuasarBackend class to transparently delegate class method calls to Forge API endpoints.

Arguments:

:param backend: string representing the backend
:type backend: str

:param method: name of the method to be called
:type method: str

:param kwargs: Keyword args passed to the method.  Positional args should be converted to kwargs
:type kwargs: dict


:return: variable; see Quasar documentation
:rtype: object
    """
    data = client_args_to_wire('circuits.run_backend_method', **locals())
    api_call = post_call('circuits/run_backend_method', data)
    api_call_id = api_call['uid']
    logger.info(
        f'API call to circuits.run_backend_method successful. Your API token is {api_call_id}'
    )
    if client_timeout() == 0:
        raise ApiTimeoutError(
            f"Api call timed out; can retrieve with qcware.api_calls.retrieve_result(call_token=\"{api_call_id}\")",
            api_call)
    else:
        return handle_result(wait_for_call(call_token=api_call_id))


async def async_run_backend_method(backend: str, method: str, kwargs: dict):
    r"""Async version of run_backend_method
Runs an arbitrary backend method.  This API call is not intended to be used directly by users; rather, it is meant to be called by the QuasarBackend class to transparently delegate class method calls to Forge API endpoints.


Arguments:

:param backend: string representing the backend
:type backend: str

:param method: name of the method to be called
:type method: str

:param kwargs: Keyword args passed to the method.  Positional args should be converted to kwargs
:type kwargs: dict


:return: variable; see Quasar documentation
:rtype: object
    """
    data = client_args_to_wire('circuits.run_backend_method', **locals())
    api_call = post_call('circuits/run_backend_method', data)
    logger.info(
        f'API call to circuits.run_backend_method successful. Your API token is {api_call["uid"]}'
    )

    return await async_retrieve_result(api_call["uid"])
