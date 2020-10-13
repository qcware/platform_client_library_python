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


def submit_echo(text: str = 'hello world.') -> str:
    r"""

Arguments:

:param text: The text to return, defaults to hello world.
:type text: str


:return: An API call UID string
:rtype: str
    """
    data = client_args_to_wire('test.echo', **locals())
    api_call = post_call('test/echo', data)
    return api_call['uid']


def echo(text: str = 'hello world.'):
    r"""

Arguments:

:param text: The text to return, defaults to hello world.
:type text: str


:return: 
:rtype: 
    """
    data = client_args_to_wire('test.echo', **locals())
    api_call = post_call('test/echo', data)
    api_call_id = api_call['uid']
    logger.info(
        f'API call to test.echo successful. Your API token is {api_call_id}')
    if client_timeout() == 0:
        raise ApiTimeoutError(
            f"Api call timed out; can retrieve with qcware.api_calls.retrieve_result(call_token=\"{api_call_id}\")",
            api_call)
    else:
        return handle_result(wait_for_call(call_token=api_call_id))


async def async_echo(text: str = 'hello world.'):
    r"""Async version of echo



Arguments:

:param text: The text to return, defaults to hello world.
:type text: str


:return: 
:rtype: 
    """
    data = client_args_to_wire('test.echo', **locals())
    api_call = post_call('test/echo', data)
    logger.info(
        f'API call to test.echo successful. Your API token is {api_call["uid"]}'
    )

    return await async_retrieve_result(api_call["uid"])
