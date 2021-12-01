#  AUTO-GENERATED FILE - MODIFY AT OWN RISK
#  Project: qcware
#  Copyright (c) 2019 QC Ware Corp - All Rights Reserved

import numpy

import quasar

from typing import Union, Optional, Tuple

import warnings
from qcware.forge.api_calls import declare_api_call


@declare_api_call(name="qutils.qdist", endpoint="qutils/qdist")
def qdist(
    x: Union[float, numpy.ndarray],
    y: Union[float, numpy.ndarray],
    loader_mode: str = "parallel",
    circuit: quasar.Circuit = None,
    backend: str = "qcware/cpu_simulator",
    num_measurements: int = 1000,
    absolute: bool = False,
    opt_shape: Optional[Tuple[int, ...]] = None,
):
    r"""Outputs the distance between input vectors; quantum analogue of::
      numpy.linalg.norm(X - Y)**2

    Cases (following numpy.dot):
      x is 1d, y is 1d; performs vector - vector multiplication. Returns float.
      x is 2d, y is 1d; performs matrix - vector multiplication. Returns 1d array.
      x is 1d, y is 2d; performs vector - matrix multiplication. Returns 1d array.
      x is 2d, y is 2d; performs matrix - matrix multiplication. Returns 2d array.

    Arguments:

    :param x: 1d or 2d array
    :type x: Union[float, numpy.ndarray]

    :param y: 1d or 2d array
    :type y: Union[float, numpy.ndarray]

    :param loader_mode: Type of loader to use, one of parallel, diagonal, semi-diagonal, or optimized, defaults to parallel
    :type loader_mode: str

    :param circuit: Circuit to use for evaluation (None to implicitly create circuit), defaults to None
    :type circuit: quasar.Circuit

    :param backend: String denoting the backend to use, defaults to qcware/cpu_simulator
    :type backend: str

    :param num_measurements: Number of measurements; required, defaults to 1000
    :type num_measurements: int

    :param absolute: Whether to return the absolute value of the result, defaults to False
    :type absolute: bool

    :param opt_shape: shape of the optimized loader's input (N1, N2), defaults to None
    :type opt_shape: Optional[Tuple[int,...]]


    :return: float, 1d array, or 2d array: distance estimation
    :rtype: Union[float, numpy.ndarray]"""
    pass
