# Script for Exercise 3 Practice 3

#!/bin/bash

#------------------------INITIALIZE VARIABLES------------------------#
# Flags to determine execution of the script (select sections to execute)
echo "REMEMBER TO SET THE FLAGS IN THE SCRIPT TO SELECT WHICH SECTIONS ARE EXECUTED"
FLAG_TIME=0
FLAG_VALGRIND=0
FLAG_PLOT_TIME=0
FLAG_PLOT_VALGRIND=0

# Configuration variables
REPS=8
Pair=10
P=$(($Pair % 7 + 4))
Ninicio=$((256 + (256 * $P)))
Npaso=32
Nfinal=$(($Ninicio + 256))

# Time data files
fDATtimeAux="data/mult_time_aux.dat"
fDATtime="data/mult_time_reps_${REPS}.dat"
fPNGtime="plot/mult_time_reps_${REPS}.png"

# Valgrind data files
fDATvalgrind="data/mult_cache.dat"
fDATvalgrindRegular="data/mult_cache_regular.dat"
fDATvalgrindTransposed="data/mult_cache_transposed.dat"
fPNGread="plot/mult_cache_read.png"
fPNGwrite="plot/mult_cache_write.png"

#------------------------CREATE DIRECTORIES------------------------#
mkdir -p data
mkdir -p plot

#------------------------DELETE PREVIOUS FILES------------------------#
if [ $FLAG_TIME -eq 1 ]
then
    # Delete time files
    rm -f $fDATtime $fDATtimeAux
fi

if [ $FLAG_PLOT_TIME -eq 1 ]
then
    # Delete time figures
    rm -f $fPNGtime
fi

if [ $FLAG_VALGRIND -eq 1 ]
then
    # Delete valgrind files
    rm -f  $fDATvalgrind $fDATvalgrindRegular $fDATvalgrindTransposed
fi

if [ $FLAG_PLOT_VALGRIND -eq 1 ]
then
    # Delete valgrind figures
    rm -f $fPNGread $fPNGwrite
fi

#------------------------CREATE NEW DATA FILES------------------------#
if [ $FLAG_TIME -eq 1 ]
then
    touch $fDATtime
    touch $fDATtimeAux
fi

if [ $FLAG_VALGRIND -eq 1 ]
then
    touch $fDATvalgrind
fi

#------------------------RUN ITERATIONS------------------------#
if [ $FLAG_TIME -eq 1 ]
then
    echo "Running regular and transposed multiplication..."
    # Loop for iterations with the loop for matrix sizes inside
    for i in $(seq 1 1 $REPS); do
        echo "ITERATION $i"
        for ((N = Ninicio ; N <= Nfinal ; N += Npaso)); do
            echo "N: $N / $Nfinal..."
            # Execute regular and transposed programs and store the times in the auxiliary files
            regularTime=$(./regular $N | grep 'time' | awk '{print $3}')
            transposedTime=$(./transposed $N | grep 'time' | awk '{print $3}')

            echo "$N	$regularTime	$transposedTime" >> $fDATtimeAux
        done
    done

    # Calculate the average for each size
    awk '{  regular_sum[$1]+=$2; 
            transposed_sum[$1]+=$3; 
            counter[$1] += 1;} 
        END {
            for (valor in regular_sum){ 
                print valor"\t"(regular_sum[valor]/counter[valor])"\t"(transposed_sum[valor]/counter[valor]);
            }
        }' $fDATtimeAux | sort > $fDATtime
fi


#------------------------RUN VALGRIND------------------------#
if [ $FLAG_VALGRIND -eq 1 ]
then
    # For loop to test every matrix size in valgrind
    echo "Running valgrind"
    for ((N = Ninicio ; N <= Nfinal ; N += Npaso)); do
        echo "N: $N / $Nfinal..."

        valgrind --tool=cachegrind --cachegrind-out-file=$fDATvalgrindRegular ./regular $N
        valgrind --tool=cachegrind --cachegrind-out-file=$fDATvalgrindTransposed ./transposed $N

        # Obtain the data from the output files and store it in the relevant file
        d1mrregular=$(cg_annotate $fDATvalgrindRegular | grep 'PROGRAM TOTALS' | awk '{print $5}')
        d1mwregular=$(cg_annotate $fDATvalgrindRegular | grep 'PROGRAM TOTALS' | awk '{print $8}')
        d1mrtransposed=$(cg_annotate $fDATvalgrindTransposed | grep 'PROGRAM TOTALS' | awk '{print $5}')
        d1mwtransposed=$(cg_annotate $fDATvalgrindTransposed | grep 'PROGRAM TOTALS' | awk '{print $8}')

        echo "$N    $d1mrregular   $d1mwregular   $d1mrtransposed   $d1mwtransposed" >> $fDATvalgrind
    done

    # Remove the commas for each 10^3 position (gives errors when printing in gnuplot)
    sed -i 's/\([0-9]\),/\1/g' $fDATvalgrind
fi

#------------------------CREATE FIGURES------------------------#
if [ $FLAG_PLOT_TIME -eq 1 ]
then
# Create Figure for the execution times
echo "Generating time plot..."
gnuplot << END_GNUPLOT
set title "Multiplication Execution Time With $REPS repetitions"
set ylabel "Execution time (s)"
set xlabel "Matrix Size"
set key right bottom
set grid
set term png
set output "$fPNGtime"
plot "$fDATtime" using 1:2 with lines lw 2 title "regular", \
    "$fDATtime" using 1:3 with lines lw 2 title "transposed"
replot
quit
END_GNUPLOT
fi

if [ $FLAG_PLOT_VALGRIND -eq 1 ]
then
# Create Figure for the read misses
echo "Generating cache read plot..."
gnuplot << END_GNUPLOT
set title "Multiplication Read Misses"
set ylabel "Read Misses"
set xlabel "Matrix Size"
set key right bottom
set grid
set term png
set output "$fPNGread"
plot "$fDATvalgrind" using 1:2 with lines lw 2 title "regular-read", \
     "$fDATvalgrind" using 1:4 with lines lw 2 title "transposed-read"
replot
quit
END_GNUPLOT

# Create Figure for the write misses
echo "Generating cache write plot..."
gnuplot << END_GNUPLOT
set title "Multiplication Write Misses"
set ylabel "Write Misses"
set xlabel "Matrix Size"
set key right bottom
set grid
set term png
set output "$fPNGwrite"
plot "$fDATvalgrind" using 1:3 with lines lw 2 title "regular-write", \
     "$fDATvalgrind" using 1:5 with lines lw 2 title "transposed-write"
replot
quit
END_GNUPLOT
fi
