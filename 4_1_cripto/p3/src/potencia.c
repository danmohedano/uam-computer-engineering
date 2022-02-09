/**
 * 06/12/2020
 * Módulo: potencia.c
 * -----------------
 * Authors:
 * - Daniel Mohedano    <daniel.mohedano@estudiante.uam.es>
 * - Silvia Sopeña      <silvia.sopenna@estudiante.uam.es>
 * -----------------------------------------------------------
 * Este módulo implementa la potenciación modular óptima y compara el tiempo de ejecución con la librería GMP.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>
#include <gmp.h>
#include <time.h>
#include "../includes/utils.h"

void cleanup(mpz_t base, mpz_t exponente, mpz_t modulo, mpz_t result, mpz_t result_gmp){
    mpz_clear(base); mpz_clear(exponente); mpz_clear(modulo); mpz_clear(result); mpz_clear(result_gmp);
}

int main(int argc, char **argv)
{
    if (argc != 4){
        fprintf(stderr, "Número incorrecto de argumentos. Uso: ./potencia.exe base exponente modulo\n");
        exit(EXIT_FAILURE);
    }

    mpz_t base, exponente, modulo, result, result_gmp;
    mpz_init(base); mpz_init(exponente); mpz_init(modulo); mpz_init(result); mpz_init(result_gmp);
    clock_t t_ini, t_end;

    // Cargado de argumentos
    if (mpz_set_str(base, argv[1], 16) == -1){
        fprintf(stderr, "Base inválida.\n");
        cleanup(base, exponente, modulo, result, result_gmp);
        exit(EXIT_FAILURE);
    }
    if (mpz_set_str(exponente, argv[2], 16) == -1){
        fprintf(stderr, "Exponente inválido.\n");
        cleanup(base, exponente, modulo, result, result_gmp);
        exit(EXIT_FAILURE);
    }
    if (mpz_set_str(modulo, argv[3], 16) == -1){
        fprintf(stderr, "Módulo inválido.\n");
        cleanup(base, exponente, modulo, result, result_gmp);
        exit(EXIT_FAILURE);
    }

    
    
    // Algoritmo de potenciación propio
    t_ini = clock();
    potenciacion_modular_optima(base, exponente, modulo, result);
    t_end = clock();

    printf("Algoritmo propio:\n");
    gmp_printf("Resultado: %Zd\n", result);
    printf("Tiempo: %lf (ms)\n", (double)(t_end - t_ini) * 1000.0 / CLOCKS_PER_SEC);

    // Utilizando función GMP
    t_ini = clock();
    mpz_powm(result_gmp, base, exponente, modulo);
    t_end = clock();

    printf("Algoritmo GMP:\n");
    gmp_printf("Resultado: %Zd\n", result);
    printf("Tiempo: %lf (ms)\n", (double)(t_end - t_ini) * 1000.0 / CLOCKS_PER_SEC);

    if (mpz_cmp(result, result_gmp) == 0){
        printf("Resultado correcto.\n");
    }else{
        printf("Resultado incorrecto.\n");
    }

    cleanup(base, exponente, modulo, result, result_gmp);
    
    exit(EXIT_SUCCESS);
}