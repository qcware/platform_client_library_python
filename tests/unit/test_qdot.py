from qcware.qutils import qdot
import numpy as np
import pytest

# the tricky thing here for serialization is to make
# sure that the types come out right.  For dot,
# we have
# scalar -> scalar -> scalar
# [m]->[m]->scalar
# m rows, n columns
# [mxn]->[n]->[m]
# [m]->[mxn]->[n]
# otherwise throw an exception


# I really wanted to use hypothesis here, but the fact is it
# takes too long to send it over the wire, so we'll do case studies
# for each
@pytest.mark.parametrize(('x,y'), [
    (np.array([5]), np.array([5])),
    (np.array([[5,4,3],[2,1,0]]), np.array([8,7,6])),
])
def test_qdot(x, y):

    result = qdot(x, y)
    numpy_result = np.dot(x, y)
    if np.isscalar(numpy_result):
        assert np.isscalar(result)
    elif isinstance(numpy_result, np.ndarray):
        assert isinstance(result,
                          np.ndarray) and result.shape == numpy_result.shape
    assert np.allclose(result, numpy_result)
