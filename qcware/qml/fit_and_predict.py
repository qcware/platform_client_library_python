#  AUTO-GENERATED FILE - MODIFY AT OWN RISK
#  Project: qcware
#  Copyright (c) 2019 QC Ware Corp - All Rights Reserved

import numpy

import asyncio
from .. import logger
from ..api_calls import post_call, wait_for_call, handle_result
from ..util.transforms import client_args_to_wire
from ..exceptions import ApiTimeoutError


def fit_and_predict(X: numpy.array,
                    model: str,
                    y: numpy.array = None,
                    T: numpy.array = None,
                    parameters: dict = {},
                    backend: str = 'classical/simulator',
                    api_key: str = None,
                    host: str = None):
    r"""This function combines both the fitting of data to a quantum model for the purposes of classification and also the use of that trained model for classifying new data.
The interface and use are similar to scikit-learn's fit and predict functions.  At the present time, since the fit data comprises (in many cases) both classical and quantum data difficult to serialize, the fitting and prediction are done in a single step.  We are looking to separate them into separate fit and predict steps in the future.
Four clustering models are implemented at this time (see parameter `model`)

Arguments:

:param X: 
:type X: numpy.array

:param model: 
:type model: str

:param y: , defaults to None
:type y: numpy.array

:param T: , defaults to None
:type T: numpy.array

:param parameters: , defaults to {}
:type parameters: dict

:param backend: , defaults to classical/simulator
:type backend: str


:return: 
:rtype: 
    """
    data = client_args_to_wire('qml.fit_and_predict', **locals())
    api_call = post_call('qml/fit_and_predict', data, host=host)
    logger.info(
        f'API call to qml.fit_and_predict successful. Your API token is {api_call["uid"]}'
    )
    return handle_result(
        wait_for_call(api_key=api_key, host=host, call_token=api_call['uid']))


async def async_fit_and_predict(X: numpy.array,
                                model: str,
                                y: numpy.array = None,
                                T: numpy.array = None,
                                parameters: dict = {},
                                backend: str = 'classical/simulator',
                                api_key: str = None,
                                host: str = None):
    r"""Async version of fit_and_predict
This function combines both the fitting of data to a quantum model for the purposes of classification and also the use of that trained model for classifying new data.
The interface and use are similar to scikit-learn's fit and predict functions.  At the present time, since the fit data comprises (in many cases) both classical and quantum data difficult to serialize, the fitting and prediction are done in a single step.  We are looking to separate them into separate fit and predict steps in the future.
Four clustering models are implemented at this time (see parameter `model`)


Arguments:

:param X: 
:type X: numpy.array

:param model: 
:type model: str

:param y: , defaults to None
:type y: numpy.array

:param T: , defaults to None
:type T: numpy.array

:param parameters: , defaults to {}
:type parameters: dict

:param backend: , defaults to classical/simulator
:type backend: str


:return: 
:rtype: 
    """
    data = client_args_to_wire('qml.fit_and_predict', **locals())
    api_call = post_call('qml/fit_and_predict', data, host=host)
    logger.info(
        f'API call to qml.fit_and_predict successful. Your API token is {api_call["uid"]}'
    )

    while True:
        try:
            return handle_result(
                wait_for_call(api_key=api_key,
                              host=host,
                              call_token=api_call['uid']))
        except ApiTimeoutError as e:
            await asyncio.sleep(5)
