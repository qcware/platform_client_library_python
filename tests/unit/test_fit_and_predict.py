import qcware
import numpy as np
import pytest
import pprint
from qcware.qml import fit_and_predict


@pytest.mark.parametrize("backend", [
    'qcware/cpu_simulator', 'qcware/gpu_simulator', 'ibm/simulator',
    'awsbraket/sv1', 'awsbraket/tn1'
])
def test_fit_and_predict(backend: str):
    X = np.array([[-1, -2, 2, -1], [-1, -1, 2, 0], [2, 1, -2, -1],
                  [1, 2, 0, -1]])
    y = np.array([0, 0, 1, 1])
    try:
        with qcware.config.additional_config(client_timeout=5 * 60):
            result = fit_and_predict(X=X,
                                     y=y,
                                     model="QNearestCentroid",
                                     backend=backend,
                                     parameters={'num_measurements': 100})
    except Exception as e:
        print(e)
        print(type(e.traceback))
        print(type(eval(e.traceback)))
        print("".join(eval(e.traceback)))
    assert (result == [0, 0, 1, 1]).all()
