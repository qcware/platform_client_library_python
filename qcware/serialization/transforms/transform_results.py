import os
from typing import Callable, Optional, cast, Dict

import numpy
from decouple import config

from ..serialize_quasar import (
    dict_to_probability_histogram,
    list_to_pauli,
    pauli_to_list,
    probability_histogram_to_dict,
    quasar_to_list,
    sequence_to_quasar,
)
from .helpers import (
    dict_to_ndarray,
    dict_to_numeric,
    dict_to_scalar,
    ndarray_to_dict,
    numeric_to_dict,
    scalar_to_dict,
)
from .to_wire import (
    binary_results_from_wire,
    brute_optimize_result_from_wire,
    fit_data_from_wire,
    fit_data_to_wire,
    to_wire,
)

_to_wire_result_replacers: Dict[str, Callable] = {}


def debug_is_set() -> bool:
    return config("QCWARE_CLIENT_DEBUG", default=False, cast=bool)


def result_represents_error(worker_result: object):
    """
    Defines whether the result object returned by a backend function represents an
    error.  This was done by backend functions returning a dict with "error" as a key
    which conflicted with some results which inherited from dict but magically parsed
    key requests and would throw exceptions.
    """
    result = isinstance(worker_result, dict) and "error" in worker_result
    return result


def strip_traceback_if_debug_set(error_result: dict) -> dict:
    result = error_result.copy()
    if not debug_is_set() and "traceback" in result:
        result.pop("traceback")
    return result


def server_result_to_wire(method_name: str, worker_result: object):
    if result_represents_error(worker_result):
        return strip_traceback_if_debug_set(cast(dict, worker_result))
    else:
        f = _to_wire_result_replacers.get(method_name, lambda x: x)
        return f(worker_result)


_from_wire_result_replacers: Dict[str, Callable] = {}


def client_result_from_wire(method_name: str, worker_result: object):
    if result_represents_error(worker_result):
        return strip_traceback_if_debug_set(cast(dict, worker_result))
    else:
        f = _from_wire_result_replacers.get(method_name, lambda x: x)
        return f(worker_result)


def register_result_transform(
    method_name: str,
    to_wire: Optional[Callable] = None,
    from_wire: Optional[Callable] = None,
):
    if to_wire is not None:
        _to_wire_result_replacers[method_name] = to_wire
    if from_wire is not None:
        _from_wire_result_replacers[method_name] = from_wire


def transform_optimization_find_optimal_qaoa_angles_to_wire(t):
    # this function requires a little special-casing since it
    # returns a number of arrays
    return (t[0], t[1], ndarray_to_dict(t[2]))


def transform_optimization_find_optimal_qaoa_angles_from_wire(t):
    return (t[0], t[1], dict_to_ndarray(t[2]))


register_result_transform(
    "qio.loader",
    to_wire=lambda x: (quasar_to_list(x[0]), ndarray_to_dict(x[1]))
    if type(x) is tuple
    else tuple([quasar_to_list(x)]),
    from_wire=lambda x: (sequence_to_quasar(x[0]), dict_to_ndarray(x[1]))
    if len(x) == 2
    else sequence_to_quasar(x[0]),
)
register_result_transform(
    "qutils.qdot", to_wire=numeric_to_dict, from_wire=dict_to_numeric
)

register_result_transform(
    "qutils.create_qdot_circuit", to_wire=quasar_to_list, from_wire=sequence_to_quasar
)

register_result_transform(
    "qutils.qdist", to_wire=numeric_to_dict, from_wire=dict_to_numeric
)

register_result_transform(
    "circuits.run_measurement",
    to_wire=probability_histogram_to_dict,
    from_wire=dict_to_probability_histogram,
)
register_result_transform(
    "circuits.run_measurements",
    to_wire=lambda x: [probability_histogram_to_dict(y) for y in x],
    from_wire=lambda x: [dict_to_probability_histogram(y) for y in x],
)
register_result_transform(
    "circuits.run_statevector", to_wire=ndarray_to_dict, from_wire=dict_to_ndarray
)
register_result_transform(
    "optimization.find_optimal_qaoa_angles",
    to_wire=transform_optimization_find_optimal_qaoa_angles_to_wire,
    from_wire=transform_optimization_find_optimal_qaoa_angles_from_wire,
)
register_result_transform(
    "qml.fit_and_predict", to_wire=ndarray_to_dict, from_wire=dict_to_ndarray
)

register_result_transform(
    "qml.fit", to_wire=fit_data_to_wire, from_wire=fit_data_from_wire
)

register_result_transform(
    "qml.predict", to_wire=ndarray_to_dict, from_wire=dict_to_ndarray
)


def run_backend_method_to_wire(backend_method_result: dict):
    result = server_result_to_wire(
        "_shadowed." + backend_method_result["method"], backend_method_result["result"]
    )
    return dict(method=backend_method_result["method"], result=result)


def run_backend_method_from_wire(backend_method_result: dict):
    return client_result_from_wire(
        "_shadowed." + backend_method_result["method"], backend_method_result["result"]
    )


# it may seem odd to have multiple registrations for solve_binary, but
# it was named multiple things in different solvers since it could be dispatched
# to different tasks based on the back ends.


def old_binary_result_from_new(x: dict):
    br = binary_results_from_wire(x)
    result = dict(
        solution=br.lowest_value_bitstring,
        extra_info=br.result_metadata["extra_info"],
    )
    if "qubo_energy_list" in br.result_metadata:
        result["qubo_energy_list"] = qubo_energy_list = (
            br.result_metadata["qubo_energy_list"],
        )

    return result


register_result_transform(
    "optimization.optimize_binary", to_wire=to_wire, from_wire=binary_results_from_wire
)

register_result_transform(
    "optimization.qaoa_expectation_value",
    to_wire=numeric_to_dict,
    from_wire=dict_to_numeric,
)
register_result_transform(
    "optimization.qaoa_sample", to_wire=to_wire, from_wire=binary_results_from_wire
)
register_result_transform(
    "solve_qubo_with_brute_force_task",
    to_wire=to_wire,
    from_wire=lambda x: binary_results_from_wire(x),
)
register_result_transform(
    "solve_qubo_with_quasar_qaoa_simulator_task",
    to_wire=to_wire,
    from_wire=lambda x: binary_results_from_wire(x),
)
register_result_transform(
    "solve_qubo_with_dwave_task",
    to_wire=to_wire,
    from_wire=lambda x: binary_results_from_wire(x),
)
register_result_transform(
    "solve_qubo_with_quasar_qaoa_vulcan_task",
    to_wire=to_wire,
    from_wire=lambda x: binary_results_from_wire(x),
)

register_result_transform(
    "circuits.run_backend_method",
    to_wire=run_backend_method_to_wire,
    from_wire=run_backend_method_from_wire,
)
register_result_transform(
    "optimization.brute_force_minimize",
    to_wire=lambda x: x.dict(),
    from_wire=brute_optimize_result_from_wire,
)
register_result_transform(
    "_shadowed.run_measurement",
    to_wire=probability_histogram_to_dict,
    from_wire=dict_to_probability_histogram,
)
register_result_transform(
    "_shadowed.run_measurements",
    to_wire=lambda x: [probability_histogram_to_dict(y) for y in x],
    from_wire=lambda x: [dict_to_probability_histogram(y) for y in x],
)

register_result_transform(
    "_shadowed.run_statevector", to_wire=ndarray_to_dict, from_wire=dict_to_ndarray
)
register_result_transform(
    "_shadowed.circuit_in_basis", to_wire=quasar_to_list, from_wire=sequence_to_quasar
)
register_result_transform(
    "_shadowed.run_density_matrix", to_wire=ndarray_to_dict, from_wire=dict_to_ndarray
)
register_result_transform(
    "_shadowed.run_pauli_diagonal", to_wire=ndarray_to_dict, from_wire=dict_to_ndarray
)
register_result_transform(
    "_shadowed.run_pauli_expectation", to_wire=pauli_to_list, from_wire=list_to_pauli
)
register_result_transform(
    "_shadowed.run_pauli_expectation_ideal",
    to_wire=pauli_to_list,
    from_wire=list_to_pauli,
)
register_result_transform(
    "_shadowed.run_pauli_expectation_measurement",
    to_wire=pauli_to_list,
    from_wire=list_to_pauli,
)
register_result_transform(
    "_shadowed.run_pauli_expectation_value",
    to_wire=lambda x: scalar_to_dict(x, dtype=numpy.float64),
    from_wire=dict_to_scalar,
)
register_result_transform(
    "_shadowed.run_pauli_expectation_value_gradient",
    to_wire=ndarray_to_dict,
    from_wire=dict_to_ndarray,
)
register_result_transform(
    "_shadowed.run_pauli_expectation_value_ideal",
    to_wire=lambda x: scalar_to_dict(x, dtype=numpy.float64),
    from_wire=dict_to_scalar,
)
register_result_transform(
    "_shadowed.run_pauli_sigma", to_wire=ndarray_to_dict, from_wire=dict_to_ndarray
)
register_result_transform(
    "_shadowed.run_unitary", to_wire=ndarray_to_dict, from_wire=dict_to_ndarray
)
