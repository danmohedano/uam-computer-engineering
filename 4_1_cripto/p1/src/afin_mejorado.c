/**
 * 18/09/2021
 * Módulo: afin_mejorado.c
 * -----------------
 * Authors:
 * - Daniel Mohedano    <daniel.mohedano@estudiante.uam.es>
 * - Silvia Sopeña      <silvia.sopenna@estudiante.uam.es>
 * -----------------------------------------------------------
 * Este módulo implementa el cifrado afín mejorado con mayor fortaleza
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

void cleanup(mpz_t m, mpz_t a, mpz_t b, mpz_t a_inv, mpz_t x, mpz_t y, FILE *in, FILE *out, char *input_str, char *output_str, mpz_t m_mul){
    mpz_clear(m); mpz_clear(a); mpz_clear(a_inv); mpz_clear(b); mpz_clear(x); mpz_clear(y); mpz_clear(m_mul);
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
    char* help_str = "Uso: afin_mejorado.exe {-C|-D} {-n #Chars en bloque} {-m |Zm|} {-a N×} {-b N+} [-i filein] [-o fileout]\n";
    bool error = false;
    char *input_str = NULL; 
    char *output_str = NULL;

    mpz_t m, a, b, a_inv, x, y, m_mul;
    int n = 1;

    // Inicializar variables
    mpz_init(m); mpz_init(a); mpz_init(b); mpz_init(a_inv); mpz_init(x); mpz_init(y); mpz_init(m_mul);

    input_str = malloc(BUFFER_SIZE + 1);
    output_str = malloc(BUFFER_SIZE + 1);

    if (!input_str || !output_str){
        fprintf(stderr, "Error. No se pudo reservar memoria para strings.\n");
        cleanup(m, a, b, a_inv, x, y, in, out, input_str, output_str, m_mul);
        exit(EXIT_FAILURE);
    }

    input_str[BUFFER_SIZE] = '\0';
    output_str[BUFFER_SIZE] = '\0';


    // Parseo de argumentos
    while ((c = getopt (argc, argv, "CDn:m:a:b:i:o:h")) != -1){
        switch (c){
            case 'C':
                mode = CYPHER;
                break;
            case 'D':
                mode = DECYPHER;
                break;
            case 'n':
                n = atoi(optarg);
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
                cleanup(m, a, b, a_inv, x, y, in, out, input_str, output_str, m_mul);
                exit(EXIT_SUCCESS);
            default:
                cleanup(m, a, b, a_inv, x, y, in, out, input_str, output_str, m_mul);
                exit(EXIT_FAILURE);
        }
    }

    if (mode == NONE){
        fprintf(stderr, "Error. No se especificó modo de operación.\n");
        error = true;
    }

    if (error){
        cleanup(m, a, b, a_inv, x, y, in, out, input_str, output_str, m_mul);
        exit(EXIT_FAILURE);
    }

    mpz_set(m_mul, m);

    // Al agruparse en bloques el tamaño del espacio de texto cifrado cambia
    for (int i = 1; i < n; ++i){
        mpz_mul(m_mul, m, m);
    }

    // Comprobar que a tenga inverso multiplicativo. Si no error
    mpz_mod(a, a, m_mul);
    mpz_mod(b, b, m_mul);

    if (euclides_extended(m_mul, a, a_inv) == 0){
        fprintf(stderr, "Error. Valor de a proporcionado no tiene inverso multiplicativo.\n");
        cleanup(m, a, b, a_inv, x, y, in, out, input_str, output_str, m_mul);
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
            fprintf(stdout, "Encrypting: %.*s\n", (int)(strlen(input_str)) / n * n, input_str);
        }else{
            fprintf(stdout, "Decrypting: %.*s\n", (int)(strlen(input_str)) / n * n, input_str);
        }

        // Se van cogiendo los bloques enteros del buffer
        for (int bloque = 0; bloque < (strlen(input_str)) / n; ++bloque){
            mpz_set_ui(x, 0);
            // Se convierte el bloque de caracteres a un valor numérico
            for (int i = 0; i < n; ++i){
                // valor = (valor*m) + char
                mpz_mul(x, x, m);
                mpz_add_ui(x, x, input_str[bloque*n+i] - 'A');
            }

            // Se realiza la operación
            if (mode == CYPHER){
                afin_cifrado(x, a, b, m_mul, y);
            }else{
                afin_descifrado(x, a_inv, b, m_mul, y);
            }

            // Se convierte el número cifrado de vuelta a cadena de caracteres
            for (int i = n-1; i >= 0; --i){
                mpz_tdiv_qr (y, x, y, m);
                output_str[(bloque*n)+i] = mpz_get_ui(x) + 'A';
            }
            
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

    cleanup(m, a, b, a_inv, x, y, in, out, input_str, output_str, m_mul);

    exit(EXIT_SUCCESS);
}