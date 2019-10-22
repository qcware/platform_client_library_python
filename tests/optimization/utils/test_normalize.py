"""
Contains tests for the normalize function.
"""

from qcware.optimization.utils import normalize
from qcware.optimization.utils import (
    DictArithmetic, QUBOMatrix, PUBOMatrix, IsingMatrix, HIsingMatrix
)
from qcware.optimization import QUBO, PUBO, Ising, HIsing, HOBO, HOIO


def test_subgraph():

    temp0 = {(0,): 4, (1,): -2}
    assert normalize(temp0) == {k: v / 4 for k, v in temp0.items()}

    temp1 = {(0,): -4, (1,): 2}
    assert normalize(temp1) == {k: v / 4 for k, v in temp1.items()}

    for t in (QUBO, PUBO, Ising, HIsing, HOBO, HOIO, DictArithmetic,
              QUBOMatrix, PUBOMatrix, IsingMatrix, HIsingMatrix):
        n = normalize(t(temp0))
        assert type(n) == t
