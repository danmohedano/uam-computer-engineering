/**
 * 07/10/2020
 * Módulo: hill.c
 * -----------------
 * Authors:
 * - Daniel Mohedano    <daniel.mohedano@estudiante.uam.es>
 * - Silvia Sopeña      <silvia.sopenna@estudiante.uam.es>
 * -----------------------------------------------------------
 * Este módulo implementa el cifrado de Hill
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

void cleanup(FILE *in, FILE *out, char *input_str, char *output_str, FILE *k, int **k_matrix, int **k_matrix_inv, int n, int *input_block){
    if (in && in != stdin) fclose(in);
    if (out && out != stdout) fclose(out);
    if (input_str) free(input_str);
    if (output_str) free(output_str);
    if (k) fclose(k);
    if (k_matrix) free_matrix(k_matrix, n);
    if (k_matrix_inv) free_matrix(k_matrix_inv, n);
    if (input_block) free(input_block);
}

int main(int argc, char **argv)
{
    int c;
    FILE *in = stdin, *out = stdout;
    enum {CYPHER, DECYPHER, NONE} mode = NONE;
    char* help_str = "Uso: hill.exe {-C|-D} {-m |Zm|} {-n Nk} {-k filek} [-i filein] [-o fileout]\n";
    bool error = false;
    char *input_str = NULL; 
    char *output_str = NULL;

    
    // Inicializar variables
    int n = -1, m = -1;
    FILE *k = NULL;
    int **k_matrix = NULL, **k_matrix_inv = NULL, *input_block = NULL, *output_block = NULL;

    input_str = malloc(BUFFER_SIZE + 1);
    output_str = malloc(BUFFER_SIZE + 1);

    if (!input_str || !output_str){
        fprintf(stderr, "Error. No se pudo reservar memoria para strings.\n");
        cleanup(in, out, input_str, output_str, k, k_matrix, k_matrix_inv, n, input_block);
        exit(EXIT_FAILURE);
    }

    input_str[BUFFER_SIZE] = '\0';
    output_str[BUFFER_SIZE] = '\0';


    // Parseo de argumentos
    while ((c = getopt (argc, argv, "CDm:n:k:i:o:h")) != -1){
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
            case 'k':
                k = fopen(optarg, "r");
                if (!k){
                    fprintf(stderr, "Error. No se pudo abrir el archivo de clave.\n");
                    k = NULL;
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
                cleanup(in, out, input_str, output_str, k, k_matrix, k_matrix_inv, n, input_block);
                exit(EXIT_SUCCESS);
            default:
                cleanup(in, out, input_str, output_str, k, k_matrix, k_matrix_inv, n, input_block);
                exit(EXIT_FAILURE);
        }
    }

    if (mode == NONE){
        fprintf(stderr, "Error. No se especificó modo de operación.\n");
        error = true;
    }

    if (k == NULL && !error){
        fprintf(stderr, "Error. No se especificó archivo de clave.\n");
        error = true;
    }

    if (n == -1){
        fprintf(stderr, "Error. No se especificó valor para n.\n");
        error = true;
    }

    if (m == -1){
        fprintf(stderr, "Error. No se especificó valor para m.\n");
        error = true;
    }

    if (error){
        cleanup(in, out, input_str, output_str, k, k_matrix, k_matrix_inv, n, input_block);
        exit(EXIT_FAILURE);
    }

    // Inicializamos las matrices y vectores
    k_matrix = allocate_matrix(n, n);
    input_block = (int*)malloc(n*sizeof(int));

    if (!k_matrix || !input_block){
        fprintf(stderr, "Error. Error al alocar memoria.\n");
        cleanup(in, out, input_str, output_str, k, k_matrix, k_matrix_inv, n, input_block);
        exit(EXIT_FAILURE);
    }

    // Leer matriz de archivo
    if (!load_matrix(k, k_matrix, n, n)){
        fprintf(stderr, "Error. Error al leer la matriz clave.\n");
        cleanup(in, out, input_str, output_str, k, k_matrix, k_matrix_inv, n, input_block);
        exit(EXIT_FAILURE);
    }


    // Comprobar que la matriz tenga inverso multiplicativo
    if ((k_matrix_inv = matrix_modular_inv(k_matrix, n, m)) == NULL){
        fprintf(stderr, "Error. La matriz proporcionada como clave no tiene inverso multiplicativo.\n");
        cleanup(in, out, input_str, output_str, k, k_matrix, k_matrix_inv, n, input_block);
        exit(EXIT_FAILURE);
    }

    int bytes_read = 0;
    int chars_sin_bloque = 0;

    // Bucle de programa
    while ((bytes_read = file_read(input_str + chars_sin_bloque, BUFFER_SIZE - chars_sin_bloque, in)) > 0 || chars_sin_bloque > 0){
        // Se lee el input mientras haya elementos que leer, y se transforman a A-Z
        string_transform(input_str);

        // Se comprueba si hay que añadir padding o no
        if (bytes_read == 0 && chars_sin_bloque > 0){
            for (int i = 0; i < n - chars_sin_bloque; ++i) input_str[chars_sin_bloque+i] = 'A';
            input_str[n] = '\0';
        }

        if (mode == CYPHER){
            fprintf(stdout, "Encrypting: %.*s\n", (int)(strlen(input_str) / n) * n, input_str);
        }else{
            fprintf(stdout, "Decrypting: %.*s\n", (int)(strlen(input_str) / n) * n, input_str);
        }

        // Se van cogiendo los bloques enteros del buffer
        for (int bloque = 0; bloque < (strlen(input_str)) / n; ++bloque){
            // Se guarda el bloque
            for (int i = 0; i < n; ++i) input_block[i] = input_str[bloque*n+i] - 'A';

            // Se realiza la operación
            if (mode == CYPHER) output_block = matrix_modular_mul(input_block, k_matrix, n, m);
            else output_block = matrix_modular_mul(input_block, k_matrix_inv, n, m);

            // Se guarda el bloque resultante en el buffer de escritura
            for (int i = 0; i < n; ++i) output_str[(bloque*n)+i] = output_block[i] + 'A';
            
            free(output_block);
        }
        // Se escribe el buffer al haber cifrado/descifrado todos los bloques enteros
        int inicio_bloque_parcial = n * (strlen(input_str) / n);
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

    fprintf(stdout, "\nFinished.\n");

    cleanup(in, out, input_str, output_str, k, k_matrix, k_matrix_inv, n, input_block);

    exit(EXIT_SUCCESS);
}