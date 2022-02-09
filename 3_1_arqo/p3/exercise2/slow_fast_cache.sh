# Script for Exercise 2 Practice 3

#!/bin/bash

#------------------------INITIALIZE VARIABLES------------------------#
# Flags to determine execution of the script (select sections to execute)
echo "REMEMBER TO SET THE FLAGS IN THE SCRIPT TO SELECT WHICH SECTIONS ARE EXECUTED"
FLAG_VALGRIND=0
FLAG_PLOT_VALGRIND=0

# Configuration variables
Pair=10
P=$(($Pair % 7 + 4))
Ninicio=$((2000 + (512 * $P)))
Npaso=64
Nfinal=$((2000 + (512 * ($P+1))))
cache_size=1024

# File names
data_file_slow="data/slow.dat"
data_file_fast="data/fast.dat"
fPNGread="plot/cache_lectura.png"
fPNGwrite="plot/cache_escritura.png"

#------------------------CREATE DIRECTORIES------------------------#
mkdir -p data
mkdir -p plot 

#------------------------DELETE PREVIOUS FILES------------------------#
if [ $FLAG_VALGRIND -eq 1 ]
then
    rm -f $data_file_slow $data_file_fast
fi

if [ $FLAG_PLOT_VALGRIND -eq 1 ]
then
    rm -f $fPNGread $fPNGwrite
fi

#------------------------CREATE NEW DATA FILES------------------------#
if [ $FLAG_VALGRIND -eq 1 ]
then
    touch $data_file_slow
    touch $data_file_fast
fi

#------------------------RUN VALGRIND------------------------#
if [ $FLAG_VALGRIND -eq 1 ]
then
    # Changing the cache configuration in each loop
    for i in $(seq 4); do
        echo "CACHE CONFIGURATION -> L1_SIZE = $cache_size B, LL_SIZE = 8388608 B, BLOCK_SIZE = 64 B"
        data_file_cache="data/${cache_size}.dat"
        # Delete data file
        rm -f $data_file_cache
        # Generate the data file
        touch $data_file_cache

        for ((N = Ninicio ; N <= Nfinal ; N += Npaso)); do
            echo "N: $N / $Nfinal..."
            
            valgrind --tool=cachegrind --I1=$cache_size,1,64 --D1=$cache_size,1,64 --LL=8388608,1,64 --cachegrind-out-file=$data_file_slow ../code/slow $N
            valgrind --tool=cachegrind --I1=$cache_size,1,64 --D1=$cache_size,1,64 --LL=8388608,1,64 --cachegrind-out-file=$data_file_fast ../code/fast $N

            d1mrslow=$(cg_annotate $data_file_slow | grep 'PROGRAM TOTALS' | awk '{print $5}')
            d1mwslow=$(cg_annotate $data_file_slow | grep 'PROGRAM TOTALS' | awk '{print $8}')
            d1mrfast=$(cg_annotate $data_file_fast | grep 'PROGRAM TOTALS' | awk '{print $5}')
            d1mwfast=$(cg_annotate $data_file_fast | grep 'PROGRAM TOTALS' | awk '{print $8}')

            echo "$N    $d1mrslow   $d1mwslow   $d1mrfast   $d1mwfast" >> $data_file_cache
        done

        # Remove commas from data file
        sed -i 's/\([0-9]\),/\1/g' $data_file_cache

        cache_size=$(($cache_size * 2))
    done
fi

if [ $FLAG_PLOT_VALGRIND -eq 1 ]
then
echo "Generating plot for read..."
gnuplot << END_GNUPLOT
set title "Read misses for each cache configuration"
set ylabel "Read misses"
set xlabel "Matrix Size"
set key right center
set grid
set term png
set output "$fPNGread"
plot "data/1024.dat" using 1:2 with lines lw 2 title "1024-slow", \
     "data/1024.dat" using 1:4 with lines lw 2 title "1024-fast", \
     "data/2048.dat" using 1:2 with lines lw 2 title "2048-slow", \
     "data/2048.dat" using 1:4 with lines lw 2 title "2048-fast", \
     "data/4096.dat" using 1:2 with lines lw 2 title "4096-slow", \
     "data/4096.dat" using 1:4 with lines lw 2 title "4096-fast", \
     "data/8192.dat" using 1:2 with lines lw 2 title "8192-slow", \
     "data/8192.dat" using 1:4 with lines lw 2 title "8192-fast"
replot
quit
END_GNUPLOT

echo "Generating plot for write..."
gnuplot << END_GNUPLOT
set title "Write misses for each cache configuration"
set ylabel "Write misses"
set xlabel "Matrix Size"
set key right center
set grid
set term png
set output "$fPNGwrite"
plot "data/1024.dat" using 1:3 with lines lw 2 title "1024-slow", \
     "data/1024.dat" using 1:5 with lines lw 2 title "1024-fast", \
     "data/2048.dat" using 1:3 with lines lw 2 title "2048-slow", \
     "data/2048.dat" using 1:5 with lines lw 2 title "2048-fast", \
     "data/4096.dat" using 1:3 with lines lw 2 title "4096-slow", \
     "data/4096.dat" using 1:5 with lines lw 2 title "4096-fast", \
     "data/8192.dat" using 1:3 with lines lw 2 title "8192-slow", \
     "data/8192.dat" using 1:5 with lines lw 2 title "8192-fast"
replot
quit
END_GNUPLOT
fi

