/**
 * 09/12/2020
 * Módulo: primo.c
 * -----------------
 * Authors:
 * - Daniel Mohedano    <daniel.mohedano@estudiante.uam.es>
 * - Silvia Sopeña      <silvia.sopenna@estudiante.uam.es>
 * -----------------------------------------------------------
 * Este módulo implementa el algoritmo de las Vegas.
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

void cleanup(FILE *out, mpz_t p, mpz_t q, mpz_t n, mpz_t e, mpz_t d, mpz_t result_1, mpz_t result_2, gmp_randstate_t rstate){
    if (out && out != stdout) fclose(out);
    mpz_clear(p); mpz_clear(q); mpz_clear(n); mpz_clear(e); mpz_clear(d); mpz_clear(result_1); mpz_clear(result_2); gmp_randclear(rstate);
}


int main(int argc, char **argv)
{
    int c;
    FILE *out = stdout;
    char* help_str = "Uso: vegas.exe -b bits -p sec [-o fileout]\n";
    bool error = false;

    int bits = 0;
    double prob = 0;
    char *eptr;
    mpz_t p, q, n, e, d, result_1, result_2;
    gmp_randstate_t rstate;

    // Inicialización de variables
    gmp_randinit_mt(rstate); gmp_randseed_ui(rstate, time(NULL)); 
    mpz_init(p); mpz_init(q); mpz_init(n); mpz_init(e); mpz_init(d); mpz_init(result_1); mpz_init(result_2);

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
                cleanup(out, p, q, n, e, d, result_1, result_2, rstate);
                exit(EXIT_SUCCESS);
            default:
                cleanup(out, p, q, n, e, d, result_1, result_2, rstate);
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
        cleanup(out, p, q, n, e, d, result_1, result_2, rstate);
        exit(EXIT_FAILURE);
    }

    // 1. Generar claves RSA
    gen_rsa(bits, prob, p, q, n, e, d, rstate);

    gmp_fprintf(out, "p: %#Zx\n", p);
    gmp_fprintf(out, "q: %#Zx\n", q);
    gmp_fprintf(out, "n: %#Zx\n", n);
    gmp_fprintf(out, "e: %#Zx\n", e);
    gmp_fprintf(out, "d: %#Zx\n", d);
    fprintf(out, "------------------------------------------------\n");

    // 2. Aplicar Algo. las Vegas
    fprintf(out, "Aplicando algoritmo de las Vegas\n");

    vegas(n, e, d, result_1, result_2, rstate);

    gmp_fprintf(out, "Resultado 1: %#Zx\n", result_1);
    gmp_fprintf(out, "Resultado 2: %#Zx\n", result_2);

    if ((mpz_cmp(result_1, p) == 0 && mpz_cmp(result_2, q) == 0) || (mpz_cmp(result_1, q) == 0 && mpz_cmp(result_2, p) == 0)){
        fprintf(out, "Comprobación: Resultado correcto.\n");
    }else{
        fprintf(out, "Comprobación: Resultado incorrecto.\n");
    }

    cleanup(out, p, q, n, e, d, result_1, result_2, rstate);   
    
    return 0;
}