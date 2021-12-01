#  AUTO-GENERATED FILE - MODIFY AT OWN RISK
#  Project: qcware
#  Copyright (c) 2019 QC Ware Corp - All Rights Reserved

import numpy

import quasar

from typing import Sequence, Tuple

import warnings
from qcware.forge.api_calls import declare_api_call


@declare_api_call(
    name="montecarlo.nisqAE.compute_mle", endpoint="montecarlo.nisqAE/compute_mle"
)
def compute_mle(target_counts: Sequence[Tuple[Tuple[int, int], int]], epsilon: float):
    r"""Given the output of the run_nisqAE functions and estimates the parameter theta via MLE.

    Arguments:

    :param target_counts: For each element in the schedule, returns a tuple of (element, target_counts), where target_counts is the number of measurements whose outcome is in the set of targetStates.
    :type target_counts: Sequence[Tuple[Tuple[int, int], int]]

    :param epsilon: The additive error within which we would like to calculate theta.
    :type epsilon: float


    :return: MLE estimate of theta.
    :rtype: float"""
    pass
