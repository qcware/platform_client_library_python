from qcware.types import PolynomialObjective, BinaryProblem

from qcware.optimization import qaoa_expectation_value
from qcware.api_calls import status, retrieve_result
import time
import pytest
import numpy as np

simulation_backends = (
    'qcware/cpu',
    'qcware/gpu',
    'qcware/cpu_simulator',
    'qcware/gpu_simulator',
    'awsbraket/sv1',
    'ibm/simulator',
)


def pubo_example(num_variables: int = 4):
    poly = {
        (0, ): -3,
        (0, 1): 2,
        (0, 2): np.random.randint(-5, 5),
        (0, 3): 2,
        (1, ): -3,
        (1, 2): 2,
        (1, 3): 2,
        (2, ): np.random.randint(-5, 5),
        (2, 3): 2,
        (3, ): -2,
        (0, 1, 3): np.random.randint(-1, 1),
        (): 7
    }
    poly = PolynomialObjective(
        polynomial=poly,
        num_variables=num_variables,
        domain=np.random.choice('spin', 'boolean')
    )
    return BinaryProblem(objective=poly)


# This test is more thorough than it looks since the qcware/cpu algorithm
# is very different from the simulator backends.
def test_qaoa_expectation_value_against_cpu_emulate():

    for backend in simulation_backends:
        instance = pubo_example()
        qaoa_p = np.random.choice([1, 2])
        beta = np.random.random(qaoa_p)
        gamma = np.random.random(qaoa_p)

        qcware_cpu_value = qaoa_expectation_value(
            problem_instance=instance,
            beta=beta,
            gamma=gamma,
            backend='qcware/cpu'
        )
        other_value = qaoa_expectation_value(
            problem_instance=instance,
            beta=beta,
            gamma=gamma,
            backend=backend
        )
        assert np.isclose(other_value, qcware_cpu_value)


# This just checks to see if we can run with samples.
def test_qaoa_expectation_value_sampled():
    for backend in simulation_backends:
        instance = pubo_example()
        qaoa_p = np.random.choice([1, 2])
        beta = np.random.random(qaoa_p)
        gamma = np.random.random(qaoa_p)

        qaoa_expectation_value(
            problem_instance=instance,
            beta=beta,
            gamma=gamma,
            num_samples=128,
            backend=backend
        )


@pytest.mark.parametrize('backend', ['ibmq:ibmq_qasm_simulator'])
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
    while job_status['status'] == 'open':
        time.sleep(0.5)
        job_status = status(job_id)

    retrieve_result(job_id)
