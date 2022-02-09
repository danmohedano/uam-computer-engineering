/**
 * 11/11/2020
 * Módulo: desECB.c
 * -----------------
 * Authors:
 * - Daniel Mohedano    <daniel.mohedano@estudiante.uam.es>
 * - Silvia Sopeña      <silvia.sopenna@estudiante.uam.es>
 * -----------------------------------------------------------
 * Este módulo implementa DES con modo de operación ECB.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>
#include <stdint.h>
#include "../includes/des.h"
#include "../includes/constants.h"

void cleanup(FILE *in, FILE *out){
    if (in && in != stdin) fclose(in);
    if (out && out != stdout) fclose(out);
}

int main(int argc, char **argv)
{
    int c;
    FILE *in = stdin, *out = stdout;
    enum {CYPHER, DECYPHER, NONE} mode = NONE;
    char* help_str = "Uso: desECB.exe {-C | -D -k clave} [-i filein] [-o fileout]\n";
    bool error = false;

    uint64_t key = 0; 

    // Parseo de argumentos
    while ((c = getopt (argc, argv, "CDk:i:o:h")) != -1){
        switch (c){
            case 'C':
                mode = CYPHER;
                break;
            case 'D':
                mode = DECYPHER;
                break;
            case 'k':
                sscanf(optarg, "%lx", &key);
                break;
            case 'i':
                in = fopen(optarg, "rb");
                if (!in){
                    fprintf(stderr, "Error. No se pudo abrir el archivo de lectura.\n");
                    in = NULL;
                    error = true;
                }
                break;
            case 'o':
                out = fopen(optarg, "wb");
                if (!out){
                    fprintf(stderr, "Error. No se pudo abrir el archivo de escritura.\n");
                    out = NULL;
                    error = true;
                }
                break;
            case 'h':
                fprintf(stderr, "%s", help_str);
                cleanup(in, out);
                exit(EXIT_SUCCESS);
            default:
                cleanup(in, out);
                exit(EXIT_FAILURE);
        }
    }

    if (mode == NONE){
        fprintf(stderr, "Error. No se especificó modo de operación.\n");
        error = true;
    }

    if (!key_check(key)){
        fprintf(stderr, "Error. Clave no cumple condición de paridad impar.\n");
        error = true;
    }

    if (error){
        cleanup(in, out);
        exit(EXIT_FAILURE);
    }

    uint64_t input = 0, result = 0;
    size_t bytes_read = 0;

    printf("Aplicando DES en modo ECB con los siguientes parametros:\n");
    printf("k = 0x%016lx\n", key);

    // Bucle de programa
    while ((bytes_read = fread(&input, 1, 8, in)) > 0){
        printf("Input leido: 0x%016lx\n", input);
        fflush(stdout);

        // 1. Cifrado/Descifrado del bloque
        des_full(input, &result, key, mode == CYPHER);

        // 2. Se escribe el output
        fwrite(&result, 1, 8, out);

        input = 0;
        result = 0;
    }

    cleanup(in, out);    
    
    return 0;
}