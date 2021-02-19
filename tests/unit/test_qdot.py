from qcware.qio import qdot
import numpy as np


def test_qdot():
    x = np.random.rand(4)
    y = np.random.rand(4)
    x = x / np.linalg.norm(x)
    y = y / np.linalg.norm(y)

    result = qdot(x, y)

    assert np.allclose(result, np.dot(x,y))
