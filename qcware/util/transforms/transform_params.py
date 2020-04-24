"""
Methods to transform FROM native types used by the backends
TO serializable types for the api to send to the client
"""
from ..serialize_quasar import quasar_to_sequence, sequence_to_quasar, probability_histogram_to_dict
from .helpers import (ndarray_to_dict, dict_to_ndarray,
                      remap_q_indices_from_strings, remap_q_indices_to_strings,
                      complex_dtype_to_string, string_to_complex_dtype)
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
    return update_with_replacers(kwargs,
                                 _to_wire_arg_replacers.get(method_name, {}))


_from_wire_arg_replacers = {}


def server_args_from_wire(method_name: str, **kwargs):
    # grab the dict of
    # key replacers and apply them
    return update_with_replacers(kwargs,
                                 _from_wire_arg_replacers.get(method_name))


def register_argument_transform(method_name: str,
                                to_wire: Optional[dict] = {},
                                from_wire: Optional[dict] = {}):
    _to_wire_arg_replacers[method_name] = to_wire
    _from_wire_arg_replacers[method_name] = from_wire


register_argument_transform('optimization.solve_binary',
                            to_wire={'Q': remap_q_indices_to_strings},
                            from_wire={'Q': remap_q_indices_from_strings})

register_argument_transform('circuits.run_measurement',
                            to_wire={
                                'circuit':
                                lambda x: list(quasar_to_sequence(x)),
                                'statevector': ndarray_to_dict,
                                'dtype': complex_dtype_to_string
                            },
                            from_wire={
                                'circuit': sequence_to_quasar,
                                'statevector': dict_to_ndarray,
                                'dtype': string_to_complex_dtype
                            })

register_argument_transform('circuits.run_statevector',
                            to_wire={
                                'circuit':
                                lambda x: list(quasar_to_sequence(x)),
                                'statevector': ndarray_to_dict,
                                'dtype': complex_dtype_to_string
                            },
                            from_wire={
                                'circuit': sequence_to_quasar,
                                'statevector': dict_to_ndarray,
                                'dtype': string_to_complex_dtype
                            })

register_argument_transform('optimization.find_optimal_qaoa_angles',
                            to_wire={'Q': remap_q_indices_to_strings},
                            from_wire={'Q': remap_q_indices_from_strings})

register_argument_transform('qio.loader',
                            to_wire={'data': ndarray_to_dict},
                            from_wire={'data': dict_to_ndarray})
