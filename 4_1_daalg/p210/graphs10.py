"""Module with the implementation of:
    - Mini-Project 1: Basic Graph Algorithms
    - Mini-Project 2: Eulerian Circuits and Paths. Sequence Reconstruction.
"""
__author__ = 'Daniel Mohedano & Silvia Sopeña'

import numpy as np
import queue
import time
import copy
import random


def _truncate(number, n_decimals):
    """Truncates a number to a certain amount of decimal places.

    Truncates a floating point number to a certain amount of decimal places.
    To do this, it uses the numpy.trunc() function.

    Args:
        number (float): Number to truncate.
        n_decimals (int): Number of decimals.

    Returns:
        float: The truncated number.
    """
    adjustment = 10 ** n_decimals
    return np.trunc(number * adjustment) / adjustment


def _min_weight(mg, u, v):
    """Calculates the edge with the minimum weight between two nodes.

    Given a certain multigraph in dictionary form and a pair of nodes,
    returns the minimum weight of all the edges existing between u and v.

    Args:
        mg (dict): Multigraph
        u (int): Starting node
        v (int): Ending node

    Returns:
        float: Smallest edge weight
    """
    min_weight = np.Inf
    for weight in mg[u][v].values():
        if weight < min_weight:
            min_weight = weight

    return min_weight


def rand_weighted_multigraph(n_nodes,
                             probability=0.2,
                             num_max_multiple_edges=1,
                             max_weight=50.,
                             decimals=0,
                             fl_unweighted=False,
                             fl_diag=True):
    """Generates a directed multigraph with the provided parameters.

    Generates a directed multigraph. Using numpy.random.uniform(), the function
    decides if edges are inserted between every two nodes. The amount of edges
    created is then calculated with the help of numpy.random.randint(). The
    function numpy.random.uniform() is also used for the generation of the
    edge's weights.

    Args:
        n_nodes (int): Number of nodes in the graph.
        probability (float): Probability of link between two nodes. Defaults to
            0.2.
        num_max_multiple_edges (int): Maximum number of edges between two
            nodes. Defaults to 1.
        max_weight (float): Max weight of any edge in the graph.
            Defaults to 50.
        decimals (int): Float decimal digits for the weight. Defaults to 0.
        fl_unweighted (bool): If True, generates an unweighted graph. Defaults
            to False.
        fl_diag (bool): If True, self connected nodes are allowed. Defaults to
            True.

    Returns:
        dict: The multigraph dict generated.
    """
    # Generate main dict
    graph = {x: {} for x in range(n_nodes)}

    # Minimum value represented with decimals (used if fl_unweighted == False)
    # Used to assure equal probability for each possible weight
    min_decimal = 1.0 / (10 ** decimals)

    # Generate random edges
    for node_start, adj_list in graph.items():
        for node_end in graph:
            # Check if there should be an edge between this two nodes
            if (np.random.uniform() < probability) and \
                    ((node_start != node_end) or fl_diag):
                # Generate amount of multiple edges
                n_edges = np.random.randint(num_max_multiple_edges) + 1
                if fl_unweighted:
                    adj_list[node_end] = {x: 1 for x in range(n_edges)}
                else:
                    adj_list[node_end] = {
                        x: _truncate(
                            np.random.uniform(min_decimal,
                                              max_weight + min_decimal),
                            decimals)
                        for x in range(n_edges)}

    return graph


