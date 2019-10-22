"""
Contains tests for the SetCover class.
"""

from qcware.optimization.problems import SetCover
from qcware.optimization.utils import solve_qubo_bruteforce, solve_ising_bruteforce
from numpy import allclose


U = {"a", "b", "c", "d"}
V = [{"a", "b"}, {"a", "c"}, {"c", "d"}]
problem_log = SetCover(U, V)
problem = SetCover(U, V, log_trick=False)
problem_weighted = SetCover(U, V, weights=(.1, .2, 1))


def test_setcover_str():

    assert eval(str(problem)) == problem
    assert eval(str(problem_log)) == problem_log
    assert eval(str(problem_weighted)) == problem_weighted


def test_properties():

    problem.weights
    problem.M
    problem.log_trick


def test_coverable():

    assert problem.is_coverable()
    assert not SetCover(U, V[:-1]).is_coverable()


def test_setcover_bruteforce():

    assert problem.solve_bruteforce() == {0, 2}


# QUBO

def test_setcover_qubo_logtrick_solve():

    e, sol = solve_qubo_bruteforce(problem_log.to_qubo())
    solution = problem_log.convert_solution(sol)
    assert problem_log.is_solution_valid(solution)
    assert problem_log.is_solution_valid(sol)
    assert solution == {0, 2}
    assert allclose(e, len(solution))


def test_setcover_qubo_solve():

    e, sol = solve_qubo_bruteforce(problem.to_qubo())
    solution = problem.convert_solution(sol)
    assert problem.is_solution_valid(solution)
    assert problem.is_solution_valid(sol)
    assert solution == {0, 2}
    assert allclose(e, len(solution))


def test_setcover_qubo_logtrick_numvars():

    Q = problem_log.to_qubo()
    assert (
        len(set(y for x in Q for y in x)) ==
        problem_log.num_binary_variables ==
        Q.num_binary_variables
    )


def test_setcover_qubo_numvars():

    Q_notlog = problem.to_qubo()
    assert (
        len(set(y for x in Q_notlog for y in x)) ==
        problem.num_binary_variables ==
        Q_notlog.num_binary_variables
    )


def test_weighted_setcover():

    e, sol = solve_qubo_bruteforce(problem_weighted.to_qubo())
    solution = problem_weighted.convert_solution(sol)
    assert problem_weighted.is_solution_valid(solution)
    assert problem_weighted.is_solution_valid(sol)
    assert solution == {0, 2}
    assert allclose(e, 1.1)


# ising

def test_setcover_ising_logtrick_solve():

    e, sol = solve_ising_bruteforce(problem_log.to_ising())
    solution = problem_log.convert_solution(sol)
    assert problem_log.is_solution_valid(solution)
    assert problem_log.is_solution_valid(sol)
    assert solution == {0, 2}
    assert allclose(e, len(solution))


def test_setcover_ising_solve():

    e, sol = solve_ising_bruteforce(problem.to_ising())
    solution = problem.convert_solution(sol)
    assert problem.is_solution_valid(solution)
    assert problem.is_solution_valid(sol)
    assert solution == {0, 2}
    assert allclose(e, len(solution))


def test_setcover_ising_logtrick_numvars():

    L = problem_log.to_ising()
    assert L.num_binary_variables == problem_log.num_binary_variables


def test_setcover_ising_numvars():

    L = problem.to_ising()
    assert L.num_binary_variables == problem.num_binary_variables
