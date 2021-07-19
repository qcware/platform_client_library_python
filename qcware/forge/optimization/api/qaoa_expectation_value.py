#  AUTO-GENERATED FILE - MODIFY AT OWN RISK
#  Project: qcware
#  Copyright (c) 2019 QC Ware Corp - All Rights Reserved

from qcware.types.optimization import BinaryProblem, BinaryResults

import numpy

from typing import Optional

import warnings
from ...api_calls import declare_api_call


@declare_api_call(
    name="optimization.qaoa_expectation_value",
    endpoint="optimization/qaoa_expectation_value",
)
def qaoa_expectation_value(
    problem_instance: BinaryProblem,
    beta: numpy.ndarray,
    gamma: numpy.ndarray,
    num_samples: Optional[int] = None,
    backend: str = "qcware/cpu",
):
    r"""Get the QAOA expectation value for a BinaryProblem instance.
    This function sets up the conventional quantum state for the quantum approximate optimization algorithm (QAOA) based on the objective function in the BinaryProblem `problem_instance`.
    Because this is conventional QAOA, `problem_instance` must be unconstrained: the user can add terms to their objective function to account for constraints.
    This function can be used in a QAOA workflow to optimize or study angles.

    Arguments:

    :param problem_instance: Unconstrained BinaryProblem instance specifying the objective function.
    :type problem_instance: BinaryProblem

    :param beta: NumPy array with shape (p,) giving beta angles as typically defined in the QAOA).
    :type beta: numpy.ndarray

    :param gamma: NumPy array with shape (p,) giving gamma angles as typically defined in the QAOA).
    :type gamma: numpy.ndarray

    :param num_samples: The number of measurements to use to estimate expectation value. When set to None (the default value), simulation is used (if the backend allows it) to get an exact expectation value. This can be much faster than using samples., defaults to None
    :type num_samples: Optional[int]

    :param backend: String specifying the backend.  Currently only [qcware/cpu] available, defaults to qcware/cpu
    :type backend: str


    :return: The expectation value for the QAOA state.
    :rtype: float"""
    pass


def submit_qaoa_expectation_value(*args, **kwargs):
    """This method is deprecated; please use qaoa_expectation_value.submit"""
    w = "The old submit_qaoa_expectation_value function has been deprecated and will be removed.  Please use qaoa_expectation_value.submit"
    warnings.warn(w, DeprecationWarning)
    print(w)
    return qaoa_expectation_value.submit(*args, **kwargs)


async def async_qaoa_expectation_value(*args, **kwargs):
    """This method is deprecated; please use qaoa_expectation_value.call_async"""
    w = "The old async_qaoa_expectation_value function has been deprecated and will be removed.  Please use qaoa_expectation_value.call_async"
    warnings.warn(w, DeprecationWarning)
    print(w)
    return await qaoa_expectation_value.call_async(*args, **kwargs)
