#  AUTO-GENERATED FILE - MODIFY AT OWN RISK
#  Project: qcware
#  Copyright (c) 2019 QC Ware Corp - All Rights Reserved


  
from .. import logger
from ..api_calls import post_call, wait_for_call, handle_result
from ..util.transforms import client_args_to_wire
  


def find_optimal_qaoa_angles(Q:dict={}, num_evals:int=100, api_key:str=None, host:str=None):
    r"""Finds the optimal expectation values for a given cost function, to be used in QAOA.

Arguments:

:param Q: The objective function matrix.  As :math:`Q` is usually sparse, it should be specified as a Python dictionary with integer pairs :math:`(i,j)` as keys (representing the :math:`(i,j)`th entry of :math:`Q`) and integer or float values.
:type Q: dict

:param num_evals: The number of evaluations used for :math:`\beta`/:math:`\gamma`
:type num_evals: int


:return: A list of the best 10 expectation values found and the corresponding :math:`\beta`/:math:`\gamma` pairs
:rtype: list
    """
    data = client_args_to_wire('optimization.find_optimal_qaoa_angles', **locals())
    api_call = post_call('optimization/find_optimal_qaoa_angles', data, host=host )
    logger.info(f'API call to optimization.find_optimal_qaoa_angles successful. Your API token is {api_call["uid"]}')
    return handle_result(wait_for_call(api_key=api_key,
                                       host=host,
                                       call_token=api_call['uid']))
