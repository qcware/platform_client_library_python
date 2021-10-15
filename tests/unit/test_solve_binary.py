import itertools

import pytest
import qcware.forge.optimization
from qcware.types.optimization import BinaryProblem


def sample_q():
    return {(0, 0): 1, (1, 1): 1, (0, 1): -2, (2, 2): -2, (3, 3): -4, (3, 2): -6}


def is_plausible_bitstring(bs, length):
    return set(bs).issubset({0, 1}) and len(bs) == length


@pytest.mark.parametrize(
    "backend",
    ("qcware/cpu", "dwave/2000q", "dwave_direct/2000q", "dwave/advantage")  # ,
    #                           'awsbraket/dwave/2000q', 'awsbraket/dwave/advantage')
)
def test_optimize_binary(backend):
    Q = sample_q()
    problem_instance = BinaryProblem.from_dict(Q)
    result = qcware.forge.optimization.optimize_binary(
        instance=problem_instance, backend=backend
    )
    assert result.original_problem.objective.dict() == problem_instance.objective.dict()
    result_bitstrings = {x.bitstring for x in result.samples}
    # this is just a smoke test now
    assert all([is_plausible_bitstring(bs, 4) for bs in result_bitstrings])
    # assert ((0, 0, 1, 1) in result_bitstrings) or ((1, 1, 1, 1) in result_bitstrings)


@pytest.mark.parametrize(
    "backend",
    (  # 'dwave/2000q', 'dwave/advantage',
        "dwave_direct/2000q",
        "dwave_direct/advantage",
    ),
)
def test_anneal_offsets(backend: str):
    """Smoke test for anneal offsets being at least callable; does not test their
    validity
    """
    Q = {(0, 0): 1, (1, 1): 1, (0, 1): -2}  # sample_q()

    result = qcware.forge.optimization.optimize_binary(
        instance=BinaryProblem.from_dict(Q),
        backend=backend,
        dwave_num_reads=1,
        dwave_anneal_offsets_delta=0.5,
    )


@pytest.mark.parametrize(
    "backend,nmeasurement",
    [
        ("qcware/cpu_simulator", None),
        ("qcware/gpu_simulator", None),
        ("awsbraket/sv1", 1000),
    ],
)
def test_optimize_binary_qaoa(backend: str, nmeasurement: int):
    Q = sample_q()

    result = qcware.forge.optimization.optimize_binary(
        instance=BinaryProblem.from_dict(Q),
        backend=backend,
        qaoa_nmeasurement=nmeasurement,
        qaoa_optimizer="analytical",
    )
    result_bitstrings = {x.bitstring for x in result.samples}
    assert all([is_plausible_bitstring(bs, 4) for bs in result_bitstrings])
    # assert ((0, 0, 1, 1) in result_bitstrings) or ((1, 1, 1, 1) in result_bitstrings)


@pytest.mark.parametrize(
    "optimizer, backend",
    itertools.product(
        ("COBYLA", "bounded_Powell", "analytical"),
        ("qcware/cpu_simulator", "qcware/gpu_simulator"),
    ),
)
def test_various_qaoa_optimizers(optimizer, backend):
    Q = sample_q()
    result = qcware.forge.optimization.optimize_binary(
        instance=BinaryProblem.from_dict(Q), backend=backend, qaoa_optimizer=optimizer
    )
    result_bitstrings = {x.bitstring for x in result.samples}
    assert all([is_plausible_bitstring(bs, 4) for bs in result_bitstrings])
    # assert ((0, 0, 1, 1) in result_bitstrings) or ((1, 1, 1, 1) in result_bitstrings)


@pytest.mark.parametrize("backend", ("qcware/cpu_simulator", "qcware/gpu_simulator"))
def test_analytical_angles_with_qaoa(backend):
    Q = sample_q()

    exvals, angles, Z = qcware.forge.optimization.find_optimal_qaoa_angles(
        Q, num_evals=100, num_min_vals=10
    )
    # print("EXVALS: ", exvals)
    # print("ANGLES: ", angles)

    result = qcware.forge.optimization.optimize_binary(
        instance=BinaryProblem.from_dict(Q),
        backend="qcware/cpu_simulator",
        qaoa_beta=angles[1][0],
        qaoa_gamma=angles[1][1],
        qaoa_p_val=1,
    )
    result_bitstrings = {x.bitstring for x in result.samples}
    assert all([is_plausible_bitstring(bs, 4) for bs in result_bitstrings])
    # assert ((0, 0, 1, 1) in result_bitstrings) or ((1, 1, 1, 1) in result_bitstrings)
