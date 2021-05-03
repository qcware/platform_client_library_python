import numpy as np
import base64
from typing import Dict
import lz4.frame
from icontract import require
from functools import singledispatch
from ...types.optimization import (PolynomialObjective, Constraints,
                                   BinaryProblem, BinaryResults,
                                   BruteOptimizeResult)


def ndarray_to_dict(x: np.ndarray):
    # from https://stackoverflow.com/questions/30698004/how-can-i-serialize-a-numpy-array-while-preserving-matrix-dimensions
    if x is None:
        return None
    else:
        if isinstance(x, list) or isinstance(x, tuple):
            x = np.array(x)
        b = x.tobytes()
        Compression_threshold = 1024
        if len(b) > Compression_threshold:
            b = lz4.frame.compress(b)
            compression = 'lz4'
        else:
            compression = 'none'
        return dict(ndarray=base64.b64encode(b).decode('utf-8'),
                    compression=compression,
                    dtype=x.dtype.str,
                    shape=x.shape)


def dict_to_ndarray(d: dict):
    if d is None:
        return None
    else:
        b = base64.b64decode(d['ndarray'])
        if d['compression'] == 'lz4':
            b = lz4.frame.decompress(b)
        return np.frombuffer(
            b,
            dtype=np.dtype(d['dtype']),
        ).reshape(d['shape'])


@require(lambda v: np.isscalar(v))
def scalar_to_dict(v, dtype=None) -> Dict:
    """
    Hack for individual numerical scalars to serializable form.
    This is done by casting them to complex128, which is byte-wasteful
    in some ways, and into an array, which is byte-wasteful in other
    ways, but at least preserves accuracy to a degree
    """
    if dtype is None:
        dtype = np.complex128 if np.iscomplex(v) else np.float64
    result = ndarray_to_dict(np.array([v], dtype=dtype))
    result['is_scalar'] = True
    return result


@require(lambda d: d.get('is_scalar', False) is True)
def dict_to_scalar(d: Dict):
    return dict_to_ndarray(d)[0]


@require(lambda x: isinstance(x, np.ndarray) or np.isscalar(x))
def numeric_to_dict(x):
    """
    A more generic transformation in the case that x represents either
    an array or a scalar
    """
    return scalar_to_dict(x) if np.isscalar(x) else ndarray_to_dict(x)


@require(lambda x: isinstance(x, dict) and 'ndarray' in x)
def dict_to_numeric(x):
    """See numeric_to_dict
    """
    if x.get('is_scalar', False) is True:
        return dict_to_scalar(x)
    else:
        return dict_to_ndarray(x)


def string_to_int_tuple(s: str):
    term_strings = s.split(',')
    if term_strings[-1] == '':
        term_strings = term_strings[:-1]
    return tuple(map(int, term_strings))


def remap_q_indices_from_strings(q_old: dict) -> dict:
    q_new = {
        string_to_int_tuple(k[1:-1].strip(", ")): v
        for k, v in q_old.items()
    }
    return q_new


def remap_q_indices_to_strings(Q: dict) -> dict:
    return {str(k): v for k, v in Q.items()}


def complex_or_real_dtype_to_string(t: type):
    if t is None:
        result = None
    else:
        if np.isreal(t()) or np.iscomplex(t()):
            result = t.__name__
        else:
            raise NotImplementedError('dtypes must be complex or real')
    return result


def string_to_complex_or_real_dtype(s: str):
    if s is None:
        result = None
    else:
        t = np.dtype(s).type
        if np.isreal(t()) or np.iscomplex(t()):
            result = t
        else:
            raise NotImplementedError('dtypes must be complex or real')
    return result


@singledispatch
def to_wire(x):
    """For complex types, this dispatches to create a JSON-compatible dict
    """
    raise NotImplementedError("Unsupported Type")


@to_wire.register(PolynomialObjective)
def _(x):
    result = x.dict()
    result['polynomial'] = remap_q_indices_to_strings(result['polynomial'])
    return result


def polynomial_objective_from_wire(d: dict):
    remapped_dict = d.copy()

    remapped_dict['polynomial'] = remap_q_indices_from_strings(d['polynomial'])
    return PolynomialObjective(**remapped_dict)


@to_wire.register(Constraints)
def _(x):
    result = x.dict()
    result['constraints'] = {
        k: [to_wire(x) for x in v]
        for k, v in x.dict()['constraints'].items()
    }
    return result


def constraints_from_wire(d: dict):
    remapped_dict = d.copy()
    remapped_dict['constraints'] = {
        k: [polynomial_objective_from_wire(x) for x in v]
        for k, v in d['constraints'].items()
    }

    return Constraints(**remapped_dict)


@to_wire.register(BinaryProblem)
def _(x):
    result = x.dict()
    result['Q_dict'] = remap_q_indices_to_strings(result['Q_dict'].polynomial)

    return result


def binary_problem_from_wire(d: dict):
    remapped_dict = d.copy()
    remapped_dict['Q_dict'] = remap_q_indices_from_strings(d['Q_dict'])
    return BinaryProblem.from_q(remapped_dict['Q_dict'])


@to_wire.register(BinaryResults)
def _(x):
    result = x.dict()
    result['original_problem'] = to_wire(x.original_problem)
    result['backend_data_start'] = {
        k: v
        for k, v in result['backend_data_start'].items()
        if k not in ('Q', 'Q_array', 'split_to_full_map_array')
    }
    return result


def binary_results_from_wire(d: dict):
    remapped_dict = d.copy()
    remapped_dict['original_problem'] = binary_problem_from_wire(
        d['original_problem'])
    return BinaryResults(**remapped_dict)


def brute_optimize_result_from_wire(d: dict):
    return BruteOptimizeResult(**d)
