#  AUTO-GENERATED FILE - MODIFY AT OWN RISK
#  Project: qcware
#  Copyright (c) 2019 QC Ware Corp - All Rights Reserved

import numpy

import quasar

from typing import Optional, Sequence, Tuple

import warnings
from ...api_calls import declare_api_call


@declare_api_call(
    name="qutils.make_nisqAE_schedule", endpoint="qutils/make_nisqAE_schedule"
)
def make_nisqAE_schedule(
    epsilon: float,
    schedule_type: str,
    max_depth: Optional[int] = 20,
    beta: Optional[float] = 0.5,
    n_shots: Optional[float] = 20,
):
    r"""Create a schedule for use in the run_nisqAE functions.

    Arguments:

    :param epsilon: The additive bound with which to approximate the amplitude
    :type epsilon: float

    :param schedule_type: schedule_type in 'linear', 'exponential', 'powerlaw', 'classical'
    :type schedule_type: str

    :param max_depth: The maximum number of times we should run the iteration circuit (does not affect 'powerlaw')., defaults to 20
    :type max_depth: Optional[int]

    :param beta: Beta parameter for powerlaw schedule (does not affect other schedule_types)., defaults to 0.5
    :type beta: Optional[float]

    :param n_shots: Number of measurements to take at each power, defaults to 20
    :type n_shots: Optional[float]


    :return: A schedule for how many times to run the iteration_circuit, and how many shots to take. A List[Tuple[power, num_shots]], where:
      - power is the number of times to run the iteration circuit
      - num_shots is the number of shots to run at the given power
    :rtype: Sequence[Tuple[int, int]]"""
    pass
