#  AUTO-GENERATED FILE - MODIFY AT OWN RISK
#  Project: qcware
#  Copyright (c) 2019 QC Ware Corp - All Rights Reserved

import numpy

import quasar

from typing import Sequence, Tuple

import warnings
from ...api_calls import declare_api_call


@declare_api_call(
    name="qutils.run_nisqAE_schedule", endpoint="qutils/run_nisqAE_schedule"
)
def run_nisqAE_schedule(
    initial_circuit: quasar.Circuit,
    iteration_circuit: quasar.Circuit,
    target_qubits: Sequence[int],
    target_states: Sequence[int],
    schedule: Sequence[Tuple[int, int]],
    backend: str = "qcware/cpu_simulator",
):
    r"""Run a nisq variant of amplitude estimation and output circuit measurements for each circuit in the given schedule.

    Arguments:

    :param initial_circuit: The oracle circuit whose output we would like to estimate.
    :type initial_circuit: quasar.Circuit

    :param iteration_circuit: The iteration circuit which we will run multiple times according to the schedule.
    :type iteration_circuit: quasar.Circuit

    :param target_qubits: The qubits which will be measured after every shot and compared to the target_states below.
    In the classic amplitude estimation problem, this is usually just [0].
    :type target_qubits: Sequence[int]

    :param target_states: The set of states states [in base-10 integer representation] which correspond to "successful" measurements of the target_qubits. If the target_qubits are measured as one of target_states at the end of a shot, target_counts will be incremented.
    In the classic amplitude estimation problem, this is usually just [1].
    :type target_states: Sequence[int]

    :param schedule: A schedule for how many times to run the iteration_circuit, and how many shots to take. A List[Tuple[power, num_shots]], where:
      - power is the number of times to run the iteration_circuit in a shot
      - num_shots is the number of shots to run at the given power
    :type schedule: Sequence[Tuple[int, int]]

    :param backend: String denoting the backend to use, defaults to qcware/cpu_simulator
    :type backend: str


    :return: For each element in the schedule, returns a tuple of (element, target_counts), where target_counts is the number of measurements whose outcome is in the set of target_states.
    :rtype: Sequence[Tuple[Tuple[int, int], int]]"""
    pass
