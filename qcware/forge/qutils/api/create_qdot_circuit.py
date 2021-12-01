#  AUTO-GENERATED FILE - MODIFY AT OWN RISK
#  Project: qcware
#  Copyright (c) 2019 QC Ware Corp - All Rights Reserved

import numpy

import warnings
from qcware.forge.api_calls import declare_api_call


@declare_api_call(
    name="qutils.create_qdot_circuit", endpoint="qutils/create_qdot_circuit"
)
def create_qdot_circuit(
    x: numpy.ndarray,
    y: numpy.ndarray,
    loader_mode: str = "parallel",
    absolute: bool = False,
):
    r"""Creates a circuit which, when run, outputs the dot product of two 1d arrays; quantum analogue of::
      numpy.dot

    Arguments:

    :param x: 1d array
    :type x: numpy.ndarray

    :param y: 1d array
    :type y: numpy.ndarray

    :param loader_mode: Type of loader to use, one of parallel, diagonal, semi-diagonal, or optimized, defaults to parallel
    :type loader_mode: str

    :param absolute: Whether to return the absolute value of output, defaults to False
    :type absolute: bool


    :return: A Quasar circuit suitable for execution on any quasar backend supporting the required gates which returns the dot product.
    :rtype: quasar.Circuit"""
    pass
