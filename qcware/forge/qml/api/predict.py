#  AUTO-GENERATED FILE - MODIFY AT OWN RISK
#  Project: qcware
#  Copyright (c) 2019 QC Ware Corp - All Rights Reserved

import numpy

import numpy.typing

from qcware.types.qml import FitData

import warnings
from qcware.forge.api_calls import declare_api_call


@declare_api_call(name="qml.predict", endpoint="qml/predict")
def predict(
    X: numpy.typing.ArrayLike, fit_data: FitData, backend: str = "qcware/cpu_simulator"
):
    r"""Predicts classification labels for fitted data.

    Arguments:

    :param X: Test data: :math:`(M\times d)` array containing test data
    :type X: numpy.typing.ArrayLike

    :param fit_data: A FitData instance representing a previous fitting operation
    :type fit_data: FitData

    :param backend: String describing the backend to use, defaults to qcware/cpu_simulator
    :type backend: str


    :return: A numpy array the length of the test data `X` containing fit labels
    :rtype:"""
    pass
