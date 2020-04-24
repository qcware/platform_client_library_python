#  AUTO-GENERATED FILE - MODIFY AT OWN RISK
#  Project: qcware
#  Copyright (c) 2019 QC Ware Corp - All Rights Reserved


  
from .. import logger
from ..api_calls import post_call, wait_for_call, handle_result
from ..util.transforms import client_args_to_wire
  


def has_statevector_input(backend:str=None, backend_args:object={}, api_key:str=None, host:str=None):
    r"""Whether or not this backend supports statevector input for various run methods. This can be called more elegantly by the use of the QuasarBackend class.

Arguments:

:param backend: string representing the backend
:type backend: str

:param backend_args: Dict representing any additional backend args (not implemented currently)
:type backend_args: object


:return: true if the backend supports statevector input
:rtype: bool
    """
    data = client_args_to_wire('circuits.has_statevector_input', **locals())
    api_call = post_call('circuits/has_statevector_input', data, host=host )
    logger.info(f'API call to circuits.has_statevector_input successful. Your API token is {api_call["uid"]}')
    return handle_result(wait_for_call(api_key=api_key,
                                       host=host,
                                       call_token=api_call['uid']))
