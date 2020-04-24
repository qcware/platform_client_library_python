from typing import Optional, Callable
from ..serialize_quasar import quasar_to_sequence, sequence_to_quasar, probability_histogram_to_dict
from .helpers import ndarray_to_dict, dict_to_ndarray
_to_wire_result_replacers = {}


def server_result_to_wire(method_name: str, worker_result: object):
    f = _to_wire_result_replacers.get(method_name, lambda x: x)
    return f(worker_result)


_from_wire_result_replacers = {}


def client_result_from_wire(method_name: str, worker_result: object):
    f = _from_wire_result_replacers.get(method_name, lambda x: x)
    return f(worker_result)


def register_result_transform(method_name: str,
                              to_wire: Optional[Callable] = None,
                              from_wire: Optional[Callable] = None):
    if to_wire is not None:
        _to_wire_result_replacers[method_name] = to_wire
    if from_wire is not None:
        _from_wire_result_replacers[method_name] = from_wire


register_result_transform('qio.loader',
                          to_wire=lambda x: list(quasar_to_sequence(x)),
                          from_wire=sequence_to_quasar)
register_result_transform('circuits.run_measurement',
                          to_wire=probability_histogram_to_dict)
register_result_transform('circuits.run_statevector',
                          to_wire=ndarray_to_dict,
                          from_wire=dict_to_ndarray)
