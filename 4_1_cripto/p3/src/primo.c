/**
 * 06/12/2020
 * Módulo: primo.c
 * -----------------
 * Authors:
 * - Daniel Mohedano    <daniel.mohedano@estudiante.uam.es>
 * - Silvia Sopeña      <silvia.sopenna@estudiante.uam.es>
 * -----------------------------------------------------------
 * Este módulo implementa el algoritmo de Miller-Rabin de generación de primos.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>
#include <stdint.h>
#include <gmp.h>
#include <time.h>
#include <math.h>
#include "../includes/constants.h"
#include "../includes/utils.h"

void cleanup(FILE *out, mpz_t p, gmp_randstate_t rstate){
    if (out && out != stdout) fclose(out);
    mpz_clear(p); gmp_randclear(rstate);
}

int main(int argc, char **argv)
{
    int c;
    FILE *out = stdout;
    char* help_str = "Uso: primo.exe -b bits -p sec [-o fileout]\n";
    bool error = false;

    int bits = 0, iter;
    double prob = 0, aux;
    char *eptr;
    mpz_t p;
    gmp_randstate_t rstate;

    // Inicialización de variables
    gmp_randinit_mt(rstate); gmp_randseed_ui(rstate, time(NULL)); 
    mpz_init(p);

    // Parseo de argumentos
    while ((c = getopt (argc, argv, "b:p:o:h")) != -1){
        switch (c){
            case 'b':
                bits = atoi(optarg);
                break;
            case 'p':
                prob = strtod(optarg, &eptr);
                break;
            case 'o':
                out = fopen(optarg, "w");
                if (!out){
                    fprintf(stderr, "Error. No se pudo abrir el archivo de escritura.\n");
                    out = NULL;
                    error = true;
                }
                break;
            case 'h':
                fprintf(stderr, "%s", help_str);
                cleanup(out, p, rstate);
                exit(EXIT_SUCCESS);
            default:
                cleanup(out, p, rstate);
                exit(EXIT_FAILURE);
        }
    }

    if (bits <= 0){
        fprintf(stderr, "Error. Proporciona un número de bits válido.\n");
        error = true;
    }

    if (prob <= 0){
        fprintf(stderr, "Error. Proporciona una probabilidad válida.\n");
        error = true;
    }

    if (error){
        cleanup(out, p, rstate);
        exit(EXIT_FAILURE);
    }

    // Calcular cantidad de tests necesarios para asegurar probabilidad de error
    aux = log((bits * log(2) - 1) * ((1 / prob) - 1)) / log(4);
    iter = ceil(aux);

    clock_t t_ini, t_end;
    t_ini = clock();

    // 1. Generar número aleatorio P
    candidato_aleatorio(p, rstate, bits);

    int counter = 1;

    while (miller_rabin(p, iter)){
        mpz_add_ui(p, p, 2);
        ++counter;
    }

    t_end = clock();

    // Devolver información. 
    gmp_fprintf(out, "Candidato: %#Zx\n", p);
    fprintf(out, "Resultado test: Posible primo.\n");
    fprintf(out, "Resultado GMP: ");
    int result_gmp = mpz_probab_prime_p(p, iter);
    if (result_gmp == 0){
        fprintf(out, "Compuesto\n");
    } else if (result_gmp == 1){
        fprintf(out, "Posible primo.\n");
    } else {
        fprintf(out, "Primo\n");
    }

    fprintf(out, "Seguridad del primo: %e [m = %d]\n", 1.0 / (1.0 + (pow(4, iter) * 1.0 / (bits * log(2)))), iter);
    fprintf(out, "Tiempo de generación: %lf (ms)\n", (double)(t_end - t_ini) * 1000.0 / CLOCKS_PER_SEC);
    fprintf(out, "Candidatos generados: %d\n", counter);


    cleanup(out, p, rstate);    
    
    return 0;
}