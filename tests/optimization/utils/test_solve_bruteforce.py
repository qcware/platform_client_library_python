"""
Contains tests for the bruteforce solvers.
"""

from qcware.optimization.utils import (
    solve_qubo_bruteforce, solve_ising_bruteforce,
    solve_pubo_bruteforce, solve_hising_bruteforce
)


def test_errors():

    assert solve_pubo_bruteforce({}) == (0, {})
    assert solve_pubo_bruteforce({}, all_solutions=True) == (0, [{}])
    assert solve_pubo_bruteforce({(): 5}) == (5, {})
    assert solve_pubo_bruteforce({(): 5}, all_solutions=True) == (5, [{}])


def test_solve_qubo_bruteforce():

    Q = {('0', 1): 1, (1, '2'): 1, (1, 1): -1, ('2', '2'): -2}
    assert solve_qubo_bruteforce(Q) == (-2, {'0': 0, 1: 0, '2': 1})

    Q = {(0, 0): 1, (0, 1): -1, (): 1}
    assert (
        solve_qubo_bruteforce(Q, True)
        ==
        (1, [{0: 0, 1: 0}, {0: 0, 1: 1}, {0: 1, 1: 1}])
    )


def test_solve_ising_bruteforce():

    L = {(0, 'a'): 1, ('a', 2): 1, ('a',): -1, (2,): -2}
    assert solve_ising_bruteforce(L) in (
        (-3, {0: -1, 'a': 1, 2: 1}),
        (-3, {0: 1, 'a': -1, 2: 1}),
    )

    L = {(0,): 0.25, (1,): -0.25, (0, 1): -0.25, (): 1.25}
    assert (
        solve_ising_bruteforce(L, True)
        ==
        (1, [{0: -1, 1: -1}, {0: -1, 1: 1}, {0: 1, 1: 1}])
    )


def test_solve_pubo_bruteforce():

    P = {
        ('0', 1): 1, (1, '2'): 1, (1, 1): -1, ('2', '2'): -2,
        (3, 4, 5): 1, (3,): 1, (4,): 1, (5,): 1
    }
    assert (
        solve_pubo_bruteforce(P)
        ==
        (-2, {'0': 0, 1: 0, '2': 1, 3: 0, 4: 0, 5: 0})
    )

    P = {
        (0, 0): 1, (0, 1): -1, (): 1,
        (3, 4, 5): 1, (3,): 1, (4,): 1, (5,): 1
    }
    assert (
        solve_pubo_bruteforce(P, True)
        ==
        (1, [{0: 0, 1: 0, 3: 0, 4: 0, 5: 0},
             {0: 0, 1: 1, 3: 0, 4: 0, 5: 0},
             {0: 1, 1: 1, 3: 0, 4: 0, 5: 0}])
    )


def test_solve_hising_bruteforce():

    H = {
        (0, 'a'): 1, ('a', 2): 1, ('a',): -1, (2,): -2,
        (3, 4, 5): -1, (3,): -1, (4,): -1, (5,): -1
    }
    assert solve_hising_bruteforce(H) in (
        (-7, {0: -1, 'a': 1, 2: 1, 3: 1, 4: 1, 5: 1}),
        (-7, {0: 1, 'a': -1, 2: 1, 3: 1, 4: 1, 5: 1}),
    )

    H = {(0,): 0.25, (1,): -0.25, (0, 1): -0.25, (): 1.25,
         (3, 4, 5): -1, (3,): -1, (4,): -1, (5,): -1}
    assert (
        solve_hising_bruteforce(H, True)
        ==
        (-3, [{0: -1, 1: -1, 3: 1, 4: 1, 5: 1},
              {0: -1, 1: 1, 3: 1, 4: 1, 5: 1},
              {0: 1, 1: 1, 3: 1, 4: 1, 5: 1}])
    )
