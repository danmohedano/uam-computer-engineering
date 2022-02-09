# Script for Exercise 3.3 Practice 4

#!/bin/bash

#------------------------INITIALIZE VARIABLES------------------------#

# Configuration variables
REPS=5
Pair=10
P=$(($Pair % 7 + 4))
Ninicio=$(( 512 + $P ))
Npaso=64
Nfinal=$(( 1024 + 1024 + $P ))
n_physical_cores=4
n_cores=$((2*$n_physical_cores))

# Data files
fDAT="data/data_reps_${REPS}.dat"
fDATacc="data/data_acc_reps_${REPS}.dat"
fDATaux="data/data_aux.dat"
fPNGtimes="plot/times.png"
fPNGacc="plot/acc.png"

#------------------------CREATE DIRECTORIES------------------------#
mkdir -p data
mkdir -p plot

#------------------------DELETE PREVIOUS FILES------------------------#
rm -rf $fDAT $fDATaux $fPNGtimes $fDATacc $fPNGacc

#------------------------CREATE NEW DATA FILES------------------------#
touch $fDATaux
touch $fDAT
touch $fDATacc

#------------------------RUN ITERATIONS------------------------#

# Run various iterations
for i in $(seq $REPS); do
    echo "Iteration: $i / $REPS..."
    # Iterate over sizes
    for ((N = Ninicio ; N <= Nfinal ; N += Npaso)); do
        echo "  N: $N / $Nfinal..."
        serieTime=$(./multiplication_serie $N | grep 'time' | awk '{print $3}')
        parTime=$(./multiplication_par3 $N $n_cores | grep 'time' | awk '{print $3}')

        echo "$N    $serieTime    $parTime" >> $fDATaux
    done
done

# Calculate the average for each size
awk '{  for (i=2;i<=NF;i++){
            sum[$1,i] += $i;
        }
        sizes[$1] = $1
        counter[$1] += 1;} 
        END {
            for (size in sizes){ 
                str = sprintf("%d", size);
                for (i=2;i<=NF;i++){
                    str = sprintf("%s\t%f",str,sum[size,i]/counter[size]);
                }
                print str
            }
        }' $fDATaux | sort -n > $fDAT

# Calculate the acceleration
awk '{  str = sprintf("%d", $1);
        for (i=2;i<=NF;i++){
            str = sprintf("%s\t%f", str, $2/$i);
        }
        print str
    }' $fDAT | sort -n > $fDATacc

#------------------------PLOT FIGURES------------------------#
echo "Generating plot for execution times..."
gnuplot << END_GNUPLOT
set title "Execution times for $REPS iterations"
set ylabel "Execution Time (s)"
set xlabel "Matrix Size"
set key left center
set grid
set term png
set output "$fPNGtimes"
plot "$fDAT" using 1:2 with lines lw 2 title "Serie", \
     "$fDAT" using 1:3 with lines lw 2 title "Par"  
replot
quit
END_GNUPLOT

echo "Generating plot for acceleration..."
gnuplot << END_GNUPLOT
set title "Accelerations for $REPS iterations"
set ylabel "Acceleration"
set xlabel "Matrix Size"
set key left center
set grid
set term png
set output "$fPNGacc"
plot "$fDATacc" using 1:2 with lines lw 2 title "Serie", \
     "$fDATacc" using 1:3 with lines lw 2 title "Par"     
replot
quit
END_GNUPLOT

