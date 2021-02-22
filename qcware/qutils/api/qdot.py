#  AUTO-GENERATED FILE - MODIFY AT OWN RISK
#  Project: qcware
#  Copyright (c) 2019 QC Ware Corp - All Rights Reserved

import numpy

import quasar

from typing import Union

import asyncio
from ... import logger
from ...api_calls import post_call, wait_for_call, handle_result, async_post_call, async_retrieve_result
from ...util.transforms import client_args_to_wire
from ...exceptions import ApiTimeoutError
from ...config import (ApiCallContext, client_timeout,
                       async_interval_between_tries)


def submit_qdot(x: Union[float, numpy.ndarray],
                y: Union[float, numpy.ndarray],
                circuit: quasar.Circuit = None,
                loader_mode: str = 'parallel',
                circuit_mode: str = 'sequential',
                backend: str = 'qcware/cpu_simulator',
                num_measurements: int = None) -> str:
    r"""Outputs the dot product of two arrays; quantum analogue of::
  numpy.dot
  
Cases (following numpy.dot):
  x is 1d, y is 1d; performs vector - vector multiplication. Returns float.
  x is 2d, y is 1d; performs matrix - vector multiplication. Returns 1d array.
  x is 1d, y is 2d; performs vector - matrix multiplication. Returns 1d array.
  x is 2d, y is 2d; performs matrix - matrix multiplication. Returns 2d array.
  

Arguments:

:param x: 1d or 2d array
:type x: Union[float, numpy.ndarray]

:param y: 1d or 2d array
:type y: Union[float, numpy.ndarray]

:param circuit: Circuit to use for evaluation (None to implicitly create circuit), defaults to None
:type circuit: quasar.Circuit

:param loader_mode: , defaults to parallel
:type loader_mode: str

:param circuit_mode: , defaults to sequential
:type circuit_mode: str

:param backend: , defaults to qcware/cpu_simulator
:type backend: str

:param num_measurements: , defaults to None
:type num_measurements: int


:return: An API call UID string
:rtype: str
    """
    data = client_args_to_wire('qutils.qdot', **locals())
    api_call = post_call('qutils/qdot', data)
    return api_call['uid']


def qdot(x: Union[float, numpy.ndarray],
         y: Union[float, numpy.ndarray],
         circuit: quasar.Circuit = None,
         loader_mode: str = 'parallel',
         circuit_mode: str = 'sequential',
         backend: str = 'qcware/cpu_simulator',
         num_measurements: int = None):
    r"""Outputs the dot product of two arrays; quantum analogue of::
  numpy.dot
  
Cases (following numpy.dot):
  x is 1d, y is 1d; performs vector - vector multiplication. Returns float.
  x is 2d, y is 1d; performs matrix - vector multiplication. Returns 1d array.
  x is 1d, y is 2d; performs vector - matrix multiplication. Returns 1d array.
  x is 2d, y is 2d; performs matrix - matrix multiplication. Returns 2d array.
  

Arguments:

:param x: 1d or 2d array
:type x: Union[float, numpy.ndarray]

:param y: 1d or 2d array
:type y: Union[float, numpy.ndarray]

:param circuit: Circuit to use for evaluation (None to implicitly create circuit), defaults to None
:type circuit: quasar.Circuit

:param loader_mode: , defaults to parallel
:type loader_mode: str

:param circuit_mode: , defaults to sequential
:type circuit_mode: str

:param backend: , defaults to qcware/cpu_simulator
:type backend: str

:param num_measurements: , defaults to None
:type num_measurements: int


:return: float, 1d array, or 2d array: dot product
:rtype: Union[float, numpy.ndarray]
    """
    data = client_args_to_wire('qutils.qdot', **locals())
    api_call = post_call('qutils/qdot', data)
    api_call_id = api_call['uid']
    logger.info(
        f'API call to qutils.qdot successful. Your API token is {api_call_id}')
    if client_timeout() == 0:
        raise ApiTimeoutError(
            f"Api call timed out; can retrieve with qcware.api_calls.retrieve_result(call_token=\"{api_call_id}\")",
            api_call)
    else:
        return handle_result(wait_for_call(call_token=api_call_id))


async def async_qdot(x: Union[float, numpy.ndarray],
                     y: Union[float, numpy.ndarray],
                     circuit: quasar.Circuit = None,
                     loader_mode: str = 'parallel',
                     circuit_mode: str = 'sequential',
                     backend: str = 'qcware/cpu_simulator',
                     num_measurements: int = None):
    r"""Async version of qdot
Outputs the dot product of two arrays; quantum analogue of::
  numpy.dot
  
Cases (following numpy.dot):
  x is 1d, y is 1d; performs vector - vector multiplication. Returns float.
  x is 2d, y is 1d; performs matrix - vector multiplication. Returns 1d array.
  x is 1d, y is 2d; performs vector - matrix multiplication. Returns 1d array.
  x is 2d, y is 2d; performs matrix - matrix multiplication. Returns 2d array.
  


Arguments:

:param x: 1d or 2d array
:type x: Union[float, numpy.ndarray]

:param y: 1d or 2d array
:type y: Union[float, numpy.ndarray]

:param circuit: Circuit to use for evaluation (None to implicitly create circuit), defaults to None
:type circuit: quasar.Circuit

:param loader_mode: , defaults to parallel
:type loader_mode: str

:param circuit_mode: , defaults to sequential
:type circuit_mode: str

:param backend: , defaults to qcware/cpu_simulator
:type backend: str

:param num_measurements: , defaults to None
:type num_measurements: int


:return: float, 1d array, or 2d array: dot product
:rtype: Union[float, numpy.ndarray]
    """
    data = client_args_to_wire('qutils.qdot', **locals())
    api_call = await async_post_call('qutils/qdot', data)
    logger.info(
        f'API call to qutils.qdot successful. Your API token is {api_call["uid"]}'
    )

    return await async_retrieve_result(api_call["uid"])
