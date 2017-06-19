import numpy as np
import networkx as nx
import qcware


def test_valid():
    my_graph = nx.complete_graph(4)
    pos = nx.spring_layout(my_graph)
    adj = nx.adjacency_matrix(my_graph).todense()
    adj = -(np.diag(np.squeeze((np.matrix(adj) * np.ones([adj.shape[0], 1])).A)) - np.matrix(adj)).astype(int)
    r = qcware.optimization.solve_binary(Q=adj, key="BH1ewSDXdbLJ")

    assert(len(r['solution']) == 4)

    return


def test_invalid_1():
    my_graph = nx.complete_graph(4)
    pos = nx.spring_layout(my_graph)
    adj = nx.adjacency_matrix(my_graph).todense()
    adj = -(np.diag(np.squeeze((np.matrix(adj) * np.ones([adj.shape[0], 1])).A)) - np.matrix(adj)).astype(int)
    r = qcware.optimization.solve_binary(Q=adj, key="BAD_KEY")

    assert(r.get('error'))

    return


def test_invalid_2():
    my_graph = nx.complete_graph(4)
    pos = nx.spring_layout(my_graph)
    adj = nx.adjacency_matrix(my_graph).todense()
    adj = -(np.diag(np.squeeze((np.matrix(adj) * np.ones([adj.shape[0], 1])).A)) - np.matrix(adj)).astype(int)
    r = qcware.optimization.solve_binary(Q=adj)

    assert(r.get('error'))

    return
