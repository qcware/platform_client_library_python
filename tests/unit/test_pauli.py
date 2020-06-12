import quasar
import time
import numpy as np
import qcware
from qcware.circuits.quasar_backend import QuasarBackend
import pytest


def generate_circuit(N: int) -> quasar.Circuit:
    gadget = quasar.Circuit().Ry(1).CZ(0, 1).Ry(1).CX(1, 0)
    circuit = quasar.Circuit().X(0)
    for I in range(N):
        circuit.add_gates(circuit=gadget, qubits=(I, I + 1))

    parameter_values = []
    for I in range(N):
        value = (1.0 - I / 17.0)
        parameter_values.append(+value)
        parameter_values.append(-value)
    circuit.set_parameter_values(parameter_values)
    return circuit


def generate_pauli(N: int) -> quasar.Pauli:
    I, X, Y, Z = quasar.Pauli.IXYZ()
    pauli = quasar.Pauli.zero()
    for k in range(N + 1):
        pauli += (k + 1) / 10.0 * Z[k]
    return pauli


@pytest.mark.parametrize(
    "backend",
    (
        'classical/simulator',
        #    'awsbraket/qs1')
    ))
def test_pauli(backend):
    N = 5
    circuit = generate_circuit(N)
    pauli = generate_pauli(N)
    vulcan_backend = QuasarBackend(backend)
    result = vulcan_backend.run_pauli_expectation_value_gradient(
        circuit=circuit, pauli=pauli, parameter_indices=[0, 1, 2, 3])
    assert np.isclose(
        result,
        np.array([0.68287656, -0.68287656, 0.37401749, -0.37401749],
                 dtype=np.complex128)).all()
