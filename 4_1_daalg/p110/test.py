import graphs10

graph = graphs10.rand_weighted_multigraph(5, num_max_multiple_edges=4, fl_diag=True)
#graph = {0: {0: {0: 43.0, 1: 4.0, 2: 17.0}, 1: {0: 1.0, 1: 1.0, 2: 16.0, 3: 4.0}}, 1: {0: {0: 1.0, 1: 1.0, 2: 16.0, 3: 4.0}, 3: {0: 14.0, 1: 34.0, 2: 38.0, 3: 22.0}}, 2: {}, 3: {1: {0: 14.0, 1: 34.0, 2: 38.0, 3: 22.0}}, 4: {4: {0: 26.0, 1: 8.0, 2: 35.0}}}
graphs10.print_adj_list_mg(graph)
print(graph)
print('===========================')
d_dist, d_prev = graphs10.dijkstra_mg(graph, 0)
print(d_dist)
print(graphs10.min_paths(d_prev))
#print(graphs10.time_dijkstra_mg(20, 10, 50, 2, 1, 0.5))

print(graphs10.dijkstra_all_pairs(graph))
