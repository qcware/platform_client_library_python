import time
import pytest
import qubovert as qv
from qcware.types.optimization import BinaryProblem
from qcware.types.optimization import PolynomialObjective
from qcware import forge


def generate_problem():
    Q = {(0, 0): 1, (1, 1): 1, (0, 1): -2, (2, 2): -2, (3, 3): -4, (3, 2): -6}

    qubo = PolynomialObjective(polynomial=Q, num_variables=4, domain="boolean")
    problem = BinaryProblem(objective=qubo)
    return problem


def test_timeout_with_solve_binary():
    old_timeout = forge.config.client_timeout()
    forge.config.set_client_timeout(0)
    old_server_timeout = forge.config.server_timeout()
    forge.config.set_server_timeout(0)

    with pytest.raises(forge.exceptions.ApiTimeoutError):
        sol = forge.optimization.find_optimal_qaoa_angles(
            generate_problem().objective,
            num_evals=100,
            num_min_vals=10,
            fastmath_flag_in=True,
            precision=30,
        )
        print(sol)

    forge.config.set_client_timeout(old_timeout)
    forge.config.set_server_timeout(old_server_timeout)


def test_retrieve_result_with_timeout():
    old_timeout = forge.config.client_timeout()
    forge.config.set_client_timeout(0)
    old_server_timeout = forge.config.server_timeout()
    forge.config.set_server_timeout(0)

    try:
        result = forge.optimization.optimize_binary(
            instance=generate_problem(), backend="qcware/cpu"
        )
    except forge.exceptions.ApiTimeoutError as e:
        call_id = e.api_call_info["uid"]
        start = time.perf_counter()
        # 30s timeouts
        timeout = 60
        while ((time.perf_counter() - start) < timeout) and forge.api_calls.status(
            call_id
        )["status"] == "open":
            time.sleep(1)
        assert forge.api_calls.status(call_id)["status"] == "success"
        result = forge.api_calls.retrieve_result(call_id)
        result_vectors = {x.bitstring for x in result.samples}
        assert (0, 0, 1, 1) in result_vectors
        assert (1, 1, 1, 1) in result_vectors
    forge.config.set_client_timeout(old_timeout)
    forge.config.set_server_timeout(old_server_timeout)


@pytest.mark.asyncio
async def test_async():
    old_timeout = forge.config.client_timeout()
    forge.config.set_client_timeout(0)
    old_server_timeout = forge.config.server_timeout()
    forge.config.set_server_timeout(0)

    result = await forge.optimization.optimize_binary.call_async(
        instance=generate_problem(), backend="qcware/cpu"
    )
    result_vectors = {x.bitstring for x in result.samples}
    assert (0, 0, 1, 1) in result_vectors
    assert (1, 1, 1, 1) in result_vectors

    forge.config.set_client_timeout(old_timeout)
    forge.config.set_server_timeout(old_server_timeout)