def rand_weighted_undirected_multigraph(n_nodes,
                                        probability=0.2,
                                        num_max_multiple_edges=1,
                                        max_weight=50.,
                                        decimals=0,
                                        fl_unweighted=False,
                                        fl_diag=True):
    """Generates an undirected multigraph with the provided parameters.

    Generates a directed multigraph. Using numpy.random.uniform(), the function
    decides if edges are inserted between every two nodes. The amount of edges
    created is then calculated with the help of numpy.random.randint(). The
    function numpy.random.uniform() is also used for the generation of the
    edge's weights.

    Args:
        n_nodes (int): Number of nodes in the graph.
        probability (float): Probability of link between two nodes. Defaults to
            0.2.
        num_max_multiple_edges (int): Maximum number of edges between two
            nodes. Defaults to 1.
        max_weight (float): Max weight of any edge in the graph.
            Defaults to 50.
        decimals (int): Float decimal digits for the weight. Defaults to 0.
        fl_unweighted (bool): If True, generates an unweighted graph. Defaults
            to False.
        fl_diag (bool): If True, self connected nodes are allowed. Defaults to
            True.

    Returns:
        dict: The undirected multigraph dict generated.
    """
    # Generate main dict
    graph = {x: {} for x in range(n_nodes)}

    # Minimum value represented with decimals (used if fl_unweighted == False)
    min_decimal = 1.0 / (10 ** decimals)

    # Generate random edges
    for node_start, adj_list in graph.items():
        for node_end in graph:
            # Check if there should be an edge between this two nodes
            if (node_start <= node_end) and \
                    (np.random.uniform() < probability) \
                    and ((node_start != node_end) or fl_diag):
                # Generate amount of multiple edges
                n_edges = np.random.randint(num_max_multiple_edges) + 1
                if fl_unweighted:
                    adj_list[node_end] = {x: 1 for x in range(n_edges)}
                    graph[node_end][node_start] = {x: 1
                                                   for x in range(n_edges)}
                else:
                    adj_list[node_end] = {
                        x: _truncate(
                            np.random.uniform(min_decimal,
                                              max_weight + min_decimal),
                            decimals)
                        for x in range(n_edges)}
                    graph[node_end][node_start] = {x: adj_list[node_end][x]
                                                   for x in range(n_edges)}

    return graph


def print_adj_list_mg(mg):
    """Prints the adjacency list of a given multigraph.

    Prints the adjacency list of a multigraph using the format A->(B,cost)->...

    Args:
        mg (dict): The multigraph to print.
    """
    for node_start, adj_list in mg.items():
        print('{}->'.format(node_start), end='')
        edges = []
        for node_end in sorted(adj_list.keys()):
            for e in adj_list[node_end]:
                edges.append((node_end, adj_list[node_end][e]))

        print(*edges, sep='->')


def dijkstra_mg(mg, u):
    """Applies Dijkstra's algorithm to a certain multigraph.

    Applies Dijkstra's algorithm to a multigraph to find the minimal paths
    starting from a given node.

    Args:
        mg (dict): Multigraph.
        u (int): Initial node.

    Returns:
        dict: Contains the minimum distances from u to them.
        dict: The previous of the accessible vertices.
    """
    # Initialize structures
    d_prev = {x: None for x in mg.keys()}
    d_dist = {x: np.Inf for x in mg.keys()}
    s = {x: False for x in mg.keys()}
    pq = queue.PriorityQueue()

    # Push starting node to Queue
    d_dist[u] = 0
    pq.put((d_dist[u], u))

    # Dijkstra's loop
    while not pq.empty():
        _, v = pq.get()
        if not s[v]:
            s[v] = True
            # If the node has not been checked
            for z in mg[v].keys():
                # Calculate the edge with minimum weight (c(v,z))
                min_weight = _min_weight(mg, v, z)

                # If a better path has been found, update it
                if d_dist[z] > d_dist[v] + min_weight:
                    d_dist[z] = d_dist[v] + min_weight
                    d_prev[z] = v
                    pq.put((d_dist[z], z))

    return d_dist, d_prev


def min_paths(d_prev):
    """Constructs paths from the parents dictionary.

    Reconstructs the paths given the parents dictionary generated by Dijkstra.

    Args:
        d_prev (dict): dictionary of parent nodes.

    Returns:
        dict: contains paths from starting node.
    """
    d_path = {x: None for x in d_prev.keys()}

    for v in d_path:
        if d_path[v] is None:
            # If the path has not already been generated
            path = [v]

            # Follow the parents dictionary
            while d_prev[path[-1]] is not None:
                path.append(d_prev[path[-1]])

            path.reverse()

            # Save the paths for v and all intermediate nodes (that do not have
            # a path already)
            while len(path) != 0:
                if d_path[path[-1]] is not None:
                    break
                d_path[path[-1]] = path
                path = path[:-1]

    return d_path


