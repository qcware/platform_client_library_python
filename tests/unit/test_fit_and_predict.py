import pprint

import numpy as np
import pytest
import qcware.forge
from qcware.forge.qml import fit_and_predict
from qcware.forge.exceptions import ApiCallExecutionError


@pytest.mark.parametrize(
    "backend",
    [
        "qcware/cpu_simulator",
        "qcware/gpu_simulator",
        "ibm/simulator",
        "ibmq:ibmq_qasm_simulator",
        "awsbraket/sv1",
        "awsbraket/tn1",
    ],
)
def test_fit_and_predict(backend: str):
    X = np.array([[-1, -2], [-1, -1], [2, 1], [1, 2]])
    y = np.array([0, 0, 1, 1])
    try:
        with qcware.forge.config.additional_config(client_timeout=5 * 60):
            result = fit_and_predict(
                X=X,
                y=y,
                model="QNearestCentroid",
                backend=backend,
                parameters={"num_measurements": 1},
            )
    except ApiCallExecutionError as e:
        print(e)
        print(type(e.traceback))
        print(type(eval(e.traceback)))
        print("".join(eval(e.traceback)))
    # smoke test here in the client
    assert set(result).issubset({0, 1})
    assert len(result) == 4
    # assert (result == [0, 0, 1, 1]).all()
