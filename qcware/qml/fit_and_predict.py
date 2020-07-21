#  AUTO-GENERATED FILE - MODIFY AT OWN RISK
#  Project: qcware
#  Copyright (c) 2019 QC Ware Corp - All Rights Reserved


  
import numpy
  
import asyncio
from .. import logger
from ..api_calls import post_call, wait_for_call, handle_result
from ..util.transforms import client_args_to_wire
from ..exceptions import ApiTimeoutError  


def fit_and_predict(X:numpy.array, model:str, y:numpy.array=None, T:numpy.array=None, parameters:dict={}, backend:str='classical/simulator', api_key:str=None, host:str=None):
    r"""

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
    api_call = post_call('qml/fit_and_predict', data, host=host )
    logger.info(f'API call to qml.fit_and_predict successful. Your API token is {api_call["uid"]}')
    return handle_result(wait_for_call(api_key=api_key,
                                       host=host,
                                       call_token=api_call['uid']))


async def async_fit_and_predict(X:numpy.array, model:str, y:numpy.array=None, T:numpy.array=None, parameters:dict={}, backend:str='classical/simulator', api_key:str=None, host:str=None):
    r"""Async version of fit_and_predict



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
    api_call = post_call('qml/fit_and_predict', data, host=host )
    logger.info(f'API call to qml.fit_and_predict successful. Your API token is {api_call["uid"]}')

    while True:
        try:
            return handle_result(wait_for_call(api_key=api_key,
                                               host=host,
                                               call_token=api_call['uid']))
        except ApiTimeoutError as e:
            await asyncio.sleep(5)


