"""
Methods to transform FROM native types used by the backends
TO serializable types for the api to send to the client
"""
from ..serialize_quasar import (quasar_to_string, string_to_quasar,
                                pauli_to_list, list_to_pauli)
from .helpers import (ndarray_to_dict, dict_to_ndarray, scalar_to_dict,
                      dict_to_scalar, remap_q_indices_from_strings,
                      remap_q_indices_to_strings, complex_dtype_to_string,
                      string_to_complex_dtype)
from typing import Optional, Mapping, Callable


def update_with_replacers(d: Mapping[object, object],
                          replacers: Mapping[object, Callable]):
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
    if method_name == 'circuits.run_backend_method':
        method_name = '_shadowed.' + kwargs.get('method', '')
        inner_kwargs = client_args_to_wire(method_name,
                                           **kwargs.get('kwargs', {}))
        return {**kwargs, **{'kwargs': inner_kwargs}}
    else:
        return update_with_replacers(
            kwargs, _to_wire_arg_replacers.get(method_name, {}))


_from_wire_arg_replacers = {}


def server_args_from_wire(method_name: str, **kwargs):
    # grab the dict of
    # key replacers and apply them
    if method_name == 'circuits.run_backend_method':
        method_name = '_shadowed.' + kwargs.get('method', '')
        inner_kwargs = server_args_from_wire(method_name,
                                             **kwargs.get('kwargs', {}))
        return {**kwargs, **{'kwargs': inner_kwargs}}
    else:
        return update_with_replacers(
            kwargs, _from_wire_arg_replacers.get(method_name, {}))


def register_argument_transform(method_name: str,
                                to_wire: Optional[dict] = {},
                                from_wire: Optional[dict] = {}):
    _to_wire_arg_replacers[method_name] = to_wire
    _from_wire_arg_replacers[method_name] = from_wire


register_argument_transform('optimization.solve_binary',
                            to_wire={'Q': remap_q_indices_to_strings},
                            from_wire={'Q': remap_q_indices_from_strings})

register_argument_transform('optimization.find_optimal_qaoa_angles',
                            to_wire={'Q': remap_q_indices_to_strings},
                            from_wire={'Q': remap_q_indices_from_strings})

register_argument_transform('qio.loader',
                            to_wire={'data': ndarray_to_dict},
                            from_wire={'data': dict_to_ndarray})

register_argument_transform('qml.fit_and_predict',
                            to_wire={
                                'X': ndarray_to_dict,
                                'y': ndarray_to_dict,
                                'T': ndarray_to_dict
                            },
                            from_wire={
                                'X': dict_to_ndarray,
                                'y': dict_to_ndarray,
                                'T': dict_to_ndarray
                            })

register_argument_transform('_shadowed.run_measurement',
                            to_wire={
                                'circuit': quasar_to_string,
                                'statevector': ndarray_to_dict,
                                'dtype': complex_dtype_to_string
                            },
                            from_wire={
                                'statevector': dict_to_ndarray,
                                'dtype': string_to_complex_dtype
                            })

register_argument_transform('_shadowed.run_statevector',
                            to_wire={
                                'circuit': quasar_to_string,
                                'statevector': ndarray_to_dict,
                                'dtype': complex_dtype_to_string
                            },
                            from_wire={
                                'statevector': dict_to_ndarray,
                                'dtype': string_to_complex_dtype
                            })

register_argument_transform('_shadowed.circuit_in_basis',
                            to_wire={
                                'circuit': quasar_to_string,
                            },
                            from_wire={})
register_argument_transform('_shadowed.run_density_matrix',
                            to_wire=dict(circuit=quasar_to_string,
                                         statevector=ndarray_to_dict),
                            from_wire=dict(statevector=dict_to_ndarray))
register_argument_transform('_shadowed.run_pauli_diagonal',
                            to_wire=dict(pauli=pauli_to_list),
                            from_wire=dict(pauli=list_to_pauli))
register_argument_transform('_shadowed.run_pauli_expectation',
                            to_wire=dict(circuit=quasar_to_string,
                                         pauli=pauli_to_list,
                                         statevector=ndarray_to_dict),
                            from_wire=dict(pauli=list_to_pauli,
                                           statevector=dict_to_ndarray))
register_argument_transform('_shadowed.run_pauli_expectation_ideal',
                            to_wire=dict(circuit=quasar_to_string,
                                         pauli=pauli_to_list,
                                         statevector=ndarray_to_dict),
                            from_wire=dict(pauli=list_to_pauli,
                                           statevector=dict_to_ndarray))
register_argument_transform('_shadowed.run_pauli_expectation_measurement',
                            to_wire=dict(circuit=quasar_to_string,
                                         pauli=pauli_to_list,
                                         statevector=ndarray_to_dict),
                            from_wire=dict(pauli=list_to_pauli,
                                           statevector=dict_to_ndarray))
register_argument_transform('_shadowed.run_pauli_expectation_value',
                            to_wire=dict(circuit=quasar_to_string,
                                         pauli=pauli_to_list,
                                         statevector=ndarray_to_dict),
                            from_wire=dict(pauli=list_to_pauli,
                                           statevector=dict_to_ndarray))
register_argument_transform('_shadowed.run_pauli_expectation_value_gradient',
                            to_wire=dict(circuit=quasar_to_string,
                                         pauli=pauli_to_list,
                                         statevector=ndarray_to_dict),
                            from_wire=dict(pauli=list_to_pauli,
                                           statevector=dict_to_ndarray))
register_argument_transform('_shadowed.run_pauli_expectation_value_ideal',
                            to_wire=dict(circuit=quasar_to_string,
                                         pauli=pauli_to_list,
                                         statevector=ndarray_to_dict),
                            from_wire=dict(pauli=list_to_pauli,
                                           statevector=dict_to_ndarray))
register_argument_transform('_shadowed.run_pauli_sigma',
                            to_wire=dict(pauli=pauli_to_list,
                                         statevector=ndarray_to_dict),
                            from_wire=dict(pauli=list_to_pauli,
                                           statevector=dict_to_ndarray))
register_argument_transform('_shadowed.run_unitary',
                            to_wire=dict(circuit=quasar_to_string),
                            from_wire=dict())
