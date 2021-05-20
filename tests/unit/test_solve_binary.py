import qcware
import pytest
import itertools
from qcware.types.optimization import BinaryProblem


def sample_q():
    return {
        (0, 0): 1,
        (1, 1): 1,
        (0, 1): -2,
        (2, 2): -2,
        (3, 3): -4,
        (3, 2): -6
    }


@pytest.mark.parametrize(
    "backend",
    ('qcware/cpu', 'dwave/2000q', 'dwave/advantage', 'dwave_direct/2000q',
     'dwave_direct/advantage')  # ,
    #                           'awsbraket/dwave/2000q', 'awsbraket/dwave/advantage')
)
def test_solve_binary(backend: str):
    Q = sample_q()

    result = qcware.optimization.solve_binary(Q=Q,
                                              backend=backend,
                                              dwave_num_reads=1)
    assert (result['solution'] == [0, 0, 1, 1]
            or result['solution'] == [1, 1, 1, 1])


@pytest.mark.parametrize("backend",
                         ('qcware/cpu', 'dwave/2000q', 'dwave_direct/2000q', 'dwave/advantage')  # ,
                         #                           'awsbraket/dwave/2000q', 'awsbraket/dwave/advantage')
                         )
def test_optimize_binary(backend):
    Q = sample_q()
    problem_instance = BinaryProblem.from_dict(Q)
    result = qcware.optimization.optimize_binary(
        instance=problem_instance, backend=backend)
    assert result.original_problem.objective.dict() == problem_instance.objective.dict()
    result_vectors = [x[1] for x in result.return_results()]
    assert ([0, 0, 1, 1] in result_vectors) or ([1, 1, 1, 1] in result_vectors)


@ pytest.mark.parametrize('backend',
                          (  # 'dwave/2000q', 'dwave/advantage',
                              'dwave_direct/2000q', 'dwave_direct/advantage'))
def test_anneal_offsets(backend: str):
    """Smoke test for anneal offsets being at least callable; does not test their
    validity
    """
    Q = {(0, 0): 1, (1, 1): 1, (0, 1): -2}  # sample_q()

    result = qcware.optimization.solve_binary(Q=Q,
                                              backend=backend,
                                              dwave_num_reads=1,
                                              dwave_anneal_offsets_delta=0.5)
    assert 'solution' in result


@ pytest.mark.parametrize("backend,nmeasurement",
                          [('qcware/cpu_simulator', None),
                           ('qcware/gpu_simulator', None),
                           ('awsbraket/sv1', 1000)])
def test_solve_binary_qaoa(backend: str, nmeasurement: int):
    Q = sample_q()

    result = qcware.optimization.optimize_binary(
        instance=BinaryProblem.from_dict(Q), backend=backend,
        qaoa_nmeasurement=nmeasurement, qaoa_optimizer='analytical')
    result_vectors = [x[1] for x in result.return_results()]
    assert ([0, 0, 1, 1] in result_vectors) or ([1, 1, 1, 1] in result_vectors)


@ pytest.mark.parametrize('optimizer, backend',
                          itertools.product(
                              ('COBYLA', 'bounded_Powell', 'analytical'),
                              ('qcware/cpu_simulator', 'qcware/gpu_simulator')))
def test_various_qaoa_optimizers(optimizer, backend):
    Q = sample_q()
    result = qcware.optimization.optimize_binary(
        instance=BinaryProblem.from_dict(Q), backend=backend,
        qaoa_optimizer=optimizer)
    result_vectors = [x[1] for x in result.return_results()]
    assert ([0, 0, 1, 1] in result_vectors) or ([1, 1, 1, 1] in result_vectors)


@ pytest.mark.parametrize('backend',
                          ('qcware/cpu_simulator', 'qcware/gpu_simulator'))
def test_analytical_angles_with_qaoa(backend):
    Q = sample_q()

    exvals, angles, Z = qcware.optimization.find_optimal_qaoa_angles(
        Q, num_evals=100, num_min_vals=10)
    # print("EXVALS: ", exvals)
    # print("ANGLES: ", angles)

    result = qcware.optimization.optimize_binary(
        instance=BinaryProblem.from_dict(Q), backend='qcware/cpu_simulator',
        qaoa_beta=angles[1][0], qaoa_gamma=angles[1][1], qaoa_p_val=1)
    result_vectors = [x[1] for x in result.return_results()]
    assert ([0, 0, 1, 1] in result_vectors) or ([1, 1, 1, 1] in result_vectors)
