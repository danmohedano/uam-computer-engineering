# Script for Exercise2.5 Practice 4

#!/bin/bash

#------------------------INITIALIZE VARIABLES------------------------#

# Configuration variables
REPS=5
Ninicio=5000000
Npaso=34500000
Nfinal=350000000
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
        serieTime=$(./pescalar_serie $N | grep 'Tiempo' | awk '{print $2}')

        line=""
        # Iterate over the number of threads
        for n_thread in $(seq $n_cores); do
            echo "      Thread: $n_thread / $n_cores..."
            parTime=$(./pescalar_par3 $N $n_thread | grep 'Tiempo' | awk '{print $2}')
            line+="$parTime    "
        done

        echo "$N    $serieTime    $line" >> $fDATaux
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
set title "Execution times for 5 iterations"
set ylabel "Execution Time (s)"
set xlabel "Vector Size"
set key left center
set grid
set term png
set output "$fPNGtimes"
plot "$fDAT" using 1:2 with lines lw 2 title "Serie", \
     "$fDAT" using 1:3 with lines lw 2 title "Par-Threads-1", \
     "$fDAT" using 1:4 with lines lw 2 title "Par-Threads-2", \
     "$fDAT" using 1:5 with lines lw 2 title "Par-Threads-3", \
     "$fDAT" using 1:6 with lines lw 2 title "Par-Threads-4", \
     "$fDAT" using 1:7 with lines lw 2 title "Par-Threads-5", \
     "$fDAT" using 1:8 with lines lw 2 title "Par-Threads-6", \
     "$fDAT" using 1:9 with lines lw 2 title "Par-Threads-7", \
     "$fDAT" using 1:10 with lines lw 2 title "Par-Threads-8"     
replot
quit
END_GNUPLOT

echo "Generating plot for acceleration..."
gnuplot << END_GNUPLOT
set title "Accelerations for 5 iterations"
set ylabel "Acceleration"
set xlabel "Vector Size"
set key left center
set grid
set term png
set output "$fPNGacc"
plot "$fDATacc" using 1:2 with lines lw 2 title "Serie", \
     "$fDATacc" using 1:3 with lines lw 2 title "Par-Threads-1", \
     "$fDATacc" using 1:4 with lines lw 2 title "Par-Threads-2", \
     "$fDATacc" using 1:5 with lines lw 2 title "Par-Threads-3", \
     "$fDATacc" using 1:6 with lines lw 2 title "Par-Threads-4", \
     "$fDATacc" using 1:7 with lines lw 2 title "Par-Threads-5", \
     "$fDATacc" using 1:8 with lines lw 2 title "Par-Threads-6", \
     "$fDATacc" using 1:9 with lines lw 2 title "Par-Threads-7", \
     "$fDATacc" using 1:10 with lines lw 2 title "Par-Threads-8"     
replot
quit
END_GNUPLOT

