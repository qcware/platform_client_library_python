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


def submit_find_optimal_qaoa_angles(Q: dict = {},
                                    num_evals: int = 100,
                                    num_min_vals: int = 10,
                                    fastmath_flag_in: bool = True,
                                    precision: int = 30) -> str:
    r"""Finds the optimal expectation values for a given cost function, to be used in QAOA.

Arguments:

:param Q: The objective function matrix.  As :math:`Q` is usually sparse, it should be specified as a Python dictionary with integer pairs :math:`(i,j)` as keys (representing the :math:`(i,j)`th entry of :math:`Q`) and integer or float values., defaults to {}
:type Q: dict

:param num_evals: The number of evaluations used for :math:`\beta`/:math:`\gamma`, defaults to 100
:type num_evals: int

:param num_min_vals: The number of returned minima, defaults to 10
:type num_min_vals: int

:param fastmath_flag_in: The "fastmath" flag in Numba, defaults to True
:type fastmath_flag_in: bool

:param precision: Inverse proportional to the minimum distance between peaks (nx/precision), defaults to 30
:type precision: int


:return: An API call UID string
:rtype: str
    """
    data = client_args_to_wire('optimization.find_optimal_qaoa_angles',
                               **locals())
    api_call = post_call('optimization/find_optimal_qaoa_angles', data)
    return api_call['uid']


def find_optimal_qaoa_angles(Q: dict = {},
                             num_evals: int = 100,
                             num_min_vals: int = 10,
                             fastmath_flag_in: bool = True,
                             precision: int = 30):
    r"""Finds the optimal expectation values for a given cost function, to be used in QAOA.

Arguments:

:param Q: The objective function matrix.  As :math:`Q` is usually sparse, it should be specified as a Python dictionary with integer pairs :math:`(i,j)` as keys (representing the :math:`(i,j)`th entry of :math:`Q`) and integer or float values., defaults to {}
:type Q: dict

:param num_evals: The number of evaluations used for :math:`\beta`/:math:`\gamma`, defaults to 100
:type num_evals: int

:param num_min_vals: The number of returned minima, defaults to 10
:type num_min_vals: int

:param fastmath_flag_in: The "fastmath" flag in Numba, defaults to True
:type fastmath_flag_in: bool

:param precision: Inverse proportional to the minimum distance between peaks (nx/precision), defaults to 30
:type precision: int


:return: A tuple of three values min_val, min_beta_gamma, Z where:
  
* min_val is a list of the best `num_min_vals` expectation values found, sorted from minimum to maximum.
* min_beta_gamma is a list of [:math:`\beta`, :math:`\gamma`] pairs representing the best
  `num_min_vals` expectation values found, in the same order as the expectation values


* Z is a numpy.ndarray of shape (num_evals, num_evals) representing the expectation value for
  the beta/gamma pair.  Each row represents a choice of :math:`\gamma` and each column represents
  a choice of :math:`\beta`, so `Z[1,2]` represents the expectation value from the :math:`\gamma` value `Y[1]`
  and the :math:`\beta` value `X[2]`
  
:rtype: tuple
    """
    data = client_args_to_wire('optimization.find_optimal_qaoa_angles',
                               **locals())
    api_call = post_call('optimization/find_optimal_qaoa_angles', data)
    api_call_id = api_call['uid']
    logger.info(
        f'API call to optimization.find_optimal_qaoa_angles successful. Your API token is {api_call_id}'
    )
    if client_timeout() == 0:
        raise ApiTimeoutError(
            f"Api call timed out; can retrieve with qcware.api_calls.retrieve_result(call_token=\"{api_call_id}\")",
            api_call)
    else:
        return handle_result(wait_for_call(call_token=api_call_id))


async def async_find_optimal_qaoa_angles(Q: dict = {},
                                         num_evals: int = 100,
                                         num_min_vals: int = 10,
                                         fastmath_flag_in: bool = True,
                                         precision: int = 30):
    r"""Async version of find_optimal_qaoa_angles
Finds the optimal expectation values for a given cost function, to be used in QAOA.


Arguments:

:param Q: The objective function matrix.  As :math:`Q` is usually sparse, it should be specified as a Python dictionary with integer pairs :math:`(i,j)` as keys (representing the :math:`(i,j)`th entry of :math:`Q`) and integer or float values., defaults to {}
:type Q: dict

:param num_evals: The number of evaluations used for :math:`\beta`/:math:`\gamma`, defaults to 100
:type num_evals: int

:param num_min_vals: The number of returned minima, defaults to 10
:type num_min_vals: int

:param fastmath_flag_in: The "fastmath" flag in Numba, defaults to True
:type fastmath_flag_in: bool

:param precision: Inverse proportional to the minimum distance between peaks (nx/precision), defaults to 30
:type precision: int


:return: A tuple of three values min_val, min_beta_gamma, Z where:
  
* min_val is a list of the best `num_min_vals` expectation values found, sorted from minimum to maximum.
* min_beta_gamma is a list of [:math:`\beta`, :math:`\gamma`] pairs representing the best
  `num_min_vals` expectation values found, in the same order as the expectation values


* Z is a numpy.ndarray of shape (num_evals, num_evals) representing the expectation value for
  the beta/gamma pair.  Each row represents a choice of :math:`\gamma` and each column represents
  a choice of :math:`\beta`, so `Z[1,2]` represents the expectation value from the :math:`\gamma` value `Y[1]`
  and the :math:`\beta` value `X[2]`
  
:rtype: tuple
    """
    data = client_args_to_wire('optimization.find_optimal_qaoa_angles',
                               **locals())
    api_call = post_call('optimization/find_optimal_qaoa_angles', data)
    logger.info(
        f'API call to optimization.find_optimal_qaoa_angles successful. Your API token is {api_call["uid"]}'
    )

    return await async_retrieve_result(api_call["uid"])
