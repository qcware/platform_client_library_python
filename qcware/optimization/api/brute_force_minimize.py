#  AUTO-GENERATED FILE - MODIFY AT OWN RISK
#  Project: qcware
#  Copyright (c) 2019 QC Ware Corp - All Rights Reserved

import qcware.types.optimization as types

from typing import Optional

import asyncio
from ... import logger
from ...api_calls import post_call, wait_for_call, handle_result, async_post_call, async_retrieve_result
from ...util.transforms import client_args_to_wire
from ...exceptions import ApiTimeoutError
from ...config import (ApiCallContext, client_timeout,
                       async_interval_between_tries)


def submit_brute_force_minimize(objective: types.PolynomialObjective,
                                constraints: Optional[
                                    types.Constraints] = None,
                                backend: str = 'qcware/cpu') -> str:
    r"""Minimize given objective polynomial subject to constraints.

Arguments:

:param objective: The integer-coefficient polynomial to be evaluated should be specified by a PolynomialObjective. See documentation for PolynomialObjective for more information. Note that variables are boolean in the sense that their values are 0 and 1.
:type objective: types.PolynomialObjective

:param constraints: Optional constraints are specified with an object of class Constraints. See its documentation for further information., defaults to None
:type constraints: Optional[types.Constraints]

:param backend: String specifying the backend.  Currently only [qcware/cpu] available, defaults to qcware/cpu
:type backend: str


:return: An API call UID string
:rtype: str
    """
    data = client_args_to_wire('optimization.brute_force_minimize', **locals())
    api_call = post_call('optimization/brute_force_minimize', data)
    return api_call['uid']


def brute_force_minimize(objective: types.PolynomialObjective,
                         constraints: Optional[types.Constraints] = None,
                         backend: str = 'qcware/cpu'):
    r"""Minimize given objective polynomial subject to constraints.

Arguments:

:param objective: The integer-coefficient polynomial to be evaluated should be specified by a PolynomialObjective. See documentation for PolynomialObjective for more information. Note that variables are boolean in the sense that their values are 0 and 1.
:type objective: types.PolynomialObjective

:param constraints: Optional constraints are specified with an object of class Constraints. See its documentation for further information., defaults to None
:type constraints: Optional[types.Constraints]

:param backend: String specifying the backend.  Currently only [qcware/cpu] available, defaults to qcware/cpu
:type backend: str


:return: BruteOptimizeResult object specifying the minimum value of the objective function (that does not violate a constraint) as well as the variables that attain this value.
:rtype: types.BruteOptimizeResult
    """
    data = client_args_to_wire('optimization.brute_force_minimize', **locals())
    api_call = post_call('optimization/brute_force_minimize', data)
    api_call_id = api_call['uid']
    logger.info(
        f'API call to optimization.brute_force_minimize successful. Your API token is {api_call_id}'
    )
    if client_timeout() == 0:
        raise ApiTimeoutError(
            f"Api call timed out; can retrieve with qcware.api_calls.retrieve_result(call_token=\"{api_call_id}\")",
            api_call)
    else:
        return handle_result(wait_for_call(call_token=api_call_id))


async def async_brute_force_minimize(
        objective: types.PolynomialObjective,
        constraints: Optional[types.Constraints] = None,
        backend: str = 'qcware/cpu'):
    r"""Async version of brute_force_minimize
Minimize given objective polynomial subject to constraints.


Arguments:

:param objective: The integer-coefficient polynomial to be evaluated should be specified by a PolynomialObjective. See documentation for PolynomialObjective for more information. Note that variables are boolean in the sense that their values are 0 and 1.
:type objective: types.PolynomialObjective

:param constraints: Optional constraints are specified with an object of class Constraints. See its documentation for further information., defaults to None
:type constraints: Optional[types.Constraints]

:param backend: String specifying the backend.  Currently only [qcware/cpu] available, defaults to qcware/cpu
:type backend: str


:return: BruteOptimizeResult object specifying the minimum value of the objective function (that does not violate a constraint) as well as the variables that attain this value.
:rtype: types.BruteOptimizeResult
    """
    data = client_args_to_wire('optimization.brute_force_minimize', **locals())
    api_call = await async_post_call('optimization/brute_force_minimize', data)
    logger.info(
        f'API call to optimization.brute_force_minimize successful. Your API token is {api_call["uid"]}'
    )

    return await async_retrieve_result(api_call["uid"])
