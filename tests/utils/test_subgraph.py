"""
Contains tests for the subgraph function.
"""

from qcware.optimization.utils import subgraph
from sympy import Symbol
from qcware.optimization.utils import QUBOMatrix, PUBOMatrix, IsingMatrix, HIsingMatrix
from qcware.optimization import QUBO, PUBO, Ising, HIsing, HOBO, HOIO
from numpy.testing import assert_raises


def test_subgraph():

    G = {(0, 1): -4, (0, 2): -1, (0,): 3, (1,): 2, (): 2}

    assert subgraph(G, {0, 2}, {1: 5}) == {(0,): -17, (0, 2): -1, (): 10}
    assert subgraph(G, {0, 2}) == {(0, 2): -1, (0,): 3}
    assert subgraph(G, {0, 1}, {2: -10}) == {(0, 1): -4, (0,): 13, (1,): 2}
    assert subgraph(G, {0, 1}) == {(0, 1): -4, (0,): 3, (1,): 2}

    a = Symbol('a')

    for t in (QUBO, PUBO, Ising, HIsing, HOBO, HOIO,
              QUBOMatrix, PUBOMatrix, IsingMatrix, HIsingMatrix):
        S = subgraph(t(G), {0, 1}, {2: a})
        assert type(S) == t
        assert S == {(0, 1): -4, (0,): 3-a, (1,): 2}
        assert S.subs(a, -10) == {(0, 1): -4, (0,): 13, (1,): 2}

    with assert_raises(ValueError):
        subgraph({0: 1, (0, 1): 1}, {})
