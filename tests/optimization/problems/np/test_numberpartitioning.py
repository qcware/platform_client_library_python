"""
Contains tests for the NumberPartitioning class.
"""

from qcware.optimization.problems import NumberPartitioning
from qcware.optimization.utils import solve_qubo_bruteforce, solve_ising_bruteforce
from numpy import allclose
from numpy.testing import assert_raises


S_withsoln = 1, 2, 3, 4
S_withoutsoln = 1, 3, 4, 4

problem_withsoln = NumberPartitioning(S_withsoln)
problem_withoutsoln = NumberPartitioning(S_withoutsoln)

solutions_withsoln = ((1, 4), (2, 3)), ((2, 3), (1, 4))
solutions_withoutsoln = ((1, 4), (3, 4)), ((3, 4), (1, 4))


def test_numberpartitioning_str():

    assert eval(str(problem_withsoln)) == problem_withsoln
    assert eval(str(problem_withoutsoln)) == problem_withoutsoln


def test_properties():

    assert problem_withsoln.S == S_withsoln


def test_invalid():

    with assert_raises(ValueError):
        NumberPartitioning([0, 1, 2])


def test_numberpartitioning_bruteforce():

    assert problem_withsoln.solve_bruteforce() in solutions_withsoln
    assert (
        problem_withsoln.solve_bruteforce(all_solutions=True) in
        (list(solutions_withsoln), list(reversed(solutions_withsoln)))
    )

    assert problem_withoutsoln.solve_bruteforce() in solutions_withoutsoln


# QUBO

def test_numberpartitioning_qubo_solve():

    e, sol = solve_qubo_bruteforce(problem_withsoln.to_qubo())
    solution = problem_withsoln.convert_solution(sol)

    assert solution in solutions_withsoln
    assert problem_withsoln.is_solution_valid(solution)
    assert problem_withsoln.is_solution_valid(sol)
    assert allclose(e, 0)

    e, sol = solve_qubo_bruteforce(problem_withoutsoln.to_qubo())
    solution = problem_withoutsoln.convert_solution(sol)

    assert solution in solutions_withoutsoln
    assert not problem_withoutsoln.is_solution_valid(solution)
    assert not problem_withoutsoln.is_solution_valid(sol)
    assert e != 0


def test_numberpartitioning_qubo_numvars():

    Q = problem_withsoln.to_qubo()
    assert (
        len(set(y for x in Q for y in x)) ==
        problem_withsoln.num_binary_variables ==
        Q.num_binary_variables
    )

    Q = problem_withoutsoln.to_qubo()
    assert (
        len(set(y for x in Q for y in x)) ==
        problem_withoutsoln.num_binary_variables ==
        Q.num_binary_variables
    )

# ising


def test_numberpartitioning_ising_solve():

    e, sol = solve_ising_bruteforce(problem_withsoln.to_ising())
    solution = problem_withsoln.convert_solution(sol)

    assert solution in solutions_withsoln
    assert problem_withsoln.is_solution_valid(solution)
    assert problem_withsoln.is_solution_valid(sol)
    assert allclose(e, 0)

    e, sol = solve_ising_bruteforce(problem_withoutsoln.to_ising())
    solution = problem_withoutsoln.convert_solution(sol)

    assert solution in solutions_withoutsoln
    assert not problem_withoutsoln.is_solution_valid(solution)
    assert not problem_withoutsoln.is_solution_valid(sol)
    assert e != 0


def test_numberpartitioning_ising_numvars():

    L = problem_withsoln.to_ising()
    assert L.num_binary_variables == problem_withsoln.num_binary_variables

    L = problem_withoutsoln.to_ising()
    assert L.num_binary_variables == problem_withoutsoln.num_binary_variables
