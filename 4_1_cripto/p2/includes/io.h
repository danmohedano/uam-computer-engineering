/**
 * 07/10/2021
 * Módulo: io
 * -----------------
 * Autores:
 * - Daniel Mohedano    <daniel.mohedano@estudiante.uam.es>
 * - Silvia Sopeña      <silvia.sopenna@estudiante.uam.es>
 * -----------------------------------------------------------
 * Este módulo alberga las funciones encargadas de input/output.
 */

#ifndef IO_H
#define IO_H

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define BUFFER_SIZE 5120

/**
 * file_len
 * 
 * Calcula la longitud de un archivo.
 * 
 * Inputs:
 *      pf (FILE*): Stream de input del archivo.
 * 
 * Outputs:
 *      long: La longitud del archivo.
 */
long file_len(FILE* pf);

/**
 * file_read
 * 
 * Lee una cantidad de bytes indicada del stream proporcionado y guarda los 
 * bytes en la string.
 * 
 * Inputs:
 *      str (char*): Buffer de lectura.
 *      size (int): Tamaño que se desea leer.
 *      pf (FILE*): Stream de input del archivo.
 * 
 * Outputs:
 *      size_t: Cantidad de bytes leidos.
 */
size_t file_read(char *str, int size, FILE *file);

/**
 * file_write
 * 
 * Escribe la string proporcionada en el stream de output.
 * 
 * Inputs:
 *      str (char*): Buffer de escritura.
 *      pf (FILE*): Stream de output del archivo.
 * 
 * Outputs:
 *      size_t: Cantidad de bytes escritos.
 */
size_t file_write(char *str, FILE *file);

/**
 * load_matrix
 * 
 * Lee una matriz de un archivo determinado con el siguiente formato:
 * M =  M11 M12 M13 ... M1n
 *      M21 ...         M2n
 *      .
 *      .
 *      .
 *      Mm1 ...         Mmn
 * 
 * Inputs:
 *      pf (FILE*): Stream de input.
 *      matrix (int**): Matriz donde almacenar los datos leidos.
 *      m (int): Filas de la matriz.
 *      n (int): Columnas de la matriz.
 * 
 * Outputs:
 *      bool: true si se ha leido correctamente (las dimensiones son las 
 *            correctas), false si no.
 */
bool load_matrix(FILE *pf, int **matrix, int m, int n);

/**
 * load_vector
 * 
 * Lee un vector de un archivo determinado con el siguiente formato:
 * V = V1 V2 V3 ... Vn
 * 
 * Inputs:
 *      pf (FILE*): Stream de input.
 *      vector (int*): Vector donde almacenar los datos leidos.
 *      size (int): Dimensión del vector.
 * 
 * Outputs:
 *      bool: true si se ha leido correctamente (las dimensiones son las 
 *            correctas), false si no.
 */
bool load_vector(FILE *pf, int *vector, int size);


#endif