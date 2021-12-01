#  AUTO-GENERATED FILE - MODIFY AT OWN RISK
#  Project: qcware
#  Copyright (c) 2019 QC Ware Corp - All Rights Reserved

import numpy

import quasar

from typing import Sequence, Tuple

import warnings
from ...api_calls import declare_api_call


@declare_api_call(name="qutils.run_nisqAE_unary", endpoint="qutils/run_nisqAE_unary")
def run_nisqAE_unary(
    circuit: quasar.Circuit,
    schedule: Sequence[Tuple[int, int]],
    backend: str = "qcware/cpu_simulator",
):
    r"""Performs amplitude estimation routine for unary circuits, assuming the 0th qubit is the target and the target state is |1>, that is, we assume that the state of our system can be written as cos(theta)|0>|badStates> + sin(theta)|1>|0> where badStates is a set of unary states (i.e ones which only one qubit at a time is at state 1) and we're trying to estimate theta.

    Arguments:

    :param circuit: The oracle circuit whose output we would like to estimate
    :type circuit: quasar.Circuit

    :param schedule: A schedule for how many times to run the iteration_circuit, and how many shots to take. A List[Tuple[power, num_shots]], where:
      - power is the number of times to run the iteration circuit
      - num_shots is the number of shots to run at the given power
    :type schedule: Sequence[Tuple[int, int]]

    :param backend: String denoting the backend to use, defaults to qcware/cpu_simulator
    :type backend: str


    :return: For each element in the schedule, returns a tuple of (element, target_counts), where target_counts is the number of measurements whose outcome is in the set of targetStates.
    :rtype: Sequence[Tuple[Tuple[int, int], int]]"""
    pass