def time_dijkstra_mg(n_graphs,
                     n_nodes_ini,
                     n_nodes_fin,
                     step,
                     num_max_multiple_edges=1,
                     probability=0.2):
    """Times the execution of Dijkstra's algorithm.

    Iterates through different graph sizes, fron n_nodes_ini to n_nodes_fin
    with step. For each size, generates n_graphs graphs and times the execution
    of the algorithm on each of the graph's nodes.

    Args:
        n_graphs (int): Number of graphs generated for each size.
        n_nodes_ini (int): Initial graph size.
        n_nodes_fin (int): Final graph size.
        step (int): Step of the size iteration.
        num_max_multiple_edges (int): Number of maximum edges allowed between
            two nodes. Defaults to 1.
        probability (float): Probability of edge between two nodes. Defaults to
            0.2.

    Returns:
        list: Average of times for each graph size.
    """
    n_nodes = n_nodes_ini
    times = []

    # Steep through each graph size
    while n_nodes <= n_nodes_fin:
        total_time = 0.0

        # Generate the requested amount of graphs
        for i in range(n_graphs):
            mg = rand_weighted_multigraph(n_nodes,
                                          probability,
                                          num_max_multiple_edges)

            # Loop through every graph node and time the Dijkstra execution
            for u in mg:
                t = time.time()
                _, _ = dijkstra_mg(mg, u)
                t = time.time() - t
                total_time += t

        total_time = total_time / (n_graphs * n_nodes)
        times.append(total_time)

        n_nodes += step

    return times


def dijkstra_all_pairs(g):
    """Applies Dijkstra's algorithm to every pair of nodes in the graph

    Applies to every node of the graph Dijkstra's algorithm in order to find
    the minimum distance between every node in the graph.

    Args:
        g (dict): The graph

    Returns:
        np.ndarray: The minimum distance between every node.
    """
    distances = np.zeros((len(g), len(g)))

    # Iterate over all nodes in the graph
    for i in g:
        d_dist, _ = dijkstra_mg(g, i)
        for j in d_dist:
            distances[i][j] = d_dist[j]

    return distances


def dg_2_ma(g):
    """Builds an adjacency matrix from a multigraph in dictionary form

    Constructs the adjacency matrix of a graph provided in dictionary form.
    Non existing edges are left with a value of numpy.Inf and the diagonal has
    a value of 0.

    Args:
        g (dict): The graph

    Returns:
        np.ndarray: The adjacency matrix.
    """
    adj_matrix = np.full((len(g), len(g)), np.Inf)
    for i in g:
        for j in g[i]:
            adj_matrix[i][j] = g[i][j][0]

    np.fill_diagonal(adj_matrix, 0)

    return adj_matrix


def floyd_warshall(ma_g):
    """Applies Floyd-Warshall's algorithm to the graph provided.

    Applies Floyd-Warshall's algorithm to the graph provided in adjacency
    matrix form. It also applies some optimizations:
        - The diagonal is never checked.
        - It does not try to update the ith row and kth column in each
        iteration.

    Args:
        ma_g (np.ndarray): The adjacency matrix for the graph.

    Returns:
        np.ndarray: The minimum distance between every node.
    """
    d = np.copy(ma_g)

    # Apply Floyd-Warshall loop
    for k in range(len(ma_g)):
        for i in range(len(ma_g)):
            for j in range(len(ma_g)):
                if i != j and i != k and j != k:
                    # Only update positions which are NOT in the i-th row and
                    # k-th column
                    c = d[i][k] + d[k][j]
                    d[i][j] = min(d[i][j], c)

    return d


