"""
Contains tests for the BILP class.
"""

from qcware.optimization.problems import BILP
from qcware.optimization.utils import solve_qubo_bruteforce, solve_ising_bruteforce
from numpy import allclose
from numpy.testing import assert_raises


c = [1, 2, -1]
S = [[1, 0, 0], [0, 1, -1]]
b = [0, 1]
problem = BILP(c, S, b)
solution = [0, 1, 0]


def test_bilp_str():

    assert eval(str(problem)) == problem


def test_properties():

    assert allclose(problem.c, c)
    assert allclose(problem.S, S)
    assert allclose(problem.b, b)


def test_errors():

    with assert_raises(ValueError):
        BILP([c], S, b)

    with assert_raises(ValueError):
        BILP(c, S, b + [0])


def test_bilp_bruteforce():

    assert allclose(problem.solve_bruteforce(), solution)


# QUBO

def test_bilp_qubo_solve():

    e, sol = solve_qubo_bruteforce(problem.to_qubo())
    conv_solution = problem.convert_solution(sol)

    assert allclose(conv_solution, solution)
    assert problem.is_solution_valid(conv_solution)
    assert problem.is_solution_valid(sol)
    assert allclose(e, 2)


def test_bilp_qubo_numvars():

    Q = problem.to_qubo()
    assert (
        len(set(y for x in Q for y in x)) ==
        problem.num_binary_variables ==
        Q.num_binary_variables
    )


# ising

def test_bilp_ising_solve():

    e, sol = solve_ising_bruteforce(problem.to_ising())
    conv_solution = problem.convert_solution(sol)

    assert allclose(conv_solution, solution)
    assert problem.is_solution_valid(conv_solution)
    assert problem.is_solution_valid(sol)
    assert allclose(e, 2)


def test_bilp_ising_numvars():

    L = problem.to_ising()
    assert L.num_binary_variables == problem.num_binary_variables
