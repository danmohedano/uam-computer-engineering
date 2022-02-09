/**
 * 16/10/2020
 * Módulo: permutacion.c
 * -----------------
 * Authors:
 * - Daniel Mohedano    <daniel.mohedano@estudiante.uam.es>
 * - Silvia Sopeña      <silvia.sopenna@estudiante.uam.es>
 * -----------------------------------------------------------
 * Este módulo implementa el producto de criptosistemas por permutación.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <gmp.h>
#include <unistd.h>
#include <string.h>
#include "../includes/utils.h"
#include "../includes/cypher.h"
#include "../includes/io.h"

void cleanup(FILE *in, FILE *out, char *input_str, char *output_str, FILE *k1_file, FILE *k2_file, int *k1, int *k2, int *k1_op, int *k2_op, int **input_matrix, int m){
    if (in && in != stdin) fclose(in);
    if (out && out != stdout) fclose(out);
    if (input_str) free(input_str);
    if (output_str) free(output_str);
    if (k1_file) fclose(k1_file);
    if (k2_file) fclose(k2_file);
    if (k1) free(k1);
    if (k2) free(k2);
    if (k1_op) free(k1_op);
    if (k2_op) free(k2_op);
    if (input_matrix) free_matrix(input_matrix, m);
}

int main(int argc, char **argv)
{
    int c;
    FILE *in = stdin, *out = stdout;
    enum {CYPHER, DECYPHER, NONE} mode = NONE;
    char* help_str = "Uso: permutacion.exe {-C|-D} {-m Filas -n Columnas} {-f K1 -c K2} [-i filein] [-o fileout]\n";
    bool error = false;
    char *input_str = NULL, *output_str = NULL; 

    int m = 0, n = 0;
    FILE *k1_file = NULL, *k2_file = NULL;

    //Inicializar variables
    input_str = malloc(BUFFER_SIZE + 1);
    output_str = malloc(BUFFER_SIZE + 1);

    if (!input_str || !output_str){
        fprintf(stderr, "Error. No se pudo reservar memoria para strings.\n");
        cleanup(in, out, input_str, output_str, k1_file, k2_file, NULL, NULL, NULL, NULL, NULL, m);
        exit(EXIT_FAILURE);
    }

    input_str[BUFFER_SIZE] = '\0';
    output_str[BUFFER_SIZE] = '\0';

    // Parseo de argumentos
    while ((c = getopt (argc, argv, "CDm:n:f:c:i:o:h")) != -1){
        switch (c){
            case 'C':
                mode = CYPHER;
                break;
            case 'D':
                mode = DECYPHER;
                break;
            case 'm':
                m = atoi(optarg);
                break;
            case 'n':
                n = atoi(optarg);
                break;
            case 'f':
                k1_file = fopen(optarg, "r");
                if (!k1_file){
                    fprintf(stderr, "Error. No se pudo abrir el archivo de permutación k1.\n");
                    k1_file = NULL;
                    error = true;
                }
                break;
            case 'c':
                k2_file = fopen(optarg, "r");
                if (!k2_file){
                    fprintf(stderr, "Error. No se pudo abrir el archivo de permutación k2.\n");
                    k2_file = NULL;
                    error = true;
                }
                break;
            case 'i':
                in = fopen(optarg, "r");
                if (!in){
                    fprintf(stderr, "Error. No se pudo abrir el archivo de lectura.\n");
                    in = NULL;
                    error = true;
                }
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
                cleanup(in, out, input_str, output_str, k1_file, k2_file, NULL, NULL, NULL, NULL, NULL, m);
                exit(EXIT_SUCCESS);
            default:
                cleanup(in, out, input_str, output_str, k1_file, k2_file, NULL, NULL, NULL, NULL, NULL, m);
                exit(EXIT_FAILURE);
        }
    }

    if (mode == NONE){
        fprintf(stderr, "Error. No se especificó modo de operación.\n");
        error = true;
    }

    if ((k1_file == NULL || k2_file == NULL) && !error){
        fprintf(stderr, "Error. No se proporcionaron permutaciones.\n");
        error = true;
    }

    if (error){
        cleanup(in, out, input_str, output_str, k1_file, k2_file, NULL, NULL, NULL, NULL, NULL, m);
        exit(EXIT_FAILURE);
    }

    // Se transforman las permutaciones proporcionadas a arrays
    int *k1 = NULL, *k2 = NULL, *k1_op = NULL, *k2_op = NULL;
    int **input_matrix = NULL, **output_matrix = NULL;

    k1 = (int*)malloc(m*sizeof(int));
    k2 = (int*)malloc(n*sizeof(int));
    k1_op = (int*)malloc(m*sizeof(int));
    k2_op = (int*)malloc(n*sizeof(int));
    input_matrix = allocate_matrix(m, n);

    if (!k1 || !k2 || !input_matrix || !k1_op || !k2_op){
        fprintf(stderr, "Error. Error al alocar memoria para arrays.\n");
        cleanup(in, out, input_str, output_str, k1_file, k2_file, k1, k2, k1_op, k2_op, input_matrix, m);
        exit(EXIT_FAILURE);
    }

    if (!load_vector(k1_file, k1, m) || !load_vector(k2_file, k2, n)){
        fprintf(stderr, "Error. Error al cargar las permutaciones.\n");
        cleanup(in, out, input_str, output_str, k1_file, k2_file, k1, k2, k1_op, k2_op, input_matrix, m);
        exit(EXIT_FAILURE);
    }

    // Se calculan las permutaciones opuestas
    for (int i = 0; i < m; ++i){
        k1_op[k1[i]] = i;
    }

    for (int i = 0; i < n; ++i){
        k2_op[k2[i]] = i;
    }

    int bytes_read = 0;
    int chars_sin_bloque = 0;

    // Bucle de programa
    while ((bytes_read = file_read(input_str + chars_sin_bloque, BUFFER_SIZE - chars_sin_bloque, in)) > 0 || chars_sin_bloque > 0){
        // Se lee el input mientras haya elementos que leer, y se transforman a A-Z
        string_transform(input_str);

        // Se comprueba si hay que añadir padding o no
        if (bytes_read == 0 && chars_sin_bloque > 0){
            for (int i = 0; i < (m*n) - chars_sin_bloque; ++i) input_str[chars_sin_bloque+i] = 'A';
            input_str[m*n] = '\0';
        }

        if (mode == CYPHER){
            fprintf(stdout, "Encrypting: %.*s\n", (int)(strlen(input_str)) / (m*n) * m*n, input_str);
        }else{
            fprintf(stdout, "Decrypting: %.*s\n", (int)(strlen(input_str)) / (m*n) * m*n, input_str);
        }

        // Se van cogiendo las matrices enteras del buffer
        for (int bloque = 0; bloque < (strlen(input_str)) / (m*n); ++bloque){
            // Se guarda la matriz
            for (int i = 0; i < m; ++i){
                for (int j = 0; j < n; ++j){
                    input_matrix[i][j] = input_str[(bloque*m*n) + (i*n) + j] - 'A';
                }
            }

            // Se realiza la operación
            if (mode == CYPHER) output_matrix = permutacion_cifrado(input_matrix, k1, k2, m, n);
            else output_matrix = permutacion_descifrado(input_matrix, k1_op, k2_op, m, n);

            // Se guarda el bloque resultante en el buffer de escritura
            for (int i = 0; i < m; ++i){
                for (int j = 0; j < n; ++j){
                    output_str[(bloque*m*n) + (i*n) + j] = output_matrix[i][j] + 'A';
                }
            }
            
            free_matrix(output_matrix, m);
        }
        // Se escribe el buffer al haber cifrado/descifrado todos los bloques enteros
        int inicio_bloque_parcial = m*n*(strlen(input_str) / (m*n));
        output_str[inicio_bloque_parcial] = '\0';
        if (out == stdout){
            fprintf(stdout, "Result: ");
        }
        file_write(output_str, out);

        // Los caracteres que han sobrado se mueven al inicio de la string
        
        for (int i = inicio_bloque_parcial; i < strlen(input_str); ++i){
            input_str[i - inicio_bloque_parcial] = input_str[i];
        }
        chars_sin_bloque = strlen(input_str) - inicio_bloque_parcial;
    }

    cleanup(in, out, input_str, output_str, k1_file, k2_file, k1, k2, k1_op, k2_op, input_matrix, m);    
    
    return 0;
}