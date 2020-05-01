import qcware
import quasar
import os
import pytest
from qcware.circuits.quasar_backend import QuasarBackend


@pytest.mark.parametrize("backend,expected", [("classical/simulator", True),
                                              ("awsbraket/qs1", False)])
def test_has_run_statevector(backend: str, expected: bool):
    assert qcware.circuits.has_run_statevector(backend=backend) is expected


@pytest.mark.parametrize("backend,expected", [("classical/simulator", True),
                                              ("awsbraket/qs1", False)])
def test_has_statevector_input(backend: str, expected: bool):
    assert qcware.circuits.has_statevector_input(backend=backend) is expected


@pytest.mark.parametrize("backend", [("classical/simulator"),
                                     ("awsbraket/qs1")])
def test_run_measurement(backend):
    q = quasar.Circuit()
    q.H(0).CX(0, 1)
    result = qcware.circuits.run_measurement(circuit=q,
                                             backend=backend)
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

