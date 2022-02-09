#include "../includes/cypher.h"
#include "../includes/utils.h"
#include <stdio.h>
#include <stdlib.h>

void afin_cifrado(mpz_t x, mpz_t a, mpz_t b, mpz_t m, mpz_t y){
    mpz_mul(y, a, x);
    mpz_add(y, y, b);
    mpz_mod(y, y, m);
}

void afin_descifrado(mpz_t y, mpz_t a_inv, mpz_t b, mpz_t m, mpz_t x){
    mpz_sub(x, y, b);
    mpz_mul(x, x, a_inv);
    mpz_mod(x, x, m);
}

int* hill_cifrado(int *x, int **k, int n, int m){
    int *result = NULL;

    if (!x || !k || n < 1 || m < 1){
        fprintf(stderr, "Unable to perform Hill Cypher. Invalid arguments.\n");
        return NULL;
    }

    result = matrix_modular_mul(x, k, n, m);

    return result;
}

int* hill_descifrado(int *y, int **k_inv, int n, int m){
    int *result = NULL;

    if (!y || !k_inv || n < 1 || m < 1){
        fprintf(stderr, "Unable to perform Hill Decypher. Invalid arguments.\n");
        return NULL;
    }

    result = matrix_modular_mul(y, k_inv, n, m);

    return result;
}

int desplazamiento_cifrado(int x, int k, int m){
    int y = (x + k) % m;
    return y; 
}

int desplazamiento_descifrado(int y, int k, int m){
    int x = (y - k) % m;
    if (x < 0) x += m;
    return x;
}

int** permutacion_cifrado(int **x, int *k1, int *k2, int m, int n){
    int **matrix_intermedia = NULL;
    int **matrix_final = NULL;
    
    if (!x || !k1 || !k2 || m < 1 || n < 1){
        fprintf(stderr, "Error en cifrado por permutación. Argumentos no válidos.\n");
    }

    matrix_intermedia = matrix_swap_rows(x, k1, m, n);

    if (!matrix_intermedia) return NULL;

    matrix_final = matrix_swap_columns(matrix_intermedia, k2, m, n);

    free_matrix(matrix_intermedia, m);
    return matrix_final;
}

int** permutacion_descifrado(int **y, int *k1_op, int *k2_op, int m, int n){
    int **matrix_intermedia = NULL;
    int **matrix_final = NULL;
    
    if (!y || !k1_op || !k2_op || m < 1 || n < 1){
        fprintf(stderr, "Error en descifrado por permutación. Argumentos no válidos.\n");
    }

    matrix_intermedia = matrix_swap_columns(y, k2_op, m, n);

    if (!matrix_intermedia) return NULL;

    matrix_final = matrix_swap_rows(matrix_intermedia, k1_op, m, n);

    free_matrix(matrix_intermedia, m);
    return matrix_final;
}