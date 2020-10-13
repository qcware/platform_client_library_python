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


def submit_loader(data: numpy.ndarray,
                  mode: str = 'optimized',
                  at_beginning_of_circuit: bool = True) -> str:
    r"""Creates a circuit which loads an array of classical data into the state space of a quantum computer or simulator.  This is useful in order to act on known data or to simulator quantum RAM.

Arguments:

:param data: A 1-d array representing the classical data to be represented in the circuit
:type data: numpy.ndarray

:param mode: Whether to used the "optimized" loader (using approximately :math:`~sqrt(d)` depth and :math:`~sqrt(d)` qubits) or the "parallel" loader (using approximately :math:`log(d)` depth and `d` qubits., defaults to optimized
:type mode: str

:param at_beginning_of_circuit: Whether the loader is at the beginning of the circuit (in which it performs an initial X gate on the first qubit), defaults to True
:type at_beginning_of_circuit: bool


:return: An API call UID string
:rtype: str
    """
    data = client_args_to_wire('qio.loader', **locals())
    api_call = post_call('qio/loader', data)
    return api_call['uid']


def loader(data: numpy.ndarray,
           mode: str = 'optimized',
           at_beginning_of_circuit: bool = True):
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
    api_call = post_call('qio/loader', data)
    api_call_id = api_call['uid']
    logger.info(
        f'API call to qio.loader successful. Your API token is {api_call_id}')
    if client_timeout() == 0:
        raise ApiTimeoutError(
            f"Api call timed out; can retrieve with qcware.api_calls.retrieve_result(call_token=\"{api_call_id}\")",
            api_call)
    else:
        return handle_result(wait_for_call(call_token=api_call_id))


async def async_loader(data: numpy.ndarray,
                       mode: str = 'optimized',
                       at_beginning_of_circuit: bool = True):
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
    api_call = post_call('qio/loader', data)
    logger.info(
        f'API call to qio.loader successful. Your API token is {api_call["uid"]}'
    )

    return await async_retrieve_result(api_call["uid"])
