from qcware.util.transforms import ndarray_to_dict, dict_to_ndarray
import numpy as np


def test():
    x = np.random.rand(10)
    assert (dict_to_ndarray(ndarray_to_dict(x)) == x).all()
