import os
from pprint import pprint

import numpy as np
import pytest
import qcware
import quasar
from qcware.forge.circuits.quasar_backend import QuasarBackend
from qcware.forge.exceptions import ApiCallExecutionError


@pytest.mark.parametrize(
    "backend,expected",
    [
        ("qcware/cpu_simulator", True),
        ("qcware/gpu_simulator", True),
        ("ibm/simulator", True),
        ("awsbraket/sv1", False),
        ("awsbraket/tn1", False),
    ],
)
def test_has_run_statevector(backend: str, expected: bool):
    b = QuasarBackend(backend)
    assert b.has_run_statevector() is expected


@pytest.mark.parametrize(
    "backend,expected",
    [
        ("qcware/cpu_simulator", True),
        ("qcware/gpu_simulator", True),
        ("ibm/simulator", True),
        ("awsbraket/sv1", False),
        ("awsbraket/tn1", False),
    ],
)
def test_has_statevector_input(backend: str, expected: bool):
    b = QuasarBackend(backend)
    assert b.has_statevector_input() is expected


@pytest.mark.parametrize(
    "backend",
    [
        ("qcware/cpu_simulator"),
        ("qcware/gpu_simulator"),
        ("ibm/simulator"),
        ("ibmq:ibmq_qasm_simulator"),
        ("awsbraket/sv1"),
        ("awsbraket/tn1"),
        #        ("awsbraket/rigetti_aspen_11")
        #        ("awsbraket/rigetti_aspen_m_1")
    ],
)
def test_run_measurement(backend):
    q = quasar.Circuit()
    # We'll use a bell-pair with an additional NOT to try and
    # flush out bit-ordering issues
    q.H(0).CX(0, 1).X(2)
    b = QuasarBackend(backend)
    result = b.run_measurement(circuit=q, nmeasurement=100)
    assert isinstance(result, quasar.ProbabilityHistogram)
    assert isinstance(result.histogram, dict)
    assert 1 in result.histogram
    assert 7 in result.histogram
    # yeah, pretty fuzzy but I'll take it; this is more or less a smoke test
    assert abs(result.histogram[1] - 0.5) < 0.2
    assert abs(result.histogram[7] - 0.5) < 0.2


@pytest.mark.parametrize(
    "backend",
    (
        ("awsbraket/ionq"),
        ("awsbraket/rigetti_aspen_11"),
        ("awsbraket/rigetti_aspen_m_1"),
    ),
)
def test_smoke_backend_exception(backend):
    """This is a 'smoke test' for having a NotImplementedError from a
    backend. Accuracy doesn't matter here so long as the call gives a
    NotImplementedError (since we call run_statevector on a backend without it)
    """
    q = quasar.Circuit()
    q.H(0).CX(0, 1)
    b = QuasarBackend(backend)
    try:
        result = b.run_statevector(circuit=q)
    except ApiCallExecutionError as e:
        assert str(e) == "NotImplementedError: "
        return
    assert False


@pytest.mark.parametrize(
    "backend",
    (
        ("awsbraket/ionq"),
        ("awsbraket/rigetti_aspen_11"),
        ("awsbraket/rigetti_aspen_m_1"),
    ),
)
def test_smoke_rescheduled_backends(backend):
    """This is another 'smoke test' for the backends that can be rescheduled; they
    need to either raise a rescheduled exception or run
    """
    q = quasar.Circuit()
    q.H(0).CX(0, 1)
    b = QuasarBackend(backend)
    result = b.run_measurement(circuit=q, nmeasurement=10)


@pytest.mark.parametrize(
    "backend",
    [
        ("qcware/cpu_simulator"),
        ("qcware/gpu_simulator"),
        #        ("awsbraket/rigetti_aspen_11")
        #        ("awsbraket/rigetti_aspen_m_1")
    ],
)
def test_run_statevector(backend):
    q = quasar.Circuit()
    q.H(0).CX(0, 1)
    b = QuasarBackend(backend)
    result = b.run_statevector(circuit=q)
    val = complex(np.sqrt(2) / 2, 0)
    assert np.allclose(result, [val, 0, 0, val])
