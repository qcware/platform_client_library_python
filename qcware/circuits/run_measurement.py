#  AUTO-GENERATED FILE - MODIFY AT OWN RISK
#  Project: qcware
#  Copyright (c) 2019 QC Ware Corp - All Rights Reserved


  
import numpy
  
from quasar import Circuit
  
import asyncio
from .. import logger
from ..api_calls import post_call, wait_for_call, handle_result
from ..util.transforms import client_args_to_wire
from ..exceptions import ApiTimeoutError  


def run_measurement(backend:str, circuit:Circuit, nmeasurement:int=None, statevector:numpy.ndarray=None, min_qubit:int=None, nqubit:int=None, dtype:type=numpy.complex128, backend_args:object={}, api_key:str=None, host:str=None):
    r"""Executes a Quasar circuit multiple times, measuring the resulting statevector for a histogram of probabilities. This is possibly best used via the QuasarBackend class, which provides a number of extensions.

Arguments:

:param backend: A string representing the backend for execution
:type backend: str

:param circuit: The circuit to execute
:type circuit: Circuit

:param nmeasurement: The number of measurements required, defaults to None
:type nmeasurement: int

:param statevector: If the  backend supports statevector input, this provides an initial state., defaults to None
:type statevector: numpy.ndarray

:param min_qubit: The minimum occupied qubit index, defaults to None
:type min_qubit: int

:param nqubit: The total number of qubit indices in the circuit, defaults to None
:type nqubit: int

:param dtype: For some backends, particularly simulators, the type used to represent the statevector, defaults to numpy.complex128
:type dtype: type

:param backend_args: Any extra parameters to pass to the backend, defaults to {}
:type backend_args: object


:return: A quasar ProbabilityHistogram object representing the histogram of states measured during execution
:rtype: quasar.ProbabilityHistogram
    """
    data = client_args_to_wire('circuits.run_measurement', **locals())
    api_call = post_call('circuits/run_measurement', data, host=host )
    logger.info(f'API call to circuits.run_measurement successful. Your API token is {api_call["uid"]}')
    return handle_result(wait_for_call(api_key=api_key,
                                       host=host,
                                       call_token=api_call['uid']))


async def async_run_measurement(backend:str, circuit:Circuit, nmeasurement:int=None, statevector:numpy.ndarray=None, min_qubit:int=None, nqubit:int=None, dtype:type=numpy.complex128, backend_args:object={}, api_key:str=None, host:str=None):
    r"""Async version of run_measurement
Executes a Quasar circuit multiple times, measuring the resulting statevector for a histogram of probabilities. This is possibly best used via the QuasarBackend class, which provides a number of extensions.


Arguments:

:param backend: A string representing the backend for execution
:type backend: str

:param circuit: The circuit to execute
:type circuit: Circuit

:param nmeasurement: The number of measurements required, defaults to None
:type nmeasurement: int

:param statevector: If the  backend supports statevector input, this provides an initial state., defaults to None
:type statevector: numpy.ndarray

:param min_qubit: The minimum occupied qubit index, defaults to None
:type min_qubit: int

:param nqubit: The total number of qubit indices in the circuit, defaults to None
:type nqubit: int

:param dtype: For some backends, particularly simulators, the type used to represent the statevector, defaults to numpy.complex128
:type dtype: type

:param backend_args: Any extra parameters to pass to the backend, defaults to {}
:type backend_args: object


:return: A quasar ProbabilityHistogram object representing the histogram of states measured during execution
:rtype: quasar.ProbabilityHistogram
    """
    data = client_args_to_wire('circuits.run_measurement', **locals())
    api_call = post_call('circuits/run_measurement', data, host=host )
    logger.info(f'API call to circuits.run_measurement successful. Your API token is {api_call["uid"]}')

    while True:
        try:
            return handle_result(wait_for_call(api_key=api_key,
                                               host=host,
                                               call_token=api_call['uid']))
        except ApiTimeoutError as e:
            await asyncio.sleep(5)


