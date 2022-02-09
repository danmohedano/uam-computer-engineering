/**
 * 07/10/2021
 * Módulo: cypher
 * -----------------
 * Autores:
 * - Daniel Mohedano    <daniel.mohedano@estudiante.uam.es>
 * - Silvia Sopeña      <silvia.sopenna@estudiante.uam.es>
 * -----------------------------------------------------------
 * Este módulo alberga las funciones encargadas de cifrado y descifrado.
 */

#ifndef CYPHER_H
#define CYPHER_H

#include <gmp.h>
#include <stdint.h>

/**
 * afin_cifrado
 * 
 * Aplica la operación de cifrado del cifrado Afín: y = x*a + b mod m.
 * 
 * Inputs:
 *      x (mpz_t): Valor a cifrar.
 *      a (mpz_t): Clave multiplicativa.
 *      b (mpz_t): Clave aditiva.
 *      m (mpz_t): Módulo a aplicar.
 * Outputs:
 *      y (mpz_t): Resultado del cifrado.
 */
void afin_cifrado(mpz_t x, mpz_t a, mpz_t b, mpz_t m, mpz_t y);

/**
 * afin_descifrado
 * 
 * Aplica la operación de descifrado del cifrado Afín: x = (y-b)*a^-1 mod m.
 * 
 * Inputs:
 *      y (mpz_t): Valor a descifrar.
 *      a_inv (mpz_t): Clave multiplicativa inversa.
 *      b (mpz_t): Clave aditiva.
 *      m (mpz_t): Módulo a aplicar.
 * Outputs:
 *      x (mpz_t): Resultado del descifrado.
 */
void afin_descifrado(mpz_t y, mpz_t a_inv, mpz_t b, mpz_t m, mpz_t x);

/**
 * hill_cifrado
 * 
 * Aplica la operación de cifrado del cifrado de Hill.
 * 
 * Inputs:
 *      x (int*): Bloque a cifrar.
 *      k (int**): Clave de cifrado.
 *      n (int): Dimensión del bloque y clave.
 *      m (int): Módulo a aplicar.
 * Outputs:
 *      int*: Bloque cifrado. Se debe liberar la memoria tras su uso.
 */
int* hill_cifrado(int *x, int **k, int n, int m);

/**
 * hill_descifrado
 * 
 * Aplica la operación de descifrado del cifrado de Hill.
 * 
 * Inputs:
 *      y (int*): Bloque a descifrar.
 *      k_inv (int**): Clave de cifrado inversa.
 *      n (int): Dimensión del bloque y clave.
 *      m (int): Módulo a aplicar.
 * Outputs:
 *      int*: Bloque descifrado. Se debe liberar la memoria tras su uso.
 */
int* hill_descifrado(int *y, int **k_inv, int n, int m);

/**
 * desplazamiento_cifrado
 * 
 * Aplica la operación de cifrado del cifrado por desplazamiento: y = x+k mod m
 * 
 * Inputs:
 *      x (int): Valor a cifrar.
 *      k (int): Clave.
 *      m (int): Módulo a aplicar.
 * Outputs:
 *      int: Valor cifrado.
 */
int desplazamiento_cifrado(int x, int k, int m);

/**
 * desplazamiento_descifrado
 * 
 * Aplica la operación de descifrado del cifrado por desplazamiento: y = x+k mod m
 * 
 * Inputs:
 *      y (int): Valor a descifrar.
 *      k (int): Clave.
 *      m (int): Módulo a aplicar.
 * Outputs:
 *      int: Valor descifrado.
 */
int desplazamiento_descifrado(int y, int k, int m);

/**
 * permutacion_cifrado
 * 
 * Aplica la operación de cifrado del cifrado por permutación.
 * 
 * Inputs:
 *      x (int**): Matriz a cifrar.
 *      k1 (int*): Permutación de filas.
 *      k2 (int*): Permutación de columnas.
 *      m (int): Filas de la matriz.
 *      n (int): Columnas de la matriz.
 * Outputs:
 *      int**: Matriz cifrada. Se debe liberar la memoria tras su uso.
 */
int** permutacion_cifrado(int **x, int *k1, int *k2, int m, int n);

/**
 * permutacion_descifrado
 * 
 * Aplica la operación de descifrado del cifrado por permutación.
 * 
 * Inputs:
 *      x (int**): Matriz a descifrar.
 *      k1_op (int*): Permutación opuesta de filas.
 *      k2_op (int*): Permutación opuesta de columnas.
 *      m (int): Filas de la matriz.
 *      n (int): Columnas de la matriz.
 * Outputs:
 *      int**: Matriz descifrada. Se debe liberar la memoria tras su uso.
 */
int** permutacion_descifrado(int **y, int *k1_op, int *k2_op, int m, int n);

#endif