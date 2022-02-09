/**
 * 16/10/2020
 * Módulo: seg_perf.c
 * -----------------
 * Authors:
 * - Daniel Mohedano    <daniel.mohedano@estudiante.uam.es>
 * - Silvia Sopeña      <silvia.sopenna@estudiante.uam.es>
 * -----------------------------------------------------------
 * Este módulo implementa una comprobación de la seguridad perfecta del cifrado Afín.
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
#include "../includes/constants.h"
#include <time.h>

void cleanup(mpz_t m, mpz_t a, mpz_t b, mpz_t a_inv, mpz_t x, mpz_t y, FILE *in, FILE *out, char *input_str){
    mpz_clear(m); mpz_clear(a); mpz_clear(a_inv); mpz_clear(b); mpz_clear(x); mpz_clear(y);
    if (in && in != stdin) fclose(in);
    if (out && out != stdout) fclose(out);
    if (input_str) free(input_str);
}

int main(int argc, char **argv)
{
    int c;
    FILE *in = stdin, *out = stdout;
    enum {EQUIP, NOEQUIP, NONE} mode = NONE;
    char* help_str = "Uso: seg_perf.exe {-P|-I} [-i filein] [-o fileout]\n";
    bool error = false;
    char *input_str = NULL;

    mpz_t m, a, b, a_inv, x, y;

    // Inicializar variables
    mpz_init(m); mpz_init(a); mpz_init(b); mpz_init(a_inv); mpz_init(x); mpz_init(y);
    input_str = malloc(BUFFER_SIZE + 1);

    if (!input_str){
        fprintf(stderr, "Error. No se pudo reservar memoria para strings.\n");
        cleanup(m, a, b, a_inv, x, y, in, out, input_str);
        exit(EXIT_FAILURE);
    }

    input_str[BUFFER_SIZE] = '\0';

    // Parseo de argumentos
    while ((c = getopt (argc, argv, "PIi:o:h")) != -1){
        switch (c){
            case 'P':
                mode = EQUIP;
                break;
            case 'I':
                mode = NOEQUIP;
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
                cleanup(m, a, b, a_inv, x, y, in, out, input_str);
                exit(EXIT_SUCCESS);
            default:
                cleanup(m, a, b, a_inv, x, y, in, out, input_str);
                exit(EXIT_FAILURE);
        }
    }

    if (mode == NONE){
        fprintf(stderr, "Error. No se especificó modo de operación.\n");
        error = true;
    }

    if (error){
        cleanup(m, a, b, a_inv, x, y, in, out, input_str);
        exit(EXIT_FAILURE);
    }

    double prob_plano[LANG_SIZE];
    double prob_cond[LANG_SIZE][LANG_SIZE];
    int c_plano, c_cifrado;

    // Se inicializan los contadores a 0
    for (int i = 0; i < LANG_SIZE; ++i){
        prob_plano[i] = 0;
        for (int j = 0; j < LANG_SIZE; ++j) prob_cond[i][j] = 0;
    }

    mpz_set_ui(m, LANG_SIZE);
    srand(time(0));

    // Bucle de programa
    while (file_read(input_str, BUFFER_SIZE, in) > 0){
        // Se lee el input mientras haya elementos que leer, y se transforman a A-Z
        string_transform(input_str);

        for (int i = 0; i < strlen(input_str); ++i){
            // Operación para cada caracter

            // Generar un clave
            if (mode == EQUIP){
                // Equiprobable
                afin_key_equiprobable(a, b);
            }else{
                // No equiprobable
                afin_key_noequiprobable(a, b);
            }

            c_plano = input_str[i] - 'A';
            prob_plano[c_plano] += 1;

            // Se cifra el caracter
            mpz_set_ui(x, c_plano);
            afin_cifrado(x, a, b, m, y);
            c_cifrado = mpz_get_ui(y);

            prob_cond[c_plano][c_cifrado] += 1;
        }
    }

    // Se calculan las probabilidades de texto plano P(x)
    double sum = 0;
    for (int i = 0; i < LANG_SIZE; ++i){
        sum += prob_plano[i];
    }
    for (int i = 0; i < LANG_SIZE; ++i){
        prob_plano[i] /= sum;
    }

    // Se calculan las probabilidades condicionales P(x|y)
    for (int j = 0; j < LANG_SIZE; ++j){
        sum = 0;
        for (int i = 0; i < LANG_SIZE; ++i){
            sum += prob_cond[i][j];
        }

        if (sum != 0){
            for (int i = 0; i < LANG_SIZE; ++i){
                prob_cond[i][j] /= sum;
            }
        } 
    }


    // Se escribe la string de output
    for (int i = 0; i < LANG_SIZE; ++i){
        fprintf(out, "Pp(%c)=%lf\n", i + 'A', prob_plano[i]);
    }

    for (int i = 0; i < LANG_SIZE; ++i){
        for (int j = 0; j < LANG_SIZE; ++j){
            fprintf(out, "Pp(%c|%c)=%lf ", i + 'A', j + 'A', prob_cond[i][j]);
        }   
        fprintf(out, "\n");
    }

    double rango = 0.01;
    bool perfecta = true;
    // Se comprueba la condición de seguridad perfecta P(x) == P(x|y)
    for (int x = 0; x < LANG_SIZE; ++x){
        for (int y = 0; y < LANG_SIZE; ++y){
            if ((prob_cond[x][y] < (prob_plano[x] - rango)) || (prob_cond[x][y] > (prob_plano[x] + rango))){
                if (perfecta){
                    perfecta = false;
                    fprintf(out, "El método Afín NO cumple la condición de seguridad perfecta:\n");
                }
                fprintf(out, "P(%c) != P(%c|%c)\n", x + 'A', x + 'A', y + 'A');
            }
        }
    }

    if (perfecta) fprintf(out, "El método Afín SI ha cumplido la condición de seguridad perfecta.\n");



    cleanup(m, a, b, a_inv, x, y, in, out, input_str);    
    
    return 0;
}