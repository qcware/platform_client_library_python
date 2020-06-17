from qcware.util.transforms import ndarray_to_dict, dict_to_ndarray
import numpy as np


def test():
    x1 = np.random.rand(10)
    d1 = ndarray_to_dict(x1)
    assert (d1['compression'] == "none")
    assert (dict_to_ndarray(d1) == x1).all()

    x2 = np.random.rand(2048)
    d2 = ndarray_to_dict(x2)
    assert d2['compression'] == 'lz4'
    assert (dict_to_ndarray(d2) == x2).all()
