from qcware.forge.qutils import distance_estimation
import numpy as np
import pytest

backends = (
    ("qcware/cpu_simulator", None),
    ("awsbraket/sv1", 100),
    ("awsbraket/tn1", 100),
    ("ibm/simulator", 100),
    ("qcware/gpu_simulator", None),
)


@pytest.mark.parametrize("backend, num_measurements", backends)
def test_distance_estimation(backend, num_measurements):
    # purely smoke test
    x = np.random.rand(4)
    y = np.random.rand(4)
    x = x / np.linalg.norm(x)
    y = y / np.linalg.norm(y)

    result = distance_estimation(
        x, y, backend=backend, num_measurements=num_measurements
    )
    distance = np.linalg.norm(x - y) ** 2
    # huge atol since this is mostly a smoke test
    assert np.allclose(result, distance, atol=2)
