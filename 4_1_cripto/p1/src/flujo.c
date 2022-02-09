/**
 * 16/10/2020
 * Módulo: flujo.c
 * -----------------
 * Authors:
 * - Daniel Mohedano    <daniel.mohedano@estudiante.uam.es>
 * - Silvia Sopeña      <silvia.sopenna@estudiante.uam.es>
 * -----------------------------------------------------------
 * Este módulo implementa el cifrado de flujo.
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
#include <inttypes.h>

void cleanup(FILE *in, FILE *out, char *input_str, char *output_str){
    if (in && in != stdin) fclose(in);
    if (out && out != stdout) fclose(out);
    if (input_str) free(input_str);
    if (output_str) free(output_str);
}

int main(int argc, char **argv)
{
    int c;
    FILE *in = stdin, *out = stdout;
    enum {CYPHER, DECYPHER, NONE} mode = NONE;
    char* help_str = "Uso: flujo.exe {-C|-D} {-s Seed} [-i filein] [-o fileout]\n";
    bool error = false;
    char *input_str = NULL, *output_str = NULL; 

    uint64_t seed = 0;

    //Inicializar variables
    input_str = malloc(BUFFER_SIZE + 1);
    output_str = malloc(BUFFER_SIZE + 1);

    if (!input_str || !output_str){
        fprintf(stderr, "Error. No se pudo reservar memoria para strings.\n");
        cleanup(in, out, input_str, output_str);
        exit(EXIT_FAILURE);
    }

    input_str[BUFFER_SIZE] = '\0';
    output_str[BUFFER_SIZE] = '\0';

    // Parseo de argumentos
    while ((c = getopt (argc, argv, "CDs:i:o:h")) != -1){
        switch (c){
            case 'C':
                mode = CYPHER;
                break;
            case 'D':
                mode = DECYPHER;
                break;
            case 's':
                seed = strtoumax(optarg, NULL, 10);
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
                cleanup(in, out, input_str, output_str);
                exit(EXIT_SUCCESS);
            default:
                cleanup(in, out, input_str, output_str);
                exit(EXIT_FAILURE);
        }
    }

    if (mode == NONE){
        fprintf(stderr, "Error. No se especificó modo de operación.\n");
        error = true;
    }

    if (error){
        cleanup(in, out, input_str, output_str);
        exit(EXIT_FAILURE);
    }

    uint64_t k = seed;

    // Bucle de programa
    while (file_read(input_str, BUFFER_SIZE, in) > 0){
        // Se lee el input mientras haya elementos que leer, y se transforman a A-Z
        string_transform(input_str);
        if (mode == CYPHER){
            fprintf(stdout, "Encrypting: %s\n", input_str);
        }else{
            fprintf(stdout, "Decrypting: %s\n", input_str);
        }

        for (int i = 0; i < strlen(input_str); ++i){
            // Operación para cada caracter
            k = key_generator(k);
            if (mode == CYPHER){
                output_str[i] = desplazamiento_cifrado(input_str[i] - 'A', k % LANG_SIZE, LANG_SIZE) + 'A';
            }else{
                output_str[i] = desplazamiento_descifrado(input_str[i] -'A', k % LANG_SIZE, LANG_SIZE) + 'A';
            }
        }

        output_str[strlen(input_str)] = '\0';
        if (out == stdout){
            fprintf(stdout, "Result: ");
        }
        file_write(output_str, out);
    }

    cleanup(in, out, input_str, output_str);    
    
    return 0;
}