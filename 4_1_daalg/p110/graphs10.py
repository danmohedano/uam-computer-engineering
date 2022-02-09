"""Module with the implementation of Mini-Project 1: Basic Graph Algorithms"""
__author__ = 'Daniel Mohedano & Silvia Sopeña'

import numpy as np
import queue
import time


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
        for node_end in adj_list:
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
