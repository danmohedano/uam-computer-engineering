/**
 * 11/11/2020
 * Módulo: tdesCFB.c
 * -----------------
 * Authors:
 * - Daniel Mohedano    <daniel.mohedano@estudiante.uam.es>
 * - Silvia Sopeña      <silvia.sopenna@estudiante.uam.es>
 * -----------------------------------------------------------
 * Este módulo implementa TripleDES con modo de operación CFB.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>
#include <stdint.h>
#include <string.h>
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
    char* help_str = "Uso: tdesCFB.exe {-C | -D -k clave} {-v IV} {-S s} [-i filein] [-o fileout]\n";
    bool error = false;

    uint64_t iv = 0, keys[3] = {0, 0, 0};
    char key_placeholder[19] = "0x0000000000000000\0";
    int s = 64;

    // Parseo de argumentos
    while ((c = getopt (argc, argv, "CDk:v:s:i:o:h")) != -1){
        switch (c){
            case 'C':
                mode = CYPHER;
                break;
            case 'D':
                mode = DECYPHER;
                break;
            case 'k':
                // Guardar cada tercio como clave
                for (int i = 0; i < 3; ++i){
                    strncpy(key_placeholder + 2, optarg + (i*16) + 2, 16);
                    sscanf(key_placeholder, "%lx", &keys[i]);
                }
                break;
            case 'v':
                sscanf(optarg, "%lx", &iv);
                break;
            case 's':
                s = atoi(optarg);
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

    if (s > 64 || s < 1 || s % 8){
        fprintf(stderr, "Error. Valor no válido para s.\n");
        error = true;
    }

    for (int i = 0; i < 3; ++i){
        if (!key_check(keys[i])){
            fprintf(stderr, "Error. Clave %d no cumple condición de paridad impar.\n", i+1);
            error = true;
        }
    }
    

    if (error){
        cleanup(in, out);
        exit(EXIT_FAILURE);
    }

    uint64_t input = 0, next_iter = iv, result = 0;
    int byte_per_block = s / 8;
    size_t bytes_read = 0;

    printf("Aplicando DES en modo CFB con los siguientes parametros:\n");
    printf("k1 = 0x%016lx\n", keys[0]);
    printf("k2 = 0x%016lx\n", keys[1]);
    printf("k3 = 0x%016lx\n", keys[2]);
    printf("IV = 0x%016lx\n", iv);
    printf("s = %d\n", s);

    // Bucle de programa
    while ((bytes_read = fread(&input, 1, byte_per_block, in)) > 0){
        printf("Input leido: 0x%016lx\n", input);
        fflush(stdout);

        // 1. Left shift
        next_iter = next_iter << (64 - s);

        // 2. Cifrado del bloque
        des_full(next_iter, &next_iter, keys[0], true);
        des_full(next_iter, &next_iter, keys[1], false);
        des_full(next_iter, &next_iter, keys[2], true);

        // 3. Select s bits
        next_iter = next_iter >> (64 - s); 

        // 4. Construir txt (cifrado o plano)
        result = input ^ next_iter;

        // 5. Se escribe el cifrado
        fwrite(&result, 1, byte_per_block, out);

        // 6. Para la siguiente iteración, se guarda Ci
        if (mode == CYPHER) next_iter = result;
        else next_iter = input;
        input = 0;
    }

    cleanup(in, out);    
    
    return 0;
}