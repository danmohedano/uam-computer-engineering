import pytest
import graphs10
import tgf
import random
import copy

PRE = ''

@pytest.mark.parametrize('tgf_name, adj, inc',
    [
        [PRE+'graph1.tgf', [1, 4, 4, 4, 4, 1], [1, 4, 4, 4, 4, 1]],
        [PRE+'graph2.tgf', [2, 1, 1, 1], [1, 1, 1, 2]],
        [PRE+'graph3.tgf', [1, 2, 1, 1, 0, 1, 2], [0, 2, 1, 1, 1, 1, 2]],
        [PRE+'graph4.tgf', [1]*9, [1]*9]
    ])

def test_adj_inc(tgf_name, adj, inc):
    """Test adj_inc_directed_multigraph()
    """
    gr = tgf.TGF_2_dg(tgf_name)
    a, i = graphs10.adj_inc_directed_multigraph(gr)
    assert a == adj, 'Incorrect adjacency'
    assert i == inc, 'Incorrect incidence'


@pytest.mark.parametrize('tgf_name',
    [
        PRE+'graph1.tgf',
        PRE+'graph2.tgf',
        PRE+'graph3.tgf',
        PRE+'graph4.tgf'
    ])

def test_euler_circuit(tgf_name):
    """Test euler_circuit_directed_multigraph()
    """
    gr = tgf.TGF_2_dg(tgf_name)
    
    for k in gr.keys():
        c = graphs10.euler_circuit_directed_multigraph(gr, k)
        if not graphs10.isthere_euler_circuit_directed_multigraph(gr):
            assert len(c) == 0, 'Inexistent circuit found'
        else:
            graph = copy.deepcopy(gr)
            for i in range(len(c) - 1):
                u, v = c[i], c[i + 1]
                assert v in graph[u], 'Inexistent edge'
                graph[u][v].pop(sorted(graph[u][v].keys())[0])
                if len(graph[u][v]) == 0:
                    graph[u].pop(v)
                    if len(graph[u]) == 0:
                        graph.pop(u)

            assert len(graph) == 0, 'Invalid circuit, remaining edges'


@pytest.mark.parametrize('len_seq, len_read',
    [[random.randint(100, 200), random.randint(7, 15)] for i in range(100)])

def test_sequences(len_seq, len_read):
    """Test check_sequencing()
    """
    assert graphs10.check_sequencing(len_seq, len_read), \
    f'Incorrect sequencing for {len_seq}:{len_read}'