def time_dijkstra_mg_all_pairs(n_graphs,
                               n_nodes_ini,
                               n_nodes_fin,
                               step,
                               num_max_multiple_edges=1,
                               probability=0.5):
    """Times the execution of Dijkstra's algorithm on all pairs.

    Iterates through different graph sizes, fron n_nodes_ini to n_nodes_fin
    with step. For each size, generates n_graphs graphs and times the execution
    of the algorithm on each of the graph's nodes.

    Args:
        n_graphs (int): Number of graphs generated for each size.
        n_nodes_ini (int): Initial graph size.
        n_nodes_fin (int): Final graph size.
        step (int): Step of the size iteration.
        num_max_multiple_edges (int): Number of maximum edges allowed between
            two nodes. Defaults to 1.
        probability (float): Probability of edge between two nodes. Defaults to
            0.5.

    Returns:
        list: Average of times for each graph size.
    """
    n_nodes = n_nodes_ini
    times = []

    # Steep through each graph size
    while n_nodes <= n_nodes_fin:
        total_time = 0.0

        # Generate the requested amount of graphs
        for i in range(n_graphs):
            mg = rand_weighted_multigraph(n_nodes,
                                          probability,
                                          num_max_multiple_edges)

            t = time.time()
            dijkstra_all_pairs(mg)
            t = time.time() - t
            total_time += t

        total_time = total_time / n_graphs
        times.append(total_time)

        n_nodes += step

    return times


def time_floyd_warshall(n_graphs,
                        n_nodes_ini,
                        n_nodes_fin,
                        step,
                        probability=0.5):
    """Times the execution of Floyd-Warshall's algorithm.

    Iterates through different graph sizes, fron n_nodes_ini to n_nodes_fin
    with step. For each size, generates n_graphs graphs and times the execution
    of the algorithm on each of the graph's nodes.

    Args:
        n_graphs (int): Number of graphs generated for each size.
        n_nodes_ini (int): Initial graph size.
        n_nodes_fin (int): Final graph size.
        step (int): Step of the size iteration.
        probability (float): Probability of edge between two nodes. Defaults to
            0.5.

    Returns:
        list: Average of times for each graph size.
    """
    n_nodes = n_nodes_ini
    times = []

    # Steep through each graph size
    while n_nodes <= n_nodes_fin:
        total_time = 0.0

        # Generate the requested amount of graphs
        for i in range(n_graphs):
            mg = rand_weighted_multigraph(n_nodes, probability)
            ma_g = dg_2_ma(mg)

            t = time.time()
            floyd_warshall(ma_g)
            t = time.time() - t
            total_time += t

        total_time = total_time / n_graphs
        times.append(total_time)

        n_nodes += step

    return times


def adj_inc_directed_multigraph(d_mg):
    """Calculates the adjacencies and incidences of each vertex.

    Calculates both adjacency and incidence values for each vertex in the given
    multigraph. The values processed in the vertices' order (0, 1, ...).

    Args:
        d_mg (dict): The multigraph.

    Returns:
        list: Adjacency of each vertex.
        list: Incidence of each vertex.
    """
    adj = [0]*len(d_mg)
    inc = [0]*len(d_mg)

    for u, adj_list in d_mg.items():
        for v, edges in adj_list.items():
            adj[u] += len(edges)
            inc[v] += len(edges)

    return adj, inc


def isthere_euler_path_directed_multigraph(d_mg):
    """Determines if there is an Eulerian path in the multigraph.

    By definition, an Eulerian path {(u,u1),...,(uk-1,v)} exists in a directed
    graph if:
        - For every w in V different from u and v, in(w) = out(w).
        - in(v) = out(v) + 1
        - in(u) = out(u) - 1

    Args:
        d_mg (dict): The multigraph.

    Returns:
        bool: True if there is an Eulerian path. False if not.
    """
    adj, inc = adj_inc_directed_multigraph(d_mg)
    diff = [inc[i] - adj[i] for i in range(len(adj))]

    start = diff.count(-1)
    end = diff.count(1)
    rest = diff.count(0)

    return start == 1 and end == 1 and rest == (len(adj) - 2)


def first_last_euler_path_directed_multigraph(d_mg):
    """Determines if there are starting and ending points in the Eulerian path
    of the multigraph.

    Args:
        d_mg (dict): The multigraph.

    Returns:
        tuple: The starting and ending point. If it is empty, it returns an
        empty tuple.
    """
    adj, inc = adj_inc_directed_multigraph(d_mg)
    diff = [inc[i] - adj[i] for i in range(len(adj))]

    start = diff.count(-1)
    end = diff.count(1)
    rest = diff.count(0)

    if start == 1 and end == 1 and rest == (len(adj) - 2):
        return (diff.index(-1), diff.index(1))
    else:
        return tuple()


