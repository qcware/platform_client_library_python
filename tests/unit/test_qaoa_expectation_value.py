from qcware.types.optimization import PolynomialObjective, BinaryProblem

from qcware.forge.optimization import qaoa_expectation_value
from qcware.forge.api_calls import status, retrieve_result
import time
import pytest
import numpy as np

Num_samples = 512

simulation_backends = (
    ("qcware/cpu", None),
    ("qcware/gpu", None),
    ("qcware/cpu_simulator", None),
    ("qcware/gpu_simulator", None),
    ("awsbraket/sv1", Num_samples),
    ("ibm/simulator", Num_samples),
)


def pubo_example(num_variables: int = 4):
    poly = {
        (0,): -3,
        (0, 1): 2,
        (0, 2): np.random.randint(-5, 5),
        (0, 3): 2,
        (1,): -3,
        (1, 2): 2,
        (1, 3): 2,
        (2,): np.random.randint(-5, 5),
        (2, 3): 2,
        (3,): -2,
        (0, 1, 3): np.random.randint(-1, 1),
        (): 7,
    }
    poly = PolynomialObjective(
        polynomial=poly,
        num_variables=num_variables,
        domain=np.random.choice(["spin", "boolean"]),
    )
    return BinaryProblem(objective=poly)


# This test is more thorough than it looks since the qcware/cpu algorithm
# is very different from the simulator backends.
@pytest.mark.parametrize(("backend", "num_samples"), simulation_backends)
def test_qaoa_expectation_value_against_cpu_emulate(backend, num_samples):

    instance = pubo_example()
    qaoa_p = np.random.choice([1, 2])
    beta = np.random.random(qaoa_p)
    gamma = np.random.random(qaoa_p)

    qcware_cpu_value = qaoa_expectation_value(
        problem_instance=instance, beta=beta, gamma=gamma, backend="qcware/cpu"
    )
    other_value = qaoa_expectation_value(
        problem_instance=instance,
        beta=beta,
        gamma=gamma,
        num_samples=num_samples,
        backend=backend,
    )
    assert np.isclose(other_value, qcware_cpu_value, rtol=0.2)


# This just checks to see if we can run with samples.
@pytest.mark.skip(
    "Calling a backend with num_samples which can't handle them can result in an error (qcware/cpu)"
)
@pytest.mark.parametrize(("backend", "num_samples"), simulation_backends)
def test_qaoa_expectation_value_sampled(backend, num_samples):
    instance = pubo_example()
    qaoa_p = np.random.choice([1, 2])
    beta = np.random.random(qaoa_p)
    gamma = np.random.random(qaoa_p)

    qaoa_expectation_value(
        problem_instance=instance,
        beta=beta,
        gamma=gamma,
        num_samples=128,
        backend=backend,
    )


@pytest.mark.parametrize("backend", ["ibmq:ibmq_qasm_simulator"])
def test_qaoa_expectation_value_ibmq(backend):
    instance = pubo_example()
    beta = np.array([5.284])
    gamma = np.array([-1.38])
    job_id = qaoa_expectation_value.submit(
        problem_instance=instance,
        beta=beta,
        gamma=gamma,
        num_samples=128,
        backend=backend,
    )
    job_status = status(job_id)
    while job_status["status"] == "open":
        time.sleep(0.5)
        job_status = status(job_id)

    retrieve_result(job_id)
