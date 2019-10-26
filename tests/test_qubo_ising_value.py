from qcware.optimization import qubo_value, ising_value


def test_qubo_value():
    Q = {(0, 0): 1, (0, 1): -1, (2, 2): 4}
    x = [1, 0, 1]
    assert qubo_value(x, Q) == 5

    offset = -2
    assert qubo_value(x, Q, offset) == 3


def test_ising_value():
    J = {(0, 1): 1, (1, 2): -2}
    h = {0: 3}
    z = [1, -1, 1]
    assert ising_value(z, h, J) == 4

    offset = -2
    assert ising_value(z, h, J, offset) == 2


if __name__ == "__main__":
    test_qubo_value()
    test_ising_value()
