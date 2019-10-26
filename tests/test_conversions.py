from qcware.optimization import ising_to_qubo, qubo_to_ising


def test_qubo_to_ising_to_qubo():

    qubo_args = {(0, 0): 1, (0, 1): 1, (1, 1): -1, (1, 2): .2}, 3
    assert qubo_args == ising_to_qubo(*qubo_to_ising(*qubo_args))


def test_ising_to_qubo_to_ising():

    ising_args = {0: 1, 2: -2}, {(0, 1): -4, (0, 2): 3}, -2
    assert ising_args == qubo_to_ising(*ising_to_qubo(*ising_args))


if __name__ == "__main__":
    test_qubo_to_ising_to_qubo()
    test_ising_to_qubo_to_ising()
