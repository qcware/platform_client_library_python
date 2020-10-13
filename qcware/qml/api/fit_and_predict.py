#  AUTO-GENERATED FILE - MODIFY AT OWN RISK
#  Project: qcware
#  Copyright (c) 2019 QC Ware Corp - All Rights Reserved

import numpy

import asyncio
from ... import logger
from ...api_calls import post_call, wait_for_call, handle_result, async_retrieve_result
from ...util.transforms import client_args_to_wire
from ...exceptions import ApiTimeoutError
from ...config import (ApiCallContext, client_timeout,
                       async_interval_between_tries)


def submit_fit_and_predict(X: numpy.array,
                           model: str,
                           y: numpy.array = None,
                           T: numpy.array = None,
                           parameters: dict = {},
                           backend: str = 'qcware/cpu_simulator') -> str:
    r"""This function combines both the fitting of data to a quantum model for the purposes of classification and also the use of that trained model for classifying new data.
The interface and use are similar to scikit-learn's fit and predict functions.  At the present time, since the fit data comprises (in many cases) both classical and quantum data difficult to serialize, the fitting and prediction are done in a single step.  We are looking to separate them into separate fit and predict steps in the future.
Four clustering models are implemented at this time (see parameter `model`)

Arguments:

:param X: Training data: :math:`(N\times d)` array containing training data
:type X: numpy.array

:param model: String for the clustering model; one of ['QNearestCentroid', 'QNeighborsClassifier', 'QNeighborsRegressor', 'QMeans']
:type model: str

:param y: Label vector: length :math:`d` array containing respective labels of each data, defaults to None
:type y: numpy.array

:param T: Test data: :math:`(M\times d)` array containing test data, defaults to None
:type T: numpy.array

:param parameters: Dictionary containing parameters for the model, defaults to {}
:type parameters: dict

:param backend: String describing the backend to use; currently one of [qcware/cpu_simulator, qcware/gpu_simulator], defaults to qcware/cpu_simulator
:type backend: str


:return: An API call UID string
:rtype: str
    """
    data = client_args_to_wire('qml.fit_and_predict', **locals())
    api_call = post_call('qml/fit_and_predict', data)
    return api_call['uid']


def fit_and_predict(X: numpy.array,
                    model: str,
                    y: numpy.array = None,
                    T: numpy.array = None,
                    parameters: dict = {},
                    backend: str = 'qcware/cpu_simulator'):
    r"""This function combines both the fitting of data to a quantum model for the purposes of classification and also the use of that trained model for classifying new data.
The interface and use are similar to scikit-learn's fit and predict functions.  At the present time, since the fit data comprises (in many cases) both classical and quantum data difficult to serialize, the fitting and prediction are done in a single step.  We are looking to separate them into separate fit and predict steps in the future.
Four clustering models are implemented at this time (see parameter `model`)

Arguments:

:param X: Training data: :math:`(N\times d)` array containing training data
:type X: numpy.array

:param model: String for the clustering model; one of ['QNearestCentroid', 'QNeighborsClassifier', 'QNeighborsRegressor', 'QMeans']
:type model: str

:param y: Label vector: length :math:`d` array containing respective labels of each data, defaults to None
:type y: numpy.array

:param T: Test data: :math:`(M\times d)` array containing test data, defaults to None
:type T: numpy.array

:param parameters: Dictionary containing parameters for the model, defaults to {}
:type parameters: dict

:param backend: String describing the backend to use; currently one of [qcware/cpu_simulator, qcware/gpu_simulator], defaults to qcware/cpu_simulator
:type backend: str


:return: A numpy array the length of the test data `T` containing fit labels
:rtype: numpy.array
    """
    data = client_args_to_wire('qml.fit_and_predict', **locals())
    api_call = post_call('qml/fit_and_predict', data)
    api_call_id = api_call['uid']
    logger.info(
        f'API call to qml.fit_and_predict successful. Your API token is {api_call_id}'
    )
    if client_timeout() == 0:
        raise ApiTimeoutError(
            f"Api call timed out; can retrieve with qcware.api_calls.retrieve_result(call_token=\"{api_call_id}\")",
            api_call)
    else:
        return handle_result(wait_for_call(call_token=api_call_id))


async def async_fit_and_predict(X: numpy.array,
                                model: str,
                                y: numpy.array = None,
                                T: numpy.array = None,
                                parameters: dict = {},
                                backend: str = 'qcware/cpu_simulator'):
    r"""Async version of fit_and_predict
This function combines both the fitting of data to a quantum model for the purposes of classification and also the use of that trained model for classifying new data.
The interface and use are similar to scikit-learn's fit and predict functions.  At the present time, since the fit data comprises (in many cases) both classical and quantum data difficult to serialize, the fitting and prediction are done in a single step.  We are looking to separate them into separate fit and predict steps in the future.
Four clustering models are implemented at this time (see parameter `model`)


Arguments:

:param X: Training data: :math:`(N\times d)` array containing training data
:type X: numpy.array

:param model: String for the clustering model; one of ['QNearestCentroid', 'QNeighborsClassifier', 'QNeighborsRegressor', 'QMeans']
:type model: str

:param y: Label vector: length :math:`d` array containing respective labels of each data, defaults to None
:type y: numpy.array

:param T: Test data: :math:`(M\times d)` array containing test data, defaults to None
:type T: numpy.array

:param parameters: Dictionary containing parameters for the model, defaults to {}
:type parameters: dict

:param backend: String describing the backend to use; currently one of [qcware/cpu_simulator, qcware/gpu_simulator], defaults to qcware/cpu_simulator
:type backend: str


:return: A numpy array the length of the test data `T` containing fit labels
:rtype: numpy.array
    """
    data = client_args_to_wire('qml.fit_and_predict', **locals())
    api_call = post_call('qml/fit_and_predict', data)
    logger.info(
        f'API call to qml.fit_and_predict successful. Your API token is {api_call["uid"]}'
    )

    return await async_retrieve_result(api_call["uid"])
