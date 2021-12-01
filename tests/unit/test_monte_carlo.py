from qcware.forge.montecarlo.nisqAE import (
    make_schedule,
    run_schedule,
    run_unary,
    compute_mle,
)
import numpy as np
import pytest
import quasar

# these are currently the very barest of smoke tests!


def test_make_schedule():
    result = make_schedule(epsilon=0.1, schedule_type="powerlaw")
    assert isinstance(result, list)


@pytest.mark.parametrize(
    "backend",
    ["qcware/cpu_simulator", "awsbraket/sv1", "ibm/simulator", "qcware/gpu_simulator"],
)
def test_run_schedule(backend):
    circuit = quasar.Circuit().H(0).CX(0, 1)
    schedule = make_schedule(epsilon=0.1, schedule_type="powerlaw")
    result = run_schedule(
        initial_circuit=circuit,
        iteration_circuit=circuit,
        target_qubits=[0],
        target_states=[1],
        schedule=schedule,
        backend=backend,
    )
    assert isinstance(result, list)


@pytest.mark.parametrize(
    "backend",
    ["qcware/cpu_simulator", "awsbraket/sv1", "ibm/simulator", "qcware/gpu_simulator"],
)
def test_run_unary(backend):
    circuit = quasar.Circuit().H(0).CX(0, 1)
    schedule = make_schedule(epsilon=0.1, schedule_type="powerlaw")
    result = run_unary(circuit=circuit, schedule=schedule, backend=backend)
    assert isinstance(result, list)


def test_compute_mle():
    circuit = quasar.Circuit().H(0).CX(0, 1)
    schedule = make_schedule(epsilon=0.1, schedule_type="powerlaw")
    counts = run_unary(
        circuit=circuit, schedule=schedule, backend="qcware/cpu_simulator"
    )
    result = compute_mle(counts, epsilon=0.1)
    assert isinstance(result, float)
