import qcware
import os
import pytest
from qcware.circuits.quasar_backend import QuasarBackend
import quasar
QCWARE_API_KEY = os.environ['QCWARE_API_KEY']
QCWARE_HOST = os.environ['QCWARE_HOST']


def test_solve_binary_with_brute_force():
    Q = {(0, 0): "POTATO"}

    # if there's a problem past the dispatcher, task_failure should handle it
    with pytest.raises(qcware.exceptions.ApiCallExecutionError):
        result = qcware.optimization.solve_binary(Q=Q, backend="qcware/cpu")

    # run_backend_method is a sort of special case because it nests kwargs, so let's
    # just make sure
    with pytest.raises(qcware.exceptions.ApiCallExecutionError):
        backend = QuasarBackend('qcware/cpu_simulator')
        q = quasar.Circuit()
        q.H(0).CX(0, 1)
        backend.run_measurement(circuit=q, nqubit=-42)

    # if there's a problem in the dispatcher (no backend), task_failure should handle that too
    with pytest.raises(qcware.exceptions.ApiCallFailedError):
        result = qcware.optimization.solve_binary(Q=Q, backend="POTATO")