def euler_walk_directed_multigraph(u, d_mg):
    """Makes an Eulerian walk starting at node u.

    Makes an Eulerian walk starting at node u. Updates the multigraph removing
    the edges traversed.

    Args:
        u (int): Starting node.
        d_mg (dict): The multigraph.

    Returns:
        list: A List with all the vertices traversed.
    """
    traversed = [u]
    w = u

    # Update dictionary to remove nodes with no edges
    no_edges = []
    for vertex in sorted(d_mg.keys()):
        if len(d_mg[vertex]) == 0:
            no_edges.append(vertex)

    for vertex in no_edges:
        d_mg.pop(vertex)

    # We traverse the paths (w, z)
    while w in d_mg:
        # Take the first node connected to w
        z = sorted(d_mg[w].keys())[0]
        traversed.append(z)

        # Remove the first edge (w,z) from the adj list
        d_mg[w][z].pop(sorted(d_mg[w][z].keys())[0])

        # Update dictionaries in case all edges are removed
        if len(d_mg[w][z]) == 0:
            d_mg[w].pop(z)

        if len(d_mg[w]) == 0:
            d_mg.pop(w)

        w = z

    return traversed


def next_first_node(l_path, d_mg):
    """Finds the next node from which an Eulerian walk should be started.

    Finds the first node in the list from which a walk should be restarted
    according to the state of the graph.

    Args:
        l_path (list): The path.
        d_mg (dict): The multigraph.

    Returns:
        int: Next node to walk from. -1 if no next node.
    """
    for v in l_path:
        if v in d_mg:
            return v

    return -1


def path_stitch(path_1, path_2):
    """Stitches two paths together.

    Stitches two paths together inserting path_2 into path_1 in the correct
    position. If there is more than one possibility, path_2 is inserted in the
    first possible place.

    Args:
        path_1 (list): First path.
        path_2 (list): Second path.

    Returns:
        list: The stitched path.
    """
    first_node = path_2[0]
    index = path_1.index(first_node)

    new_path = path_1[:index] + path_2 + path_1[index+1:]

    return new_path


def euler_path_directed_multigraph(d_mg):
    """Finds an Eulerian path in the multigraph

    Args:
        d_mg (dict): The multigraph.

    Returns:
        list: The Euler path
    """
    path = []

    # Copy the original graph
    graph = copy.deepcopy(d_mg)

    first_last = first_last_euler_path_directed_multigraph(graph)
    if not first_last:
        return path

    first_node = first_last[0]

    path = euler_walk_directed_multigraph(first_node, graph)
    while len(graph) > 0:
        first_node = next_first_node(path, graph)
        path2 = euler_walk_directed_multigraph(first_node, graph)
        path = path_stitch(path, path2)

    return path


def isthere_euler_circuit_directed_multigraph(d_mg):
    """Determines if there is an Euler circuit in the multigraph.

    Args:
        d_mg (dict): The multigraph.

    Returns:
        bool: True if there is an Euler circuit. False if not.
    """
    adj, inc = adj_inc_directed_multigraph(d_mg)
    diff = [inc[i] - adj[i] for i in range(len(adj))]

    return diff.count(0) == len(d_mg)


def euler_circuit_directed_multigraph(d_mg, u=0):
    """Calculates an Eulerian circuit in the multigraph starting at u.

    Args:
        d_mg (dict): The multigraph.
        u (int): Starting vertex.

    Returns:
        list: Eulerian circuit.
    """
    circuit = []

    if not isthere_euler_circuit_directed_multigraph(d_mg):
        return circuit

    # Search for a node with an edge of the form (end_node, u)
    for end_node, adj_list in d_mg.items():
        if end_node != u and u in adj_list:
            break

    # Remove first edge between them
    graph = copy.deepcopy(d_mg)
    graph[end_node][u].pop(sorted(graph[end_node][u].keys())[0])

    if len(graph[end_node][u]) == 0:
        graph[end_node].pop(u)

    path = euler_path_directed_multigraph(graph)

    circuit = path + [u]

    return circuit


