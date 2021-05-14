import qcware
import os
import pytest
import qubovert as qv
from qcware.types.optimization import BinaryProblem
from qcware.circuits.quasar_backend import QuasarBackend
from qcware.types.optimization import PolynomialObjective
import quasar
QCWARE_API_KEY = os.environ['QCWARE_API_KEY']
QCWARE_HOST = os.environ['QCWARE_HOST']

# test temporarily removed since the BinaryProblem class should check this
# def test_solve_binary_with_brute_force():
#     Q = {(0, 0): "POTATO"}

def test_solve_binary_with_brute_force():
    Q = {(0, 0): 1, (1, 1): 1, (0, 1): -2, (2, 2): -2, (3, 3): -4, (3, 2): -6}
#    Q = {(0, 0): "POTATO"}
    qubo = PolynomialObjective(
        polynomial=Q,
        num_variables=4,
        domain='boolean'
    )
    problem = BinaryProblem(Q_dict=qubo)

    # run_backend_method is a sort of special case because it nests kwargs, so let's
    # just make sure
    with pytest.raises(qcware.exceptions.ApiCallExecutionError):
        backend = QuasarBackend('qcware/cpu_simulator')
        q = quasar.Circuit()
        q.H(0).CX(0, 1)
        backend.run_measurement(circuit=q, nqubit=-42)

    # if there's a problem in the dispatcher (no backend), task_failure should handle that too
    with pytest.raises(qcware.exceptions.ApiCallFailedError):
        result = qcware.optimization.optimize_binary(Q=problem, backend="POTATO")
