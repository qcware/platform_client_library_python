from qcware.serialization.transforms import ndarray_to_dict, dict_to_ndarray
from qcware.serialization.transforms.helpers import (
    scalar_to_dict,
    dict_to_scalar,
    numeric_to_dict,
    dict_to_numeric,
)
import numpy as np
from hypothesis.strategies import floats, one_of
from hypothesis import given
from hypothesis.extra.numpy import arrays, array_shapes

Simple_floats = floats(allow_nan=False, allow_infinity=False)
Simple_arrays = arrays(
    dtype=np.float64,
    shape=array_shapes(),
    elements=floats(allow_nan=False, allow_infinity=False),
)


@given(Simple_floats)
def test_serialize_scalars(x):
    assert dict_to_scalar(scalar_to_dict(x)) == x


@given(Simple_arrays)
def test_serialize_arrays(x):
    assert (dict_to_ndarray(ndarray_to_dict(x)) == x).all()


@given(one_of(Simple_floats, Simple_arrays))
def test_serialize_numeric(x):
    result = dict_to_numeric(numeric_to_dict(x))
    if np.isscalar(x):
        assert result == x
    else:
        assert (result == x).all()


def test():
    x1 = np.random.rand(10)
    d1 = ndarray_to_dict(x1)
    assert d1["compression"] == "none"
    assert (dict_to_ndarray(d1) == x1).all()

    x2 = np.random.rand(2048)
    d2 = ndarray_to_dict(x2)
    assert d2["compression"] == "lz4"
    assert (dict_to_ndarray(d2) == x2).all()