def random_sequence(len_seq):
    """Generates random sequences of the given length.

    Generates a random sequence of the given length with the characters A, C,
    G and T.

    Args:
        len_seq (int): Length of the sequence.

    Returns:
        str: The random sequence
    """
    return ''.join(random.choices(['A', 'C', 'G', 'T'], k=len_seq))


def spectrum(sequence, len_read):
    """Generates the unordered spectrum of the sequence provided.

    Args:
        sequence (str): Sequence.
        len_read (int): Length of the reads.

    Returns:
        list: The unordered spectrum.
    """
    spectrum = [sequence[i:i + len_read]
                for i in range(len(sequence) - len_read + 1)]

    random.shuffle(spectrum)
    return spectrum


def spectrum_2(spectr):
    """Generates the (l-1)-spectrum associated with the l-spectrum provided.

    Args:
        spectr (list): l-spectrum.

    Returns:
        list: (l-1)-spectrum.
    """
    new_spectrum = []

    for seq in spectr:
        if seq[:-1] not in new_spectrum:
            new_spectrum.append(seq[:-1])
        if seq[1:] not in new_spectrum:
            new_spectrum.append(seq[1:])

    return new_spectrum


def spectrum_2_graph(spectr):
    """Creates the multigraph from a given spectrum placing the l-mers in the
    edges.

    Args:
        spectr (list): l-spectrum.

    Returns:
        dict: Multigraph.
    """
    nodes = spectrum_2(spectr)

    # Generate dictionary with indexes of each (l-1)-mer to improve efficiency
    node_indexes = {nodes[i]: i for i in range(len(nodes))}

    d_mg = {i: {} for i in range(len(nodes))}

    for l_mer in spectr:
        # l_mer = 'GTA' -> node_ini = 'GT' node_end = 'TA'
        node_ini = l_mer[:-1]
        node_end = l_mer[1:]

        idx_ini = node_indexes[node_ini]
        idx_end = node_indexes[node_end]

        # Add an edge between node_ini and node_end
        if idx_end in d_mg[idx_ini]:
            # If there are already edges (node_ini, node_end) add another one
            edge_idx = max(d_mg[idx_ini][idx_end].keys()) + 1
            d_mg[idx_ini][idx_end][edge_idx] = 1.0
        else:
            # If there are no edges, create one
            d_mg[idx_ini][idx_end] = {0: 1.0}

    return d_mg


def spectrum_2_sequence(spectr):
    """Creates a possible sequence that gave rise to the spectrum provided.

    Args:
        spectr (list): l-spectrum.

    Returns:
        str: Sequence.
    """
    d_mg = spectrum_2_graph(spectr)

    if isthere_euler_circuit_directed_multigraph(d_mg):
        print('Eulerian circuit detected in spectrum_2_graph. Error.')
        return ''

    path = euler_path_directed_multigraph(d_mg)

    return path_2_sequence(path, spectrum_2(spectr))


def path_2_sequence(l_path, spectrum_2):
    """Converts a list of vertices from the spectrum into a sequence.

    Args:
        l_path (list): List of vertices.
        spectrum_2 (list): (l-1)-spectrum.

    Returns:
        str: Sequence from the spectrum.
    """
    sequence = spectrum_2[l_path[0]]
    last_chars = [spectrum_2[l_path[i]][-1] for i in range(1, len(l_path))]

    sequence += ''.join(last_chars)
    return sequence


def check_sequencing(len_seq, len_read):
    """Checks the sequencing by generating a random sequence and reconstructing
    it.

    Args:
        len_seq (int): Length of the sequence.
        len_read (int): Length of the l-mers in the l-spectrum.

    Returns:
        boolean: True if reconstruction successful, False otherwise.
    """
    sequence = random_sequence(len_seq)
    spectr = spectrum(sequence, len_read)
    reconstructed = spectrum_2_sequence(spectr)
    spectr_reconstructed = spectrum(reconstructed, len_read)

    spectr.sort()
    spectr_reconstructed.sort()

    return spectr == spectr_reconstructed
