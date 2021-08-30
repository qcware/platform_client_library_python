import base64
from functools import singledispatch
from typing import Dict

import lz4.frame
import numpy as np
from icontract import require
from qcware.types.optimization import (
    BinaryProblem,
    BruteOptimizeResult,
    Constraints,
    PolynomialObjective,
)
from qcware.types.optimization.results.results_types import BinaryResults, Sample


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
            compression = "lz4"
        else:
            compression = "none"
        return dict(
            ndarray=base64.b64encode(b).decode("utf-8"),
            compression=compression,
            dtype=x.dtype.str,
            shape=x.shape,
        )


def dict_to_ndarray(d: dict):
    if d is None:
        return None
    else:
        b = base64.b64decode(d["ndarray"])
        if d["compression"] == "lz4":
            b = lz4.frame.decompress(b)
        return np.frombuffer(
            b,
            dtype=np.dtype(d["dtype"]),
        ).reshape(d["shape"])


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
    result["is_scalar"] = True
    return result


@require(lambda d: d.get("is_scalar", False) is True)
def dict_to_scalar(d: Dict):
    return dict_to_ndarray(d)[0]


@require(lambda x: isinstance(x, np.ndarray) or np.isscalar(x))
def numeric_to_dict(x):
    """
    A more generic transformation in the case that x represents either
    an array or a scalar
    """
    return scalar_to_dict(x) if np.isscalar(x) else ndarray_to_dict(x)


@require(lambda x: isinstance(x, dict) and "ndarray" in x)
def dict_to_numeric(x):
    """See numeric_to_dict"""
    if x.get("is_scalar", False) is True:
        return dict_to_scalar(x)
    else:
        return dict_to_ndarray(x)


def string_to_int_tuple(s: str):
    term_strings = s.split(",")
    if term_strings[-1] == "":
        term_strings = term_strings[:-1]
    return tuple(map(int, term_strings))


def remap_q_indices_from_strings(q_old: dict) -> dict:
    q_new = {string_to_int_tuple(k[1:-1].strip(", ")): v for k, v in q_old.items()}
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
            raise NotImplementedError("dtypes must be complex or real")
    return result


def string_to_complex_or_real_dtype(s: str):
    if s is None:
        result = None
    else:
        t = np.dtype(s).type
        if np.isreal(t()) or np.iscomplex(t()):
            result = t
        else:
            raise NotImplementedError("dtypes must be complex or real")
    return result


@singledispatch
def to_wire(x):
    """For complex types, this dispatches to create a JSON-compatible dict"""
    raise NotImplementedError("Unsupported Type")


@to_wire.register(PolynomialObjective)
def polynomial_objective_to_wire(x):
    result = x.dict()
    result["polynomial"] = remap_q_indices_to_strings(result["polynomial"])
    result["variable_name_mapping"] = {
        str(k): v for k, v in result["variable_name_mapping"].items()
    }
    return result


def polynomial_objective_from_wire(d: dict):
    remapped_dict = d.copy()

    remapped_dict["polynomial"] = remap_q_indices_from_strings(d["polynomial"])
    remapped_dict["variable_name_mapping"] = {
        int(k): v for k, v in remapped_dict["variable_name_mapping"].items()
    }
    return PolynomialObjective(**remapped_dict)


@to_wire.register(Constraints)
def constraints_to_wire(x):
    result = x.dict()
    result["constraints"] = {
        k: [to_wire(x) for x in v] for k, v in x.dict()["constraints"].items()
    }
    return result


def constraints_from_wire(d: dict):
    remapped_dict = d.copy()
    remapped_dict["constraints"] = {
        k: [polynomial_objective_from_wire(x) for x in v]
        for k, v in d["constraints"].items()
    }

    return Constraints(**remapped_dict)


@to_wire.register(BinaryProblem)
def binary_problem_to_wire(x):
    result = x.dict()
    result["objective"] = to_wire(result["objective"])
    result["constraints"] = (
        to_wire(result["constraints"]) if result["constraints"] is not None else None
    )
    return result


def binary_problem_from_wire(d: dict):
    remapped_dict = d.copy()
    remapped_dict["objective"] = polynomial_objective_from_wire(d["objective"])
    remapped_dict["constraints"] = (
        constraints_from_wire(remapped_dict["constraints"])
        if remapped_dict["constraints"] is not None
        else None
    )
    return BinaryProblem(**remapped_dict)


@to_wire.register(BinaryResults)
def _(x):
    result = x.dict()
    result["original_problem"] = to_wire(x.original_problem)
    result["task_metadata"] = {
        k: v
        for k, v in result["task_metadata"].items()
        if k not in ("Q", "Q_array", "split_to_full_map_array", "instance")
    }
    return result


def binary_results_from_wire(d: dict):
    remapped_dict = d.copy()
    remapped_dict["sample_ordered_dict"] = {
        k: Sample(**v) for k, v in remapped_dict["sample_ordered_dict"].items()
    }
    remapped_dict["original_problem"] = binary_problem_from_wire(d["original_problem"])
    return BinaryResults(**remapped_dict)


def brute_optimize_result_from_wire(d: dict):
    return BruteOptimizeResult(**d)
