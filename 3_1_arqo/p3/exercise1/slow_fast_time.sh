# Script for Exercise 1 Practice 3

#!/bin/bash

#------------------------INITIALIZE VARIABLES------------------------#
# Flags to determine execution of the script (select sections to execute)
echo "REMEMBER TO SET THE FLAGS IN THE SCRIPT TO SELECT WHICH SECTIONS ARE EXECUTED"
FLAG_TIME=0
FLAG_PLOT_TIME=0

# Configuration variables
REPS=8
Pair=10
P=$(($Pair % 7 + 4))
Ninicio=$((10000 + (1024 * $P)))
Npaso=64
Nfinal=$(($Ninicio + 1024))

# File names
fDATaux="data/data_aux.dat"
fDAT="data/slow_fast_time_reps_${REPS}.dat"
fPNG="plot/slow_fast_time_reps_${REPS}.png"

#------------------------CREATE DIRECTORIES------------------------#
mkdir -p data
mkdir -p plot

#------------------------DELETE PREVIOUS FILES------------------------#
if [ $FLAG_TIME -eq 1 ]
then 
    rm -f $fDAT $fDATaux
fi

if [ $FLAG_PLOT_TIME -eq 1 ]
then
    rm -f $fPNG
fi

#------------------------CREATE NEW DATA FILES------------------------#
if [ $FLAG_TIME -eq 1 ] 
then
    touch $fDAT
    touch $fDATaux
fi

#------------------------RUN ITERATIONS------------------------#
if [ $FLAG_TIME -eq 1 ]
then
    echo "Running slow and fast..."
    # Loop for iterations
    for i in $(seq 1 1 $REPS); do
        echo "ITERATION $i"
        for ((N = Ninicio ; N <= Nfinal ; N += Npaso)); do
            echo "N: $N / $Nfinal..."
            
            slowTime=$(../code/slow $N | grep 'time' | awk '{print $3}')
            fastTime=$(../code/fast $N | grep 'time' | awk '{print $3}')

            echo "$N	$slowTime	$fastTime" >> $fDATaux
        done
    done

    # Calculate the average time
    awk '{  slow_sum[$1]+=$2; 
            fast_sum[$1]+=$3; 
            counter[$1] += 1;} 
        END {
            for (valor in slow_sum){ 
                print valor"\t"(slow_sum[valor]/counter[valor])"\t"(fast_sum[valor]/counter[valor]);
            }
        }' $fDATaux | sort > $fDAT
fi

#------------------------CREATE FIGURES------------------------#
if [ $FLAG_PLOT_TIME -eq 1 ]
then
echo "Generating plot..."
gnuplot << END_GNUPLOT
set title "Slow-Fast Execution Time With $REPS repetitions"
set ylabel "Execution time (s)"
set xlabel "Matrix Size"
set key right bottom
set grid
set term png
set output "$fPNG"
plot "$fDAT" using 1:2 with lines lw 2 title "slow", \
     "$fDAT" using 1:3 with lines lw 2 title "fast"
replot
quit
END_GNUPLOT
fi
