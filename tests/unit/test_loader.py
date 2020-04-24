from qcware.qio import loader
from qcware.circuits import run_statevector
import numpy as np


def test_loader():
    x = np.random.rand(4)
    x = x / np.linalg.norm(x)

    circ = loader(data=x, mode='optimized')
    state = np.real(run_statevector(backend='classical/simulator', circuit=circ))
    indices = [10,9,6,5]
    reduced_vec = state[indices]
    eps = np.linalg.norm(np.abs(np.array(x) - np.abs(reduced_vec)))
    assert eps <= 1e2

