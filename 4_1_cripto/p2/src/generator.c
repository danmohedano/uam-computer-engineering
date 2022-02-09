/**
 * 11/11/2020
 * Módulo: generator.c
 * -----------------
 * Authors:
 * - Daniel Mohedano    <daniel.mohedano@estudiante.uam.es>
 * - Silvia Sopeña      <silvia.sopenna@estudiante.uam.es>
 * -----------------------------------------------------------
 * Este módulo genera claves e IVs aleatorios.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>
#include <stdint.h>
#include <time.h>
#include "../includes/constants.h"

int main(int argc, char **argv)
{
    int c;
    char* help_str = "Uso: generator.exe {-K #} {-V}\n";

    int n_keys = 0;
    bool iv_gen = false;
    srand(time(0));

    // Parseo de argumentos
    while ((c = getopt (argc, argv, "K:Vh")) != -1){
        switch (c){
            case 'K':
                n_keys = atoi(optarg);
                break;
            case 'V':
                iv_gen = true;
                break;
            case 'h':
                fprintf(stderr, "%s", help_str);
                exit(EXIT_SUCCESS);
            default:
                exit(EXIT_FAILURE);
        }
    }

    uint64_t key = 0;
    int ones;
    uint64_t iv = 0;

    for (int i = 0; i < n_keys; ++i){
        // Se genera clave aleatoria
        key = rand();
        key <<= 32;
        key += rand();

        // Se fuerza a que cumpla la condición de paridad
        for (int group = 0; group < 8; ++group){
            ones = 1;
            for (int j = 0; j < 7; ++j){
                if (((key << (group*8 + j)) & FIRST_BIT) != 0) ++ones;
            }

            ones = ones % 2;

            // Se pone el bit de paridad con el valor correcto
            if (ones == 0){
                key = key & ~((FIRST_BIT) >> (group*8 + 7));
            }else{
                key = key | (FIRST_BIT >> (group*8 + 7));
            }
        }

        printf("Key[%d] = 0x%016lx\n", i, key);
    }

    if (iv_gen){
        iv = rand();
        iv <<= 32;
        iv += rand();
        printf("IV = 0x%016lx\n", iv);
    }
    
    return 0;
}