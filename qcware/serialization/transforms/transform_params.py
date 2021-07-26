"""
Methods to transform FROM native types used by the backends
TO serializable types for the api to send to the client.

This file should primarily contain the marshaling for argument
transformations and functions, not so much the transformation functions
themselves for particular types (those go in the helpers file).
"""
from ..serialize_quasar import (
    quasar_to_string,
    string_to_quasar,
    pauli_to_list,
    list_to_pauli,
)
from .helpers import (
    ndarray_to_dict,
    dict_to_ndarray,
    scalar_to_dict,
    dict_to_scalar,
    numeric_to_dict,
    dict_to_numeric,
    remap_q_indices_from_strings,
    remap_q_indices_to_strings,
    complex_or_real_dtype_to_string,
    string_to_complex_or_real_dtype,
    to_wire,
    polynomial_objective_from_wire,
    constraints_from_wire,
    binary_problem_from_wire,
    binary_results_from_wire,
)
from typing import Optional, Mapping, Callable
from ...types.optimization import BinaryProblem


def update_with_replacers(
    d: Mapping[object, object], replacers: Mapping[object, Callable]
):
    """for all (k,f) in replacers, updates the dict entry marked by k by calling the
    function f on the value"""
    result = d.copy()
    for k, f in replacers.items():
        if k in result:
            result[k] = f(result[k])
    return result


_to_wire_arg_replacers = {}


def client_args_to_wire(method_name: str, **kwargs):
    # grab the dict of
    # key replacers and apply them
    if method_name == "circuits.run_backend_method":
        method_name = "_shadowed." + kwargs.get("method", "")
        inner_kwargs = client_args_to_wire(method_name, **kwargs.get("kwargs", {}))
        return {**kwargs, **{"kwargs": inner_kwargs}}
    else:
        return update_with_replacers(
            kwargs, _to_wire_arg_replacers.get(method_name, {})
        )


_from_wire_arg_replacers = {}


def server_args_from_wire(method_name: str, **kwargs):
    # grab the dict of
    # key replacers and apply them
    if method_name == "circuits.run_backend_method":
        method_name = "_shadowed." + kwargs.get("method", "")
        inner_kwargs = server_args_from_wire(method_name, **kwargs.get("kwargs", {}))
        return {**kwargs, **{"kwargs": inner_kwargs}}
    else:
        return update_with_replacers(
            kwargs, _from_wire_arg_replacers.get(method_name, {})
        )


def register_argument_transform(
    method_name: str, to_wire: Optional[dict] = None, from_wire: Optional[dict] = None
):
    if to_wire is None:
        to_wire = dict()
    if from_wire is None:
        from_wire = dict()

    _to_wire_arg_replacers[method_name] = to_wire
    _from_wire_arg_replacers[method_name] = from_wire


register_argument_transform(
    "optimization.optimize_binary",
    to_wire={"instance": to_wire},
    from_wire={"instance": binary_problem_from_wire},
)

register_argument_transform(
    "optimization.find_optimal_qaoa_angles",
    to_wire={"Q": remap_q_indices_to_strings},
    from_wire={"Q": remap_q_indices_from_strings},
)

register_argument_transform(
    "optimization.qaoa_expectation_value",
    to_wire={
        "problem_instance": to_wire,
        "beta": ndarray_to_dict,
        "gamma": ndarray_to_dict,
    },
    from_wire={
        "problem_instance": binary_problem_from_wire,
        "beta": dict_to_ndarray,
        "gamma": dict_to_ndarray,
    },
)

register_argument_transform(
    "optimization.qaoa_sample",
    to_wire={
        "problem_instance": to_wire,
        "beta": ndarray_to_dict,
        "gamma": ndarray_to_dict,
    },
    from_wire={
        "problem_instance": binary_problem_from_wire,
        "beta": dict_to_ndarray,
        "gamma": dict_to_ndarray,
    },
)


register_argument_transform(
    "optimization.brute_force_minimize",
    to_wire={
        "objective": lambda x: to_wire(x),
        "constraints": lambda x: to_wire(x) if x is not None else None,
    },
    from_wire={
        "objective": polynomial_objective_from_wire,
        "constraints": lambda x: constraints_from_wire(x) if x is not None else None,
    },
)

register_argument_transform(
    "qio.loader", to_wire={"data": ndarray_to_dict}, from_wire={"data": dict_to_ndarray}
)

register_argument_transform(
    "qml.fit_and_predict",
    to_wire={"X": ndarray_to_dict, "y": ndarray_to_dict, "T": ndarray_to_dict},
    from_wire={"X": dict_to_ndarray, "y": dict_to_ndarray, "T": dict_to_ndarray},
)

register_argument_transform(
    "qutils.qdot",
    to_wire={
        "x": numeric_to_dict,
        "y": numeric_to_dict,
        "circuit": lambda x: quasar_to_string(x) if x is not None else None,
    },
    from_wire={
        "x": dict_to_numeric,
        "y": dict_to_numeric,
        "circuit": lambda x: string_to_quasar(x) if x is not None else None,
    },
)

register_argument_transform(
    "qutils.distance_estimation",
    to_wire={
        "x": numeric_to_dict,
        "y": numeric_to_dict,
        "circuit": lambda x: quasar_to_string(x) if x is not None else None,
    },
    from_wire={
        "x": dict_to_numeric,
        "y": dict_to_numeric,
        "circuit": lambda x: string_to_quasar(x) if x is not None else None,
    },
)

register_argument_transform(
    "_shadowed.run_measurement",
    to_wire={
        "circuit": quasar_to_string,
        "statevector": ndarray_to_dict,
        "dtype": complex_or_real_dtype_to_string,
    },
    from_wire={
        "statevector": dict_to_ndarray,
        "dtype": string_to_complex_or_real_dtype,
    },
)

register_argument_transform(
    "_shadowed.run_statevector",
    to_wire={
        "circuit": quasar_to_string,
        "statevector": ndarray_to_dict,
        "dtype": complex_or_real_dtype_to_string,
    },
    from_wire={
        "statevector": dict_to_ndarray,
        "dtype": string_to_complex_or_real_dtype,
    },
)

register_argument_transform(
    "_shadowed.circuit_in_basis",
    to_wire={
        "circuit": quasar_to_string,
    },
    from_wire={},
)
register_argument_transform(
    "_shadowed.run_density_matrix",
    to_wire=dict(
        circuit=quasar_to_string,
        statevector=ndarray_to_dict,
        dtype=complex_or_real_dtype_to_string,
    ),
    from_wire=dict(statevector=dict_to_ndarray, dtype=string_to_complex_or_real_dtype),
)
register_argument_transform(
    "_shadowed.run_pauli_diagonal",
    to_wire=dict(pauli=pauli_to_list, dtype=complex_or_real_dtype_to_string),
    from_wire=dict(pauli=list_to_pauli, dtype=string_to_complex_or_real_dtype),
)
register_argument_transform(
    "_shadowed.run_pauli_expectation",
    to_wire=dict(
        circuit=quasar_to_string,
        pauli=pauli_to_list,
        statevector=ndarray_to_dict,
        dtype=complex_or_real_dtype_to_string,
    ),
    from_wire=dict(
        pauli=list_to_pauli,
        statevector=dict_to_ndarray,
        dtype=string_to_complex_or_real_dtype,
    ),
)
register_argument_transform(
    "_shadowed.run_pauli_expectation_ideal",
    to_wire=dict(
        circuit=quasar_to_string,
        pauli=pauli_to_list,
        statevector=ndarray_to_dict,
        dtype=complex_or_real_dtype_to_string,
    ),
    from_wire=dict(
        pauli=list_to_pauli,
        statevector=dict_to_ndarray,
        dtype=string_to_complex_or_real_dtype,
    ),
)
register_argument_transform(
    "_shadowed.run_pauli_expectation_measurement",
    to_wire=dict(
        circuit=quasar_to_string,
        pauli=pauli_to_list,
        statevector=ndarray_to_dict,
        dtype=complex_or_real_dtype_to_string,
    ),
    from_wire=dict(
        pauli=list_to_pauli,
        statevector=dict_to_ndarray,
        dtype=string_to_complex_or_real_dtype,
    ),
)
register_argument_transform(
    "_shadowed.run_pauli_expectation_value",
    to_wire=dict(
        circuit=quasar_to_string,
        pauli=pauli_to_list,
        statevector=ndarray_to_dict,
        dtype=complex_or_real_dtype_to_string,
    ),
    from_wire=dict(
        pauli=list_to_pauli,
        statevector=dict_to_ndarray,
        dtype=string_to_complex_or_real_dtype,
    ),
)
register_argument_transform(
    "_shadowed.run_pauli_expectation_value_gradient",
    to_wire=dict(
        circuit=quasar_to_string,
        pauli=pauli_to_list,
        statevector=ndarray_to_dict,
        dtype=complex_or_real_dtype_to_string,
    ),
    from_wire=dict(
        pauli=list_to_pauli,
        statevector=dict_to_ndarray,
        dtype=string_to_complex_or_real_dtype,
    ),
)
register_argument_transform(
    "_shadowed.run_pauli_expectation_value_ideal",
    to_wire=dict(
        circuit=quasar_to_string,
        pauli=pauli_to_list,
        statevector=ndarray_to_dict,
        dtype=complex_or_real_dtype_to_string,
    ),
    from_wire=dict(
        pauli=list_to_pauli,
        statevector=dict_to_ndarray,
        dtype=string_to_complex_or_real_dtype,
    ),
)
register_argument_transform(
    "_shadowed.run_pauli_sigma",
    to_wire=dict(
        pauli=pauli_to_list,
        statevector=ndarray_to_dict,
        dtype=complex_or_real_dtype_to_string,
    ),
    from_wire=dict(
        pauli=list_to_pauli,
        statevector=dict_to_ndarray,
        dtype=string_to_complex_or_real_dtype,
    ),
)
register_argument_transform(
    "_shadowed.run_unitary",
    to_wire=dict(circuit=quasar_to_string, dtype=complex_or_real_dtype_to_string),
    from_wire=dict(dtype=string_to_complex_or_real_dtype),
)
