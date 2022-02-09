#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import os
import sys
import argparse
import textwrap

from sklearn.linear_model import LinearRegression

import graphs10 as my_gr

def fit(l, func_2_fit, size_ini, size_fin, step):
    """Fits a function func_2_fit to the values in l using the 
    LinearRegression class from scikit-learn.
    """
    l_func_values =[func_2_fit(i) for i in range(size_ini, size_fin+1, step)]
    
    lr_m = LinearRegression()
    X = np.array(l_func_values).reshape( len(l_func_values), -1 )
    lr_m.fit(X, l)
    y_pred = lr_m.predict(X)
    
    return y_pred #ajuste a l por l func_2_fit


def n2_log_n(n):
    """Returns the square of n times its log.
    """
    if n > 0.:
        return n**2. * np.log(n)
    sys.exit("arg <= 0.")


def n3_log_n(n):
    """Returns the cube of n times its log.
    """
    if n > 0.:
        return n**3. * np.log(n)
    sys.exit("arg <= 0.")

def n3(n):
    """Returns the cube of n.
    """
    if n > 0.:
        return n**3.
    sys.exit("arg <= 0.")

  
####################################### main
def main(n_graphs, 
         n_nodes_ini, 
         n_nodes_fin, 
         step, 
         probability,
         num_max_multiple_edges,
         max_weight):
    """Prueba las funciones de generación y gestión de grafos, y las que implementan los algoritmos
    dijkstra y floyd_warshall.
    
    Args: 
        n_graphs
        n_nodes_ini
        n_nodes_fin
        step
        probability
        num_max_multiple_edges
        max_weight
        
    Returns:
        None
    """
    
    # check print y conversión de matriz de adyacencia
    print("\ncomprobamos funciones básicas en un grafo predefinido ..........")
    mg_fix = {
          0: {1: {0: 10}, 2: {0:1}}, 
          1: {2: {0: 1}}, 
          2: {3: {0: 1}},
          3: {1: {0: 1}}
         }
    
    print("\nlista de adyacencia")
    gr.print_adj_list_mg(mg_fix)
    
    g = {
          0: {1: {0: 10}}, 
          1: {2: {0: 1}}, 
          2: {3: {0: 1}},
          3: {1: {0: 1}}
         }
    
    ma_g = gr.dg_2_ma(mg_fix)
    print("\nmatriz de adyacencia\n")
    for i in range(ma_g.shape[0]):
        print(ma_g[i, :])
    
    _ = input("\npulsar Intro para continuar ....................\n")
    
    # check generar/imprimir grafo, multigrafo
    print("\ncomprobamos la generación de multigrafos dirigidos aleatorios ..........")
    r_mg = gr.rand_weighted_multigraph(n_nodes=5,
                                       probability=probability,
                                       num_max_multiple_edges=num_max_multiple_edges,
                                       max_weight=max_weight,
                                       decimals=0,
                                       fl_unweighted=False,
                                       fl_diag=True)
    
    print("lista de adyacencia del multigrafo generado")
    gr.print_adj_list_mg(r_mg)
    
    print("\n\ncomprobamos la generación de grafos estándar aleatorios ..........")
    r_mg = gr.rand_weighted_multigraph(n_nodes=5,
                                       probability=probability,
                                       num_max_multiple_edges=1, 
                                       max_weight=max_weight,
                                       decimals=0,
                                       fl_unweighted=False,
                                       fl_diag=True)
    
    print("\n\nlista de adyacencia del grafo generado")
    gr.print_adj_list_mg(r_mg)
    
    print("\n\nmatriz de adyacencia del grafo generado")
    ma_g = gr.dg_2_ma(r_mg)
    for i in range(ma_g.shape[0]):
        print(ma_g[i, :])
    
    _ = input("\npulsar Intro para continuar ....................\n")
    
    print("\ncomprobamos la generación de grafos no dirigidos aleatorios ..........")
    
    r_mg = gr.rand_weighted_undirected_multigraph(n_nodes=5,
                                                  probability=probability,
                                                  num_max_multiple_edges=1, 
                                                  max_weight=max_weight,
                                                  decimals=0,
                                                  fl_unweighted=False,
                                                  fl_diag=True)

    print("\nlista de adyacencia del grafo generado")
    gr.print_adj_list_mg(r_mg)  
    
    ma_g = gr.dg_2_ma(r_mg)
    print("\n\nmatriz de adyacencia del grafo generado")
    for i in range(ma_g.shape[0]):
        print(ma_g[i, :])
    
    _ = input("\npulsar Intro para continuar ....................\n")
    
    # check dijkstra y caminos óptimos
    print("\nsingle source Dijkstra ....................")
    
    node = np.random.randint(0, len(mg_fix.keys()))
    print("starting node {0:d}\n".format(node))
    d, p = gr.dijkstra_mg(mg_fix, node)
    my_d, my_p = my_gr.dijkstra_mg(mg_fix, node)
    
    assert d == my_d, 'distances not equal'
    assert p == my_p, 'prev not equal'
    
    print("\ndistancias", d)
    print("mi_distancias", my_d)
    print("\nprevios", p)
    print("mi_previos", my_p)

    d_path = gr.min_paths(p)
    my_d_path = my_gr.min_paths(p)
    
    for k in d_path.keys():
        print("\npaths_from ", k, d_path[k])
        print("mi_paths_from ", k, my_d_path[k])
        
        assert d_path[k] == my_d_path[k], 'path {0:d}not equal'.format(k)
    
    _ = input("\npulsar Intro para continuar ....................\n")
    
    print("\nDijkstra all pairs minimum distances ....................")
    dist_dijkstra    = gr.dijkstra_all_pairs(mg_fix)
    my_dist_dijkstra = my_gr.dijkstra_all_pairs(mg_fix)
    
    print("\nall_dist_dijkstra\n", dist_dijkstra)
    print("\nmy_all_dist_dijkstra\n", my_dist_dijkstra)
    
    assert dist_dijkstra.all() == my_dist_dijkstra.all(), 'all pairs dijkstra matrices not equal'
    
    _ = input("\npulsar Intro para continuar ....................\n")
    # check floyd warshall
    print("\nFloyd-Warshall all pairs minimum distances ....................")
    ma_g = gr.dg_2_ma(mg_fix)
    dist_fw    = gr.floyd_warshall(ma_g)
    my_dist_fw = my_gr.floyd_warshall(ma_g)
    
    print("floyd_warshall\n", dist_fw)
    print("\nmy_floyd_warshall\n", my_dist_fw)
    assert dist_fw.all() == my_dist_fw.all(), 'floyd_warshall distances not equal'
    
    _ = input("\npulsar Intro para continuar ....................\n")
    
    # check tiempos djikstra/fw
    print("\ntiming all pairs dijkstra ....................")
    l_t_d = gr.time_dijkstra_mg_all_pairs(n_graphs, n_nodes_ini, n_nodes_fin, step, num_max_multiple_edges=num_max_multiple_edges, probability=probability)
    t_pred_d = fit(l_t_d, n3_log_n, size_ini=n_nodes_ini, size_fin=n_nodes_fin, step=step)
    
    
    print("\ntiming Floyd-Warshall ....................")
    l_t_f = gr.time_floyd_warshall(n_graphs, n_nodes_ini, n_nodes_fin, step, probability=probability)
    t_pred_f = fit(l_t_f, n3, size_ini=n_nodes_ini, size_fin=n_nodes_fin, step=step)
    
    print("\ntiempos_dijkstra_reales   ", np.array(l_t_d).round(4))
    print("\ntiempos_fw_reales         ", np.array(l_t_f).round(4))
    
    print("\ntiempos_dijsktra_ajustados", t_pred_d.round(4))
    print("\ntiempos_fw_ajustados      ", t_pred_f.round(4))
    
    
###############################################################################################
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="comprobador de la práctica 1.")
    
    parser.add_argument("-p", "--pareja", type=str, default=None)
    parser.add_argument("-ng", "--num_graphs", type=int, default=10)
    parser.add_argument("-is", "--initial_size", type=int, default=10)
    parser.add_argument("-fs", "--final_size", type=int, default=20)
    parser.add_argument("-me", "--num_max_multiple_edges", type=int, default=1)
    parser.add_argument("-s", "--step", type=int, default=2)    
    parser.add_argument("-pr", "--probability", type=float, default=0.5)    
    parser.add_argument("-mw", "--max_weight", type=float, default=10.)    
    
    args = parser.parse_args()
    
    if len(sys.argv) > 1:
        if args.pareja is not None:
            f_path = "./p1" + args.pareja + "/grafos" + args.pareja + ".py"
            if os.path.isfile(f_path):
                str_comm = "cp ./p1" + args.pareja + "/grafos" + args.pareja + ".py  ./grafos.py"
                print(str_comm)
                os.system(str_comm)
                import grafos as gr
        
        else:
            import graphs10 as gr
        
        main(args.num_graphs, 
            args.initial_size, 
            args.final_size, 
            args.step, 
            args.probability,
            args.num_max_multiple_edges,
            args.max_weight)
    
    else:
        parser.print_help()
            
        