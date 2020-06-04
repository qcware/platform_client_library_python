#  AUTO-GENERATED FILE - MODIFY AT OWN RISK
#  Project: qcware
#  Copyright (c) 2019 QC Ware Corp - All Rights Reserved


  
import asyncio
from .. import logger
from ..api_calls import post_call, wait_for_call, handle_result
from ..util.transforms import client_args_to_wire
from ..exceptions import ApiTimeoutError  


def run_backend_method(backend:str, method:str, kwargs:dict, api_key:str=None, host:str=None):
    r"""Runs an arbitrary backend method.  This API call is not intended to be used directly by users; rather, it is meant to be called by the QuasarBackend class to transparently delegate class method calls to Forge API endpoints.

Arguments:

:param backend: string representing the backend
:type backend: str

:param method: name of the method to be called
:type method: str

:param kwargs: Keyword args passed to the method.  Positional args should be converted to kwargs
:type kwargs: dict


:return: variable; see Quasar documentation
:rtype: object
    """
    data = client_args_to_wire('circuits.run_backend_method', **locals())
    api_call = post_call('circuits/run_backend_method', data, host=host )
    logger.info(f'API call to circuits.run_backend_method successful. Your API token is {api_call["uid"]}')
    return handle_result(wait_for_call(api_key=api_key,
                                       host=host,
                                       call_token=api_call['uid']))


async def async_run_backend_method(backend:str, method:str, kwargs:dict, api_key:str=None, host:str=None):
    r"""Async version of run_backend_method
Runs an arbitrary backend method.  This API call is not intended to be used directly by users; rather, it is meant to be called by the QuasarBackend class to transparently delegate class method calls to Forge API endpoints.


Arguments:

:param backend: string representing the backend
:type backend: str

:param method: name of the method to be called
:type method: str

:param kwargs: Keyword args passed to the method.  Positional args should be converted to kwargs
:type kwargs: dict


:return: variable; see Quasar documentation
:rtype: object
    """
    data = client_args_to_wire('circuits.run_backend_method', **locals())
    api_call = post_call('circuits/run_backend_method', data, host=host )
    logger.info(f'API call to circuits.run_backend_method successful. Your API token is {api_call["uid"]}')

    while True:
        try:
            return handle_result(wait_for_call(api_key=api_key,
                                               host=host,
                                               call_token=api_call['uid']))
        except ApiTimeoutError as e:
            await asyncio.sleep(5)


