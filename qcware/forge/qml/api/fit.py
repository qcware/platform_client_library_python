#  AUTO-GENERATED FILE - MODIFY AT OWN RISK
#  Project: qcware
#  Copyright (c) 2019 QC Ware Corp - All Rights Reserved

import numpy

import numpy.typing

from qcware.types.qml import FitData

import warnings
from qcware.forge.api_calls import declare_api_call


@declare_api_call(name="qml.fit", endpoint="qml/fit")
def fit(
    X: numpy.typing.ArrayLike,
    model: str,
    y: numpy.typing.ArrayLike = None,
    parameters: dict = {"num_measurements": 100},
    backend: str = "qcware/cpu_simulator",
):
    r"""This function fits data to a quantum model for purposes of classification.
    Four clustering models are implemented at this time (see parameter `model`)

    Arguments:

    :param X: Training data: :math:`(N\times d)` array containing training data
    :type X: numpy.typing.ArrayLike

    :param model: String for the clustering model; one of ['QNearestCentroid', 'QNeighborsClassifier', 'QNeighborsRegressor', 'QMeans']
    :type model: str

    :param y: Label vector: length :math:`d` array containing respective labels of each data, defaults to None
    :type y: numpy.typing.ArrayLike

    :param parameters: Dictionary containing parameters for the model, defaults to {'num_measurements': 100}
    :type parameters: dict

    :param backend: String describing the backend to use, defaults to qcware/cpu_simulator
    :type backend: str


    :return: A FitData structure holding information to be passed back for the prediction step.
    :rtype: FitData"""
    pass
