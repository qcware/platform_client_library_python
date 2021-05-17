import time
import qcware
import pytest
import qubovert as qv
from qcware.types.optimization import BinaryProblem
from qcware.types.optimization import PolynomialObjective

def generate_problem():
    Q = {(0, 0): 1, (1, 1): 1, (0, 1): -2, (2, 2): -2, (3, 3): -4, (3, 2): -6}

    qubo = PolynomialObjective(
        polynomial=Q,
        num_variables=4,
        domain='boolean'
    )
    problem = BinaryProblem(objective=qubo)
    return problem


def test_timeout_with_solve_binary():
    old_timeout = qcware.config.client_timeout()
    qcware.config.set_client_timeout(0)
    old_server_timeout = qcware.config.server_timeout()
    qcware.config.set_server_timeout(0)

    with pytest.raises(qcware.exceptions.ApiTimeoutError):
        sol = qcware.optimization.find_optimal_qaoa_angles(
            generate_problem().objective,
            num_evals=100,
            num_min_vals=10,
            fastmath_flag_in=True,
            precision=30)
        print(sol)

    qcware.config.set_client_timeout(old_timeout)
    qcware.config.set_server_timeout(old_server_timeout)


def test_retrieve_result_with_timeout():
    old_timeout = qcware.config.client_timeout()
    qcware.config.set_client_timeout(0)
    old_server_timeout = qcware.config.server_timeout()
    qcware.config.set_server_timeout(0)

    try:
        result = qcware.optimization.optimize_binary(
            instance=generate_problem(), backend='qcware/cpu')
    except qcware.exceptions.ApiTimeoutError as e:
        # should change this to use batching API
        time.sleep(8)
        result = qcware.api_calls.retrieve_result(e.api_call_info['uid'])
        result_vectors = [x[1] for x in result.return_results()]
        assert ([0, 0, 1, 1] in result_vectors)
        assert ([1, 1, 1, 1] in result_vectors)
    qcware.config.set_client_timeout(old_timeout)
    qcware.config.set_server_timeout(old_server_timeout)


@pytest.mark.asyncio
async def test_async():
    old_timeout = qcware.config.client_timeout()
    qcware.config.set_client_timeout(0)
    old_server_timeout = qcware.config.server_timeout()
    qcware.config.set_server_timeout(0)

    result = await qcware.optimization.optimize_binary.call_async(
        instance=generate_problem(),
        backend='qcware/cpu')
    result_vectors = [x[1] for x in result.return_results()]
    assert ([0, 0, 1, 1] in result_vectors)
    assert ([1, 1, 1, 1] in result_vectors)

    qcware.config.set_client_timeout(old_timeout)
    qcware.config.set_server_timeout(old_server_timeout)
