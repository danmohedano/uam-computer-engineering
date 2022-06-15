# Script para test y plot de resultados

#!/bin/bash

# -- VARIABLES -- #
FLAG_LOGIC=0
FLAG_REAL1=0
FLAG_REAL2=1
FLAG_REAL2_FINAL=0

LOGIC_FILES=( "../data/and.txt" "../data/or.txt" "../data/nand.txt" "../data/xor.txt" )
LOGIC_GATES=( "AND" "OR" "NAND" "XOR" )


# -- EJERCICIO 4.1 -- #
# Fronteras de decisión para problemas lógicos

if [[ $FLAG_LOGIC -eq 1 ]]
then
    echo "PROBLEMAS LÓGICOS"
    echo "================="
    echo "PERCEPTRON"
    echo "----------"
    for gate in $(seq 0 1 3); do
        echo "Operación: ${LOGIC_GATES[$gate]}" 
        python3 ../src/main.py perceptron 2 ${LOGIC_FILES[$gate]} 1 50 0.2 -frontera
        echo ""
    done
    echo "----------"
    echo "ADALINE"
    echo "-------"
    for gate in $(seq 0 1 3); do
        echo "Operación: ${LOGIC_GATES[$gate]}" 
        python3 ../src/main.py adaline 2 ${LOGIC_FILES[$gate]} 0.1 50 0.001 -frontera
        echo ""
    done
    echo "==============="
fi

# -- EJERCICIO 4.2 -- #
# Problema Real 1

if [[ $FLAG_REAL1 -eq 1 ]]
then
    echo "PROBLEMA REAL 1"
    echo "==============="
    echo "PERCEPTRON"
    echo "----------"
    umbral=0.2
    umbrales=( 0.1 0.2 0.3 0.4 )
    const=0.01
    constantes=( 1 0.1 0.01 0.001 )
    epochs=200
    portion=0.25

    for alpha in "${constantes[@]}"
    do
        echo "Alpha=${alpha}"
        python3 ../src/main.py perceptron 1 "../data/problema_real1.txt" $alpha $epochs $umbral -portion $portion > "perceptron_alpha_${alpha}.dat"
    done

    for um in "${umbrales[@]}"
    do
        echo "Umbral=${um}"
        python3 ../src/main.py perceptron 1 "../data/problema_real1.txt" $const $epochs $um -portion $portion > "perceptron_umbral_${um}.dat"
    done


    echo "----------"
    echo "ADALINE"
    echo "-------"

    constantes=( 0.1 0.01 0.001 )
    tolerancias=( 0.1 0.01 0.001 0.0001)
    tol=0.0001

    for alpha in "${constantes[@]}"
    do
        echo "Alpha=${alpha}"
        python3 ../src/main.py adaline 1 "../data/problema_real1.txt" $alpha $epochs $tol -portion $portion > "adaline_alpha_${alpha}.dat"
    done

    for t in "${tolerancias[@]}"
    do
        echo "Tolerancia=${t}"
        python3 ../src/main.py adaline 1 "../data/problema_real1.txt" $const $epochs $t -portion $portion > "adaline_tol_${t}.dat"
    done

    echo "==============="
fi


if [[ $FLAG_REAL2 -eq 1 ]]
then
    echo "PROBLEMA REAL 2"
    echo "==============="
    echo "PERCEPTRON"
    echo "----------"
    umbrales=( 0.1 0.2 0.3 0.4 )
    constantes=( 1 0.1 0.01 0.001 )
    epochs=2000
    portion=0.25

    for alpha in "${constantes[@]}"
    do
        for um in "${umbrales[@]}"
        do
            echo "Alpha=${alpha}, Umbral=${um}"
            python3 ../src/main.py perceptron 1 "../data/problema_real2.txt" $alpha $epochs $um -portion $portion | tail -n 1
        done
    done


    echo "----------"
    echo "ADALINE"
    echo "-------"

    constantes=( 0.1 0.01 0.001 )
    tolerancias=( 0.1 0.01 0.001 0.0001)

    for alpha in "${constantes[@]}"
    do
        for t in "${tolerancias[@]}"
        do
            echo "Alpha=${alpha}, Tolerancia=${t}"
            python3 ../src/main.py adaline 1 "../data/problema_real2.txt" $alpha $epochs $t -portion $portion | tail -n 1
        done
    done

    

    echo "==============="
fi

if [[ $FLAG_REAL2_FINAL -eq 1 ]]
then
    python3 ../src/main.py perceptron 3 "../data/problema_real2.txt" 1 200 0.1 --file_test "../data/problema_real2_no_etiquetados.txt" -predicciones
    python3 ../src/main.py adaline 3 "../data/problema_real2.txt" 0.01 200 0.0001 --file_test "../data/problema_real2_no_etiquetados.txt" -predicciones
fi