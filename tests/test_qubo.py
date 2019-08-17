import qcware
import os
import numpy as np

AQUA_KEY = os.environ['AQUA_TEST_KEY']
AQUA_HOST = os.environ['AQUA_HOST']

solver = "brute_force"


def test_qubo():
    Q = {(0, 0): 1, (0, 1): 1, (1, 1): 1, (1, 2): 1, (2, 2): -1}
    result = qcware.optimization.solve_binary(
        AQUA_KEY,
        Q,
        solver=solver,
        host=AQUA_HOST)
    print(result)


if __name__ == "__main__":
    test_qubo()
