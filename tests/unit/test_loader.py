from qcware.forge.qio import loader
from qcware.forge.circuits.quasar_backend import QuasarBackend
import numpy as np
import pytest


def test_loader():
    x = np.random.rand(4)
    x = x / np.linalg.norm(x)

    circ = loader(data=x, mode="optimized")
    backend = QuasarBackend("qcware/cpu_simulator")
    state = np.real(backend.run_statevector(circuit=circ))
    indices = [10, 9, 6, 5]
    reduced_vec = state[indices]
    eps = np.linalg.norm(np.abs(np.array(x) - np.abs(reduced_vec)))
    assert eps <= 1e-2

@pytest.mark.parametrize(
    "kwparams",
    [
        {"mode": "parallel"},
        {"mode": "optimized"},
        {"mode": "optimized", "opt_shape": (1, 4)},
        {"mode": "diagonal"},
        {"mode": "semi-diagonal"},
        {"mode": "semi-diagonal-middle"},
    ]
)
def test_loader_with_indices(kwparams):
    x = np.random.rand(4)
    x = x / np.linalg.norm(x)
    backend = QuasarBackend("qcware/cpu_simulator")

    circ, indices = loader(data=x, **kwparams, return_statevector_indices=True)
    state = np.real(backend.run_statevector(circuit=circ))
    reduced_vec = state[indices]
    eps = np.linalg.norm(np.abs(np.array(x) - np.abs(reduced_vec)))
    assert eps <= 1e-2
