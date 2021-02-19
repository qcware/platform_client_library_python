from qcware.qio import distance_estimation
import numpy as np


def test_distance_estimation():
    # purely smoke test
    x = np.random.rand(4)
    y = np.random.rand(4)
    x = x / np.linalg.norm(x)
    y = y / np.linalg.norm(y)

    result = distance_estimation(x, y)
    distance = np.linalg.norm(x - y)**2
    assert np.allclose(result, distance)
