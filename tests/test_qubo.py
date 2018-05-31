import qcware
import os
import numpy as np

Aqua_key = os.environ['AQUA_TEST_KEY']


def test_qubo():
    Q = {(0, 0): 1, (0, 1): 1, (1, 1): 1, (1, 2): 1, (2, 2): -1}
    solver = 'dwave_software'
    result = qcware.optimization.solve_binary(
        Aqua_key,
        Q,
        solver=solver,
        host="http://platform.qcware.com")
    assert(np.equal(
        result['solution'],
        np.array([0, 0, 1])).all())
    print(result)


if __name__ == "__main__":
    test_qubo()


    
