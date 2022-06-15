# Script para test y plot de resultados

#!/bin/bash

# -- VARIABLES -- #
FLAG_REAL=0
FLAG_NORM=0
FLAG_EXTRA=1

EJERCICIO2=( 1 2 3 5 )
EJERCICIO3=( 4 6 )


# -- EJERCICIO 2 -- #
# Problemas reales 1 2 3 y 5 (sin normalización)

if [[ $FLAG_REAL -eq 1 ]]
then
    for p in "${EJERCICIO2[@]}"; do
        echo "PROBLEMA REAL ${p}"
        echo "================"
        mkdir p$p
        rm "p${p}/files.txt"
        
        alphas=( 1 0.1 0.01 0.001 0.0001 )
        alpha=0.01
        paciencias=( 10 20 30 40 50 )
        paciencia=30
        layers=( 5 10 15 "5 5" "10 10" )
        layer=15
        epochs=500
        portion=0.6

        for a in "${alphas[@]}"
        do
            echo "Alpha=${a}"
            python3 ../src/main.py 1 "../data/problema_real$p.txt" $a $epochs $portion -hidden_layers $layer -val -wait $paciencia > "p${p}/${a}-${epochs}-${paciencia}-${layer}.dat"
            echo "p${p}/${a}-${epochs}-${paciencia}-${layer}.dat" >> "p${p}/files.txt"
        done

        echo "=" >> "p${p}/files.txt"

        for pac in "${paciencias[@]}"
        do
            echo "Wait=${pac}"
            python3 ../src/main.py 1 "../data/problema_real$p.txt" $alpha $epochs $portion -hidden_layers $layer -val -wait $pac > "p${p}/${alpha}-${epochs}-${pac}-${layer}.dat"
            echo "p${p}/${alpha}-${epochs}-${pac}-${layer}.dat" >> "p${p}/files.txt"
        done

        echo "=" >> "p${p}/files.txt"
        
        for l in "${layers[@]}"
        do
            echo "Layer=${l}"
            python3 ../src/main.py 1 "../data/problema_real$p.txt" $alpha $epochs $portion -hidden_layers $l -val -wait $paciencia > "p${p}/${alpha}-${epochs}-${paciencia}-${l}.dat"
            echo "p${p}/${alpha}-${epochs}-${paciencia}-${l}.dat" >> "p${p}/files.txt"
        done
    done
fi

if [[ $FLAG_NORM -eq 1 ]]
then
    for p in "${EJERCICIO3[@]}"; do
        echo "PROBLEMA REAL ${p}"
        echo "================"
        mkdir p$p
        rm "p${p}/files.txt"
        
        alphas=( 1 0.1 0.01 0.001 0.0001 )
        alpha=0.01
        paciencias=( 10 20 30 40 50 )
        paciencia=30
        layers=( 5 10 15 "5 5" "10 10" )
        layer=15
        epochs=500
        portion=0.6

        for a in "${alphas[@]}"
        do
            echo "Alpha=${a}"
            python3 ../src/main.py 1 "../data/problema_real$p.txt" $a $epochs $portion -hidden_layers $layer -val -wait $paciencia -norm > "p${p}/${a}-${epochs}-${paciencia}-${layer}.dat"
            echo "p${p}/${a}-${epochs}-${paciencia}-${layer}.dat" >> "p${p}/files.txt"
        done

        echo "=" >> "p${p}/files.txt"

        for pac in "${paciencias[@]}"
        do
            echo "Wait=${pac}"
            python3 ../src/main.py 1 "../data/problema_real$p.txt" $alpha $epochs $portion -hidden_layers $layer -val -wait $pac -norm > "p${p}/${alpha}-${epochs}-${pac}-${layer}.dat"
            echo "p${p}/${alpha}-${epochs}-${pac}-${layer}.dat" >> "p${p}/files.txt"
        done

        echo "=" >> "p${p}/files.txt"
        
        for l in "${layers[@]}"
        do
            echo "Layer=${l}"
            python3 ../src/main.py 1 "../data/problema_real$p.txt" $alpha $epochs $portion -hidden_layers $l -val -wait $paciencia -norm > "p${p}/${alpha}-${epochs}-${paciencia}-${l}.dat"
            echo "p${p}/${alpha}-${epochs}-${paciencia}-${l}.dat" >> "p${p}/files.txt"
        done
    done
fi

if [[ $FLAG_EXTRA -eq 1 ]]
then
    echo "GRID SEARCH PROBLEMA 2"
    alphas=( 1 0.1 0.01 0.001 0.0001 )
    paciencias=( 10 20 30 40 50 )
    layers=( 5 10 15 "5 5" "10 10" )
    epochs=500
    portion=0.7

    for alpha in "${alphas[@]}"
    do
        for pac in "${paciencias[@]}"
        do
            for l in "${layers[@]}"
            do
                echo "A=${alpha},P=${pac},L=${l}"
                python3 ../src/main.py 1 "../data/problema_real2.txt" $alpha $epochs $portion -hidden_layers $l -val -wait $pac | tail -n 1
            done
        done
    done

    echo "5000 ITERACIONES PROBLEMA 6"
    python3 ../src/main.py 1 "../data/problema_real6.txt" 0.1 5000 0.7 -hidden_layers 20 -norm > ejecucion_6.dat
fi
