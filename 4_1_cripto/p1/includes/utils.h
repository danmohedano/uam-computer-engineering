/**
 * 23/09/2021
 * Módulo: utils
 * -----------------
 * Autores:
 * - Daniel Mohedano    <daniel.mohedano@estudiante.uam.es>
 * - Silvia Sopeña      <silvia.sopenna@estudiante.uam.es>
 * -----------------------------------------------------------
 * Este módulo alberga funciones auxiliares.
 */

#ifndef UTILS_H
#define UTILS_H

#include <gmp.h>
#include <stdio.h>
#include <stdint.h>

#define LANG_SIZE 26

/**--------------------------------------------------------------------------**/
/**-------------------------------UTILIDAD MCD-------------------------------**/
/**--------------------------------------------------------------------------**/
/**
 * euclides_extended
 * 
 * Aplica el algoritmo de Euclides extendido para calcular tanto el mcd(m,a) 
 * como el inverso multiplicativo de a.
 * 
 * Inputs:
 *      m (mpz_t): Número m.
 *      a (mpz_t): Número a.
 * Outputs:
 *      inverse_a (mpz_t): Inverso multiplicativo de a en Zm (valor real solo 
 *                         si mcd(m,a)==1).
 *      (int): 1 si mcd(m,a) == 1, 0 en cualquier otro caso.
 */
int euclides_extended(mpz_t m, mpz_t a, mpz_t inverse_a);


/**--------------------------------------------------------------------------**/
/**-----------------------------UTILIDAD MATRICES----------------------------**/
/**--------------------------------------------------------------------------**/
/**
 * matrix_modular_mul
 * 
 * Realiza la multiplicación en aritmética modular del vector x con la matriz k.
 * 
 * Inputs:
 *      x (int*): Vector x.
 *      k (int**): Matriz k.
 *      n (int): Dimensión del vector y matriz.
 *      m (int): Módulo aplicado.
 * Outputs:
 *      int*: Vector resultante de la multiplicación. Se debe liberar la memoria
 *            tras su uso.
 */
int* matrix_modular_mul(int *x, int **k, int n, int m);

/**
 * matrix_modular_det
 * 
 * Calcula el determinante en aritmética modular de la matriz k. Para realizar 
 * el cálculo, hace uso de la expansión de Laplace, calculando el determinante
 * en función del determinante de las menores.
 * 
 * Inputs:
 *      k (int**): Matriz k.
 *      n (int): Dimensión de la matriz.
 *      m (int): Módulo aplicado.
 * Outputs:
 *      int: Valor del determinante.
 */
int matrix_modular_det(int **k, int n, int m);

/**
 * matrix_modular_inv
 * 
 * Calcula la matriz inversa de la matriz proporcionada en aritmética modular. 
 * El cálculo se realiza como: K^-1 = det(K)^-1 * adj(K)
 * 
 * Inputs:
 *      k (int**): Matriz k.
 *      n (int): Dimensión del vector y matriz.
 *      m (int): Módulo aplicado.
 * Outputs:
 *      int**: Matriz inversa. Se debe liberar la memoria tras su uso.
 */
int** matrix_modular_inv(int **k, int n, int m);

/**
 * minor_matrix
 * 
 * Calcula la matriz menor eliminando la fila i y la columna j de la matriz 
 * original.
 * 
 * Inputs:
 *      x (int**): Matriz original.
 *      n (int): Dimensión de la matriz.
 *      i (int): Fila que se ignora.
 *      j (int): Columna que se ignora.
 * Outputs:
 *      m (int**): La matriz menor.
 */
void minor_matrix(int **x, int **m, int n, int i, int j);

/**
 * allocate_matrix
 * 
 * Aloca memoria para la creación de una matriz de dimensión m x n.
 * 
 * Inputs:
 *      m (int): Filas de la matriz.
 *      n (int): Columnas de la matriz.
 * Outputs:
 *      int**: Matriz creada. Se debe liberar la memoria tras su uso.
 */
int** allocate_matrix(int m, int n);

/**
 * free_matrix
 * 
 * Libera la memoria utilizada en la creación de una matriz. 
 * 
 * Inputs:
 *      matrix (int**): Matriz a liberar.
 *      m (int): Filas de la matriz..
 */
void free_matrix(int **matrix, int m);

/**
 * matrix_swap_rows
 * 
 * Permuta las filas de la matriz x utilizando la permutación k proporcionada.
 * 
 * Inputs:
 *      x (int**): Matriz x.
 *      k (int*): Permutación k.
 *      m (int): Filas de la matriz.
 *      n (int): Columnas de la matriz.
 * Outputs:
 *      int*: Matriz resultante tras la permutación. Se debe liberar la memoria
 *            tras su uso.
 */
int** matrix_swap_rows(int **x, int *k, int m, int n);

/**
 * matrix_swap_columns
 * 
 * Permuta las columnas de la matriz x utilizando la permutación k proporcionada
 * 
 * Inputs:
 *      x (int**): Matriz x.
 *      k (int*): Permutación k.
 *      m (int): Filas de la matriz.
 *      n (int): Columnas de la matriz.
 * Outputs:
 *      int*: Matriz resultante tras la permutación. Se debe liberar la memoria
 *            tras su uso.
 */
int** matrix_swap_columns(int **x, int *k, int m, int n);

/**
 * matrix_print
 * 
 * Realiza un print de la matriz proporcionada usando el FILE* proporcionado.
 * 
 * Inputs:
 *      pf (FILE*): Stream de output.
 *      matrix (int**): Matriz.
 *      m (int): Filas de la matriz.
 *      n (int): Columnas de la matriz.
 */
void matrix_print(FILE* pf, int **matrix, int m, int n);

uint64_t key_generator(uint64_t state);

/**--------------------------------------------------------------------------**/
/**-----------------------------UTILIDAD STRINGS-----------------------------**/
/**--------------------------------------------------------------------------**/
/**
 * string_transform
 * 
 * Transforma la string proporcionada para convertir los caracteres a mayúscula
 * y elimina cualquier caracter no alfabético.
 * 
 * Inputs:
 *      string (char*): String que transformar. Debe finalizar con '\0'.
 */
void string_transform(char *string);


#endif