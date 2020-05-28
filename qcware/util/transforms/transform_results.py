import os
from typing import Optional, Callable
from ..serialize_quasar import (quasar_to_sequence, sequence_to_quasar,
                                probability_histogram_to_dict, dict_to_probability_histogram)
from .helpers import ndarray_to_dict, dict_to_ndarray
_to_wire_result_replacers = {}


def debug_is_set() -> bool:
    return os.environ.get("QCWARE_CLIENT_DEBUG", False)


def result_represents_error(worker_result: object):
    return isinstance(worker_result, dict) and 'error' in worker_result


def strip_traceback_if_debug_set(error_result: dict) -> dict:
    result = error_result.copy()
    if not debug_is_set() and 'traceback' in result:
        result.pop('traceback')
    return result


def server_result_to_wire(method_name: str, worker_result: object):
    if result_represents_error(worker_result):
        return strip_traceback_if_debug_set(worker_result)
    else:
        f = _to_wire_result_replacers.get(method_name, lambda x: x)
        return f(worker_result)


_from_wire_result_replacers = {}


def client_result_from_wire(method_name: str, worker_result: object):
    if result_represents_error(worker_result):
        return strip_traceback_if_debug_set(worker_result)
    else:
        f = _from_wire_result_replacers.get(method_name, lambda x: x)
        return f(worker_result)


def register_result_transform(method_name: str,
                              to_wire: Optional[Callable] = None,
                              from_wire: Optional[Callable] = None):
    if to_wire is not None:
        _to_wire_result_replacers[method_name] = to_wire
    if from_wire is not None:
        _from_wire_result_replacers[method_name] = from_wire


def transform_optimization_find_optimal_qaoa_angles_to_wire(t):
    # this function requires a little special-casing since it
    # returns a number of arrays
    return (
        t[0],
        t[1],
        ndarray_to_dict(t[2]))


def transform_optimization_find_optimal_qaoa_angles_from_wire(t):
    return (
        t[0],
        t[1],
        dict_to_ndarray(t[2]))


register_result_transform('qio.loader',
                          to_wire=lambda x: list(quasar_to_sequence(x)),
                          from_wire=sequence_to_quasar)
register_result_transform('circuits.run_measurement',
                          to_wire=probability_histogram_to_dict,
                          from_wire=dict_to_probability_histogram)
register_result_transform('circuits.run_statevector',
                          to_wire=ndarray_to_dict,
                          from_wire=dict_to_ndarray)
register_result_transform('optimization.find_optimal_qaoa_angles',
                          to_wire=transform_optimization_find_optimal_qaoa_angles_to_wire,
                          from_wire=transform_optimization_find_optimal_qaoa_angles_from_wire)
