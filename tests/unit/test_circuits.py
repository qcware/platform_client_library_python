import qcware
import quasar
import os
import pytest
from qcware.circuits.quasar_backend import QuasarBackend
from pprint import pprint
import numpy as np


@pytest.mark.parametrize("backend,expected", [("qcware/cpu_simulator", True),
                                              ("awsbraket/sv1", False)])
def test_has_run_statevector(backend: str, expected: bool):
    b = QuasarBackend(backend)
    assert b.has_run_statevector() is expected


@pytest.mark.parametrize("backend,expected", [("qcware/cpu_simulator", True),
                                              ("awsbraket/sv1", False)])
def test_has_statevector_input(backend: str, expected: bool):
    b = QuasarBackend(backend)
    assert b.has_statevector_input() is expected


@pytest.mark.parametrize(
    "backend",
    [
        ("qcware/cpu_simulator"),
        ("awsbraket/sv1"),
        #        ("awsbraket/rigetti")
    ])
def test_run_measurement(backend):
    q = quasar.Circuit()
    q.H(0).CX(0, 1)
    b = QuasarBackend(backend)
    result = b.run_measurement(circuit=q)
    assert isinstance(result, quasar.ProbabilityHistogram)
    assert isinstance(result.histogram, dict)
    assert 0 in result.histogram
    # yeah, pretty fuzzy but I'll take it
    assert abs(result.histogram[0] - 0.5) < 0.05

    # now try with the backend
    backend = QuasarBackend(backend)
    result = backend.run_measurement(circuit=q)
    assert isinstance(result, quasar.ProbabilityHistogram)
    assert isinstance(result.histogram, dict)
    assert 0 in result.histogram
    # yeah, pretty fuzzy but I'll take it
    assert abs(result.histogram[0] - 0.5) < 0.05


@pytest.mark.parametrize(
    "backend",
    [
        ("qcware/cpu_simulator"),
        #        ("awsbraket/rigetti")
    ])
def test_run_statevector(backend):
    q = quasar.Circuit()
    q.H(0).CX(0, 1)
    b = QuasarBackend(backend)
    result = b.run_statevector(circuit=q)
    val = np.complex(np.sqrt(2) / 2, 0)
    assert np.allclose(result, [val, 0, 0, val])
