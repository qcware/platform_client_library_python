#  AUTO-GENERATED FILE - MODIFY AT OWN RISK
#  Project: qcware
#  Copyright (c) 2019 QC Ware Corp - All Rights Reserved

import numpy

from typing import Optional, Tuple

import warnings
from ...api_calls import declare_api_call


@declare_api_call(name="qio.loader", endpoint="qio/loader")
def loader(
    data: numpy.ndarray,
    mode: str = "optimized",
    opt_shape: Optional[Tuple[int, ...]] = None,
    initial: bool = True,
):
    r"""Creates a circuit which loads an array of classical data into the state space of a quantum computer or simulator.  This is useful in order to act on known data or to simulator quantum RAM.

    Arguments:

    :param data: A 1-d array representing the classical data to be represented in the circuit
    :type data: numpy.ndarray

    :param mode: Whether to used the "optimized" loader (using approximately :math:`~sqrt(d)` depth and :math:`~sqrt(d)` qubits) or the "parallel" loader (using approximately :math:`log(d)` depth and `d` qubits., defaults to optimized
    :type mode: str

    :param opt_shape: If the loader is an optimized loader, this corresponds to the new shape of the input matrix, defaults to None
    :type opt_shape: Optional[Tuple[int,...]]

    :param initial: Whether the loader is at the beginning of the circuit (in which it performs an initial X gate on the first qubit), defaults to True
    :type initial: bool


    :return: A Quasar circuit suitable for execution on any quasar backend supporting the required gates which loads the classical vector into a quantum state.
    :rtype: quasar.Circuit"""
    pass
