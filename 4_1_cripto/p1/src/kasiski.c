/**
 * 14/10/2020
 * Módulo: kasiski.c
 * -----------------
 * Authors:
 * - Daniel Mohedano    <daniel.mohedano@estudiante.uam.es>
 * - Silvia Sopeña      <silvia.sopenna@estudiante.uam.es>
 * -----------------------------------------------------------
 * Este módulo implementa el  método de Kasiski
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
    char* help_str = "Uso: kasiski.exe [-i filein] [-o fileout]\n";
    bool error = false;
    char *input_str = NULL, *output_str = NULL; 

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
    while ((c = getopt (argc, argv, "i:o:h")) != -1){
        switch (c){
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
                    fprintf(stderr, "Error. No se pudo abrir el archivo de lectura.\n");
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

    if (error){
        cleanup(in, out, input_str, output_str);
        exit(EXIT_FAILURE);
    }

    int len;
    int min_len = 3;
    int k, k_prev = 0, i_prev = 0; 

    sprintf(output_str, "INI \tFIN \tDIST\tLONG\n");
    file_write(output_str, out);

    while (file_read(input_str, BUFFER_SIZE, in) > 0){
        // Se convierte la string leida
        string_transform(input_str);

        len = strlen(input_str);
        k = 0; k_prev = 0; i_prev = 0;

        // Se buscan las coincidencias de tamaño mayor que 3
        for (int i = 0; i < len; ++i){
            for (int j = i+1; j < len; ++j){
                k = 0;
                while (input_str[i+k] == input_str[j+k]) ++k;
                if ((k > min_len) && i > i_prev + k_prev){
                    k_prev = k;
                    i_prev = i;
                    sprintf(output_str, "%.4d\t%.4d\t%.4d\t%.4d\n", i, j, j-i, k);
                    file_write(output_str, out);               
                }
            }
        } 
    } 

    fprintf(stdout, "\nFinished.\n");

    cleanup(in, out, input_str, output_str);
    exit(EXIT_SUCCESS);
}