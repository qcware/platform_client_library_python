import qcware
import os
import pytest
QCWARE_API_KEY = os.environ['QCWARE_API_KEY']
QCWARE_HOST = os.environ['QCWARE_HOST']


def test_solve_binary_with_brute_force():
    Q = {(0, 0): "POTATO"}

    result = qcware.optimization.solve_binary(Q=Q,
                                              backend="classical",
                                              api_key=QCWARE_API_KEY,
                                              host=QCWARE_HOST)
    assert 'error' in result
