import qcware
import numpy as np
import pytest
import pprint

@pytest.mark.parametrize("backend", ['qcware/cpu_simulator', 'qcware/gpu_simulator', 'ibm/simulator', 'awsbraket/sv1'])
def test_fit_and_predict(backend: str):
    X = np.array([[-1, -2, 2, -1], [-1, -1, 2, 0], [2, 1, -2, -1],
                  [1, 2, 0, -1]])
    y = np.array([0, 0, 1, 1])
    try:
        result = qcware.qml.fit_and_predict(X=X,
                                            y=y,
                                            model="QNearestCentroid",
                                            backend=backend)
    except Exception as e:
        print(e)
        print(type(e.traceback))
        print(type(eval(e.traceback)))
        print("".join(eval(e.traceback)))
    assert (result == [0, 0, 1, 1]).all()
