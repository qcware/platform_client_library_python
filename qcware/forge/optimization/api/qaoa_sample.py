#  AUTO-GENERATED FILE - MODIFY AT OWN RISK
#  Project: qcware
#  Copyright (c) 2019 QC Ware Corp - All Rights Reserved

from qcware.types.optimization import BinaryProblem, BinaryResults

import numpy

import warnings
from qcware.forge.api_calls import declare_api_call


@declare_api_call(name="optimization.qaoa_sample", endpoint="optimization/qaoa_sample")
def qaoa_sample(
    problem_instance: BinaryProblem,
    beta: numpy.ndarray,
    gamma: numpy.ndarray,
    num_samples: int,
    backend: str = "qcware/cpu",
):
    r"""Build a QAOA circuit for given (objective, angles) and sample.
    This function sets up the conventional quantum state for the quantum approximate optimization algorithm (QAOA) based on the objective function in the BinaryProblem `problem_instance`. That state is then samples and a histogram of results is returned.
    Because this is conventional QAOA, `problem_instance` must be unconstrained: the user can add terms to their objective function to account for constraints.

    Arguments:

    :param problem_instance: Unconstrained BinaryProblem instance specifying the objective function.
    :type problem_instance: BinaryProblem

    :param beta: NumPy array with shape (p,) giving beta angles as typically defined in the QAOA).
    :type beta: numpy.ndarray

    :param gamma: NumPy array with shape (p,) giving gamma angles as typically defined in the QAOA).
    :type gamma: numpy.ndarray

    :param num_samples: The number of samples to take from the QAOA state.
    :type num_samples: int

    :param backend: String specifying the backend.  Currently only [qcware/cpu] available, defaults to qcware/cpu
    :type backend: str


    :return: BinaryResults providing a histogram of bit samples.
    :rtype: BinaryResults"""
    pass
