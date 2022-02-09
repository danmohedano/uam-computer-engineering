/**
 * 11/11/2020
 * Módulo: des_linealidad.c
 * -----------------
 * Authors:
 * - Daniel Mohedano    <daniel.mohedano@estudiante.uam.es>
 * - Silvia Sopeña      <silvia.sopenna@estudiante.uam.es>
 * -----------------------------------------------------------
 * Este módulo comprueba la linealidad de las S-Boxes de DES.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>
#include <stdint.h>
#include <time.h>
#include "../includes/constants.h"

void get_x_y(short num, short *x, short *y){
    *x = ((num >> 5) & 1u) != 0 ? 2 : 0;
    if ((num & 1u) != 0) *x = *x + 1;

    *y = 0;
    for (int j = 4; j > 0; --j){
        *y *= 2;
        if (((num >> j) & 1u) != 0) *y += 1;
    }
}

int main(int argc, char **argv)
{   
    FILE *pf = NULL;
    int histograma[31];
    short xor_x, xor_y, a_x, a_y, b_x, b_y;
    short xor, result;

    pf = fopen("test/des/histograma.csv", "w");
    if (!pf){
        fprintf(stderr, "Error. No se pudo abrir el archivo de escritura.\n");
        exit(EXIT_FAILURE);
    }
    fprintf(pf, "Diff\tCount\n");

    for (int box = 0; box < NUM_S_BOXES; ++box){
        for (int i = 0; i < 31; ++i) histograma[i] = 0;

        for (short a = 0; a < 64; ++a){
            for (short b = a; b < 64; ++b){
                // Para cada posible pareja de A y B
                xor = a ^ b;

                get_x_y(xor, &xor_x, &xor_y);
                get_x_y(a, &a_x, &a_y);
                get_x_y(b, &b_x, &b_y);
                
                result = S_BOXES[box][xor_x][xor_y] - (S_BOXES[box][a_x][a_y] ^ S_BOXES[box][b_x][b_y]);
                histograma[result + 15] += 1;
            }
        }

        for (int i = 0; i < 31; ++i){
            fprintf(pf, "%d\t%d\n", i - 15, histograma[i]);
        }
    }
    return 0;
}