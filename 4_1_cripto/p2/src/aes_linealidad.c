/**
 * 11/11/2020
 * Módulo: aes_linealidad.c
 * -----------------
 * Authors:
 * - Daniel Mohedano    <daniel.mohedano@estudiante.uam.es>
 * - Silvia Sopeña      <silvia.sopenna@estudiante.uam.es>
 * -----------------------------------------------------------
 * Este módulo comprueba la linealidad de las S-Boxes de AES.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>
#include <stdint.h>
#include <time.h>
#include "../includes/constants.h"

void get_x_y(short num, short *x, short *y){
    short mask = 0x000F;

    *x = (num >> 4) & mask;
    *y = num & mask;
}

int main(int argc, char **argv)
{   
    FILE *pf = NULL;
    int histograma[2][511];
    short s_xor, s_a, s_b;
    short xor_x, xor_y, a_x, a_y, b_x, b_y;
    short xor, result;

    pf = fopen("test/aes/histograma.csv", "w");
    if (!pf){
        fprintf(stderr, "Error. No se pudo abrir el archivo de escritura.\n");
        exit(EXIT_FAILURE);
    }
    fprintf(pf, "Diff\tCount\n");

    for (int box = 0; box < 2; ++box){
        for (int i = 0; i < 511; ++i) histograma[box][i] = 0;
    }
    
    for (int box = 0; box < 2; ++box){
        for (short a = 0; a < 256; ++a){
            for (short b = a; b < 256; ++b){
                // Para cada posible pareja de A y B
                xor = a ^ b;

                get_x_y(xor, &xor_x, &xor_y);
                get_x_y(a, &a_x, &a_y);
                get_x_y(b, &b_x, &b_y);

                if (box == 0){
                    sscanf(DIRECT_SBOX[xor_x][xor_y], "%hx", &s_xor);
                    sscanf(DIRECT_SBOX[a_x][a_y], "%hx", &s_a);
                    sscanf(DIRECT_SBOX[b_x][b_y], "%hx", &s_b);
                }else{
                    sscanf(INVERSE_SBOX[xor_x][xor_y], "%hx", &s_xor);
                    sscanf(INVERSE_SBOX[a_x][a_y], "%hx", &s_a);
                    sscanf(INVERSE_SBOX[b_x][b_y], "%hx", &s_b);
                }
                
                result =  s_xor - (s_a ^ s_b);
                histograma[box][result + 255] += 1;
            }
        }
    }

    for (int box = 0; box < 2; ++box){
        for (int i = 0; i < 511; ++i){
            fprintf(pf, "%d\t%d\n", i - 255, histograma[box][i]);
        }
    }
    

    return 0;
}