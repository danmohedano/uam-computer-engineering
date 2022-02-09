#!/usr/bin/env python
# -*- coding: utf-8 -*-

######################################## trivial graph format
def dg_2_TGF(d_mg, f_name):
    """Saves a multigraph dict as a TGF file.
    
    Args:
        d_mg: multigraph dict.
        f_name: string with target TGF file name.
    
    Returns:
        None
    """
    f = open(f_name, 'w')
    
    for u in sorted(d_mg.keys()):
        f.write(str(u) + '\n')
    f.write('#\n')
    
    for u in d_mg.keys():
        for v in d_mg[u].keys():
            for k in d_mg[u][v].keys():
                s = str(u) + ' ' + str(v) + ' ' + str(d_mg[u][v][k]) + '\n'   
            f.write(s)   
    
    f.close()

    
def TGF_2_dg(f_name):
    """Reads a TGF file into a multigraph dict.
    
    Args:
        f_name: string with target TGF file name.
    
    Returns:
        d_mg: multigraph dict.
    """
    f = open(f_name, 'r')
    s = f.read().split('\n')
    n_v = s.index('#')
    d_mg = {}
    d_ramas_from_u_to_v = {}
    
    for u in s[ : n_v]:
        d_mg[ int(u) ] = {}
        d_ramas_from_u_to_v[int(u)] = {}
    
    for s2 in s[n_v +  1 : ]:
        s2 = s2.split()
        if len(s2) == 3:
            u, v, w = tuple(s2)
            if int(v) not in d_ramas_from_u_to_v[int(u)].keys():
                d_ramas_from_u_to_v[int(u)][int(v)] = 0
                d_mg[int(u)][int(v)] = {}
                d_mg[int(u)][int(v)][0] = float(w)
                
            else:
                d_ramas_from_u_to_v[int(u)][int(v)] += 1
                d_mg[ int(u)][ int(v)][d_ramas_from_u_to_v[int(u)][int(v)]] = float(w)
                
        elif len(s2) > 0:
            print("erroneous_line:", s2)
    
    f.close()
    
    return d_mg
    
