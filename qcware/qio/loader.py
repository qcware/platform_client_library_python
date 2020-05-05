#  AUTO-GENERATED FILE - MODIFY AT OWN RISK
#  Project: qcware
#  Copyright (c) 2019 QC Ware Corp - All Rights Reserved


  
import numpy
  
import asyncio
from .. import logger
from ..api_calls import post_call, wait_for_call, handle_result
from ..util.transforms import client_args_to_wire
from ..exceptions import ApiTimeoutError  


def loader(data:numpy.ndarray, mode:str='optimized', at_beginning_of_circuit:bool=True, api_key:str=None, host:str=None):
    r"""Creates a circuit which loads an array of classical data into the state space of a quantum computer or simulator.  This is useful in order to act on known data or to simulator quantum RAM.

Arguments:

:param data: A 1-d array representing the classical data to be represented in the circuit
:type data: numpy.ndarray

:param mode: Whether to used the "optimized" loader (using approximately :math:`~sqrt(d)` depth and :math:`~sqrt(d)` qubits) or the "parallel" loader (using approximately :math:`log(d)` depth and `d` qubits., defaults to optimized
:type mode: str

:param at_beginning_of_circuit: Whether the loader is at the beginning of the circuit (in which it performs an initial X gate on the first qubit), defaults to True
:type at_beginning_of_circuit: bool


:return: A Quasar circuit suitable for execution on any quasar backend supporting the required gates which loads the classical vector into a quantum state.
:rtype: quasar.Circuit
    """
    data = client_args_to_wire('qio.loader', **locals())
    api_call = post_call('qio/loader', data, host=host )
    logger.info(f'API call to qio.loader successful. Your API token is {api_call["uid"]}')
    return handle_result(wait_for_call(api_key=api_key,
                                       host=host,
                                       call_token=api_call['uid']))


async def async_loader(data:numpy.ndarray, mode:str='optimized', at_beginning_of_circuit:bool=True, api_key:str=None, host:str=None):
    r"""Async version of loader
Creates a circuit which loads an array of classical data into the state space of a quantum computer or simulator.  This is useful in order to act on known data or to simulator quantum RAM.


Arguments:

:param data: A 1-d array representing the classical data to be represented in the circuit
:type data: numpy.ndarray

:param mode: Whether to used the "optimized" loader (using approximately :math:`~sqrt(d)` depth and :math:`~sqrt(d)` qubits) or the "parallel" loader (using approximately :math:`log(d)` depth and `d` qubits., defaults to optimized
:type mode: str

:param at_beginning_of_circuit: Whether the loader is at the beginning of the circuit (in which it performs an initial X gate on the first qubit), defaults to True
:type at_beginning_of_circuit: bool


:return: A Quasar circuit suitable for execution on any quasar backend supporting the required gates which loads the classical vector into a quantum state.
:rtype: quasar.Circuit
    """
    data = client_args_to_wire('qio.loader', **locals())
    api_call = post_call('qio/loader', data, host=host )
    logger.info(f'API call to qio.loader successful. Your API token is {api_call["uid"]}')

    while True:
        try:
            return handle_result(wait_for_call(api_key=api_key,
                                               host=host,
                                               call_token=api_call['uid']))
        except ApiTimeoutError as e:
            await asyncio.sleep(5)


