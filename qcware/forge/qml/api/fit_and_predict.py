#  AUTO-GENERATED FILE - MODIFY AT OWN RISK
#  Project: qcware
#  Copyright (c) 2019 QC Ware Corp - All Rights Reserved

import numpy

import numpy.typing

import warnings
from qcware.forge.api_calls import declare_api_call


@declare_api_call(name="qml.fit_and_predict", endpoint="qml/fit_and_predict")
def fit_and_predict(
    X: numpy.typing.ArrayLike,
    model: str,
    y: numpy.typing.ArrayLike = None,
    T: numpy.typing.ArrayLike = None,
    parameters: dict = {"num_measurements": 100},
    backend: str = "qcware/cpu_simulator",
):
    r"""This function combines both the fitting of data to a quantum model for the purposes of classification and also the use of that trained model for classifying new data.
    The interface and use are similar to scikit-learn's fit and predict functions.  At the present time, since the fit data comprises (in many cases) both classical and quantum data difficult to serialize, the fitting and prediction are done in a single step.  We are looking to separate them into separate fit and predict steps in the future.
    Four clustering models are implemented at this time (see parameter `model`)

    Arguments:

    :param X: Training data: :math:`(N\times d)` array containing training data
    :type X: numpy.typing.ArrayLike

    :param model: String for the clustering model; one of ['QNearestCentroid', 'QNeighborsClassifier', 'QNeighborsRegressor', 'QMeans']
    :type model: str

    :param y: Label vector: length :math:`d` array containing respective labels of each data, defaults to None
    :type y: numpy.typing.ArrayLike

    :param T: Test data: :math:`(M\times d)` array containing test data, defaults to None
    :type T: numpy.typing.ArrayLike

    :param parameters: Dictionary containing parameters for the model, defaults to {'num_measurements': 100}
    :type parameters: dict

    :param backend: String describing the backend to use, defaults to qcware/cpu_simulator
    :type backend: str


    :return: A numpy array the length of the test data `T` containing fit labels
    :rtype: numpy.array"""
    pass
