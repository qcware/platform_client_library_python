import qcware
import networkx as nx
import numpy


def generate_rand_reg_p5(d, n):
    '''Generate a random d regular graph with n nodes with a P5 hamiltonian'''
    G = nx.random_regular_graph(d, n, seed=999)
    cost_dictionary = {}
    for elm in list(G.nodes()):
        cost_dictionary[elm, ] = 1
    edges = [sorted(elm) for elm in list(G.edges())]
    for elm in edges:
        cost_dictionary[elm[0], elm[1]] = 1
    return cost_dictionary, G


def test_analytical_angle_determination():
    cost_dictionary, graph = generate_rand_reg_p5(2, 5)
    n_linear = 100
    # Q = {(0, 0): 1, (1, 1): 1, (0, 1): -2, (2, 2): -2, (3, 3): -4, (3, 2): -5}
    sol = qcware.optimization.find_optimal_qaoa_angles(cost_dictionary,
                                                       num_evals=n_linear,
                                                       num_min_vals=10,
                                                       fastmath_flag_in=True,
                                                       precision=30)
    assert sol[0].sort() == [
        -2.7542642560338755, -2.754264256033875, -2.7495290205139753,
        -2.7495290205139744, -0.7480763200529221, -0.47430595681568066,
        -0.47430595681568033, -0.4193709671367115, 0, 0
    ].sort()
    assert sol[1][:4] == [[2.729060284936588, 0.28559933214452665],
                          [0.4125323686532052, 2.8559933214452666],
                          [2.729060284936588, 1.3010636242139548],
                          [0.4125323686532052, 1.8405290293758385]]
    assert sol[2].shape == (n_linear, n_linear)
