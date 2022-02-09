#!/bin/bash

file="test/potencia/output.dat"
file_graph="test/potencia/potencia_tiempos.png"

# PLOT #
echo "Generando gráfica de tiempos..."
gnuplot << END_GNUPLOT
set title "Tiempo de ejecución de algoritmo de potenciación modular
set ylabel "Tiempo de ejecución (ms)"
set xlabel "Tamaño del exponente (b)"
set key left top
set grid
set term png
set output "$file_graph"
plot "$file" using 1:2 title "Implementación propia", \
     "$file" using 1:3 title "GMP"
replot
quit
END_GNUPLOT