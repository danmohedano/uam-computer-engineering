/**
 * 18/09/2021
 * Módulo: afin.c
 * -----------------
 * Authors:
 * - Daniel Mohedano    <daniel.mohedano@estudiante.uam.es>
 * - Silvia Sopeña      <silvia.sopenna@estudiante.uam.es>
 * -----------------------------------------------------------
 * Este módulo implementa el cifrado afín
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

void cleanup(mpz_t m, mpz_t a, mpz_t b, mpz_t a_inv, mpz_t x, mpz_t y, FILE *in, FILE *out, char *input_str, char *output_str){
    mpz_clear(m); mpz_clear(a); mpz_clear(a_inv); mpz_clear(b); mpz_clear(x); mpz_clear(y);
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
    char* help_str = "Uso: afin.exe {-C|-D} {-m |Zm|} {-a N×} {-b N+} [-i filein] [-o fileout]\n";
    bool error = false;
    char *input_str = NULL; 
    char *output_str = NULL;

    mpz_t m, a, b, a_inv, x, y;

    // Inicializar variables
    mpz_init(m); mpz_init(a); mpz_init(b); mpz_init(a_inv); mpz_init(x); mpz_init(y);

    input_str = malloc(BUFFER_SIZE + 1);
    output_str = malloc(BUFFER_SIZE + 1);

    if (!input_str || !output_str){
        fprintf(stderr, "Error. No se pudo reservar memoria para strings.\n");
        cleanup(m, a, b, a_inv, x, y, in, out, input_str, output_str);
        exit(EXIT_FAILURE);
    }

    input_str[BUFFER_SIZE] = '\0';
    output_str[BUFFER_SIZE] = '\0';


    // Parseo de argumentos
    while ((c = getopt (argc, argv, "CDm:a:b:i:o:h")) != -1){
        switch (c){
            case 'C':
                mode = CYPHER;
                break;
            case 'D':
                mode = DECYPHER;
                break;
            case 'm':
                mpz_set_str(m, optarg, 10);
                break;
            case 'a':
                mpz_set_str(a, optarg, 10);
                break;
            case 'b':
                mpz_set_str(b, optarg, 10);
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
                cleanup(m, a, b, a_inv, x, y, in, out, input_str, output_str);
                exit(EXIT_SUCCESS);
            default:
                cleanup(m, a, b, a_inv, x, y, in, out, input_str, output_str);
                exit(EXIT_FAILURE);
        }
    }

    if (mode == NONE){
        fprintf(stderr, "Error. No se especificó modo de operación.\n");
        error = true;
    }

    if (error){
        cleanup(m, a, b, a_inv, x, y, in, out, input_str, output_str);
        exit(EXIT_FAILURE);
    }

    // Comprobar que a tenga inverso multiplicativo. Si no error
    mpz_mod(a, a, m);
    mpz_mod(b, b, m);

    if (euclides_extended(m, a, a_inv) == 0){
        fprintf(stderr, "Error. Valor de a proporcionado no tiene inverso multiplicativo.\n");
        cleanup(m, a, b, a_inv, x, y, in, out, input_str, output_str);
        exit(EXIT_FAILURE);
    }
    
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
            if (mode == CYPHER){
                mpz_set_ui(x, input_str[i] - 'A');
                afin_cifrado(x, a, b, m, y);
                output_str[i] = mpz_get_ui(y) + 'A';
            }else{
                mpz_set_ui(y, input_str[i] - 'A');
                afin_descifrado(y, a_inv, b, m, x);
                output_str[i] = mpz_get_ui(x) + 'A';
            }
        }

        output_str[strlen(input_str)] = '\0';
        if (out == stdout){
            fprintf(stdout, "Result: ");
        }
        file_write(output_str, out);
    }

    fprintf(stdout, "\nFinished.\n");

    cleanup(m, a, b, a_inv, x, y, in, out, input_str, output_str);

    exit(EXIT_SUCCESS);
}