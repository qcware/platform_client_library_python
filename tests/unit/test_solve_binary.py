import qcware
import pytest


@pytest.mark.parametrize("backend", (
    'classical',
    'dwave',
))
def test_solve_binary(backend):
    Q = {(0, 0): 1, (1, 1): 1, (0, 1): -2, (2, 2): -2, (3, 3): -4, (3, 2): -5}

    result = qcware.optimization.solve_binary(Q=Q, backend=backend)
    assert (result['solution'] == [0, 0, 1, 1])


@pytest.mark.parametrize("backend", (
    'classical/simulator',
))
def test_solve_binary(backend):
    Q = {(0, 0): 1, (1, 1): 1, (0, 1): -2, (2, 2): -2, (3, 3): -4, (3, 2): -5}

    result = qcware.optimization.solve_binary(Q=Q, backend=backend)
    assert (result['solution'] == [0, 0, 1, 1]
            or result['solution'] == [1, 1, 1, 1])
