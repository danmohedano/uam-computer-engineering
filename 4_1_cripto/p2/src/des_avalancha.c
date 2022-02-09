/**
 * 11/11/2020
 * Módulo: des_avalancha.c
 * -----------------
 * Authors:
 * - Daniel Mohedano    <daniel.mohedano@estudiante.uam.es>
 * - Silvia Sopeña      <silvia.sopenna@estudiante.uam.es>
 * -----------------------------------------------------------
 * Este módulo comprueba el efecto avalancha del DES.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>
#include <stdint.h>
#include <time.h>
#include "../includes/constants.h"
#include "../includes/des.h"

void gen_round_outputs(uint64_t input, uint64_t seed, uint64_t outputs[17]){
    uint64_t sub_key[16], future_key = 0;

    // 1. Generación de las subclaves para cada ronda
    sub_key[0] = seed;
    for (int i = 0; i < 16; ++i){
        key_round(&sub_key[i], &future_key, i);
        if (i < 15){
            sub_key[i + 1] = future_key;
        }   
    }

    // 2. Aplicar 16 rondas Feistel
    uint64_t round_result = input;
    outputs[0] = input;
    for (int i = 0; i < 16; ++i){
        des_round(&round_result, sub_key[i]);
        outputs[i + 1] = round_result;
    }
}

void print_results(uint64_t out1[17], uint64_t out2[17]){
    uint64_t xor;
    int counter;
    for (int i = 0; i < 17; ++i){
        xor = out1[i] ^ out2[i];

        counter = 0;
        for (int j = 0; j < 64; ++j){
            if (((xor >> j) & 1u) != 0) ++counter;
        }

        printf("Ronda %2d: %2d\n", i, counter);
    }
}

int main(int argc, char **argv)
{   
    uint64_t input1 = 0x0000000000000000;
    uint64_t input2 = 0x0000000000000001;
    uint64_t key1 = 0x58e0136b6e923da8;
    uint64_t key2 = 0x58e0136b6e923da9;

    uint64_t outputs1[17], outputs2[17];

    // Test avalancha en bloque
    gen_round_outputs(input1, key1, outputs1);
    gen_round_outputs(input2, key1, outputs2);

    printf("Avalancha Bloques\nRonda  i: # bits diferentes\n");
    print_results(outputs1, outputs2);

    // Test avalancha en clave
    gen_round_outputs(input1, key1, outputs1);
    gen_round_outputs(input1, key2, outputs2);

    printf("Avalancha Clave\nRonda  i: # bits diferentes\n");
    print_results(outputs1, outputs2);

    return 0;
}