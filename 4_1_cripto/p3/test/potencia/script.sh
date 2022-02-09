#!/bin/bash

# VARIABLES #
N_ini=100
N_fin=4000
N_step=100

file="test/potencia/output.dat"
file_graph="test/potencia/potencia_tiempos.png"

rm -f $file
touch $file

for ((N = N_ini ; N <= N_fin ; N += N_step)); do
    echo "N: $N"
    base=$(openssl rand -hex $N)
    exponente=$(openssl rand -hex $N)
    modulo=$(openssl rand -hex $N)
    times=$(./potencia.exe $base $exponente $modulo | grep 'Tiempo:' | awk '{times[NR] = $2} END {print times[1], "\t" ,times[2]}')
    echo "$N    $times" >> $file
done
