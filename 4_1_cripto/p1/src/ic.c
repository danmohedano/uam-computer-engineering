/**
 * 14/10/2020
 * Módulo: ic.c
 * -----------------
 * Authors:
 * - Daniel Mohedano    <daniel.mohedano@estudiante.uam.es>
 * - Silvia Sopeña      <silvia.sopenna@estudiante.uam.es>
 * -----------------------------------------------------------
 * Este módulo implementa el método de índice de coincidencia para 
 * averiguar la longitud de clave.
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

void cleanup(FILE *in, FILE *out, char *input_str, char *output_str, char *k, double **f, int l, int *vector_len){
    if (in && in != stdin) fclose(in);
    if (out && out != stdout) fclose(out);
    if (input_str) free(input_str);
    if (output_str) free(output_str);
    if (k) free(k);
    if (f){
        for (int i = 0; i < l; ++i) 
            if (f[i]) free(f[i]);
        free(f);
    }
    if (vector_len) free(vector_len);
}


int main(int argc, char **argv)
{
    int c;
    FILE *in = stdin, *out = stdout;
    enum {LENGTH, KEY, NONE} mode = NONE;
    char* help_str = "Uso: ic.exe {-L|-K} {-l Ngrama} [-k Clave] [-x Idioma (0: Español, 1: Inglés)] [-i filein] [-o fileout]\n";
    bool error = false;
    char *input_str = NULL, *output_str = NULL; 

    int l = 0, idioma = 0;
    char *k = NULL;

    //Inicializar variables
    input_str = malloc(BUFFER_SIZE + 1);
    output_str = malloc(BUFFER_SIZE + 1);
    k = malloc(BUFFER_SIZE + 1);

    if (!input_str || !output_str || !k){
        fprintf(stderr, "Error. No se pudo reservar memoria para strings.\n");
        cleanup(in, out, input_str, output_str, k, NULL, l, NULL);
        exit(EXIT_FAILURE);
    }

    input_str[BUFFER_SIZE] = '\0';
    output_str[BUFFER_SIZE] = '\0';

    // Parseo de argumentos
    while ((c = getopt (argc, argv, "LKl:k:x:i:o:h")) != -1){
        switch (c){
            case 'L':
                mode = LENGTH;
                break;
            case 'K':
                mode = KEY;
                break;
            case 'l':
                l = atoi(optarg);
                break;
            case 'k':
                strcpy(k, optarg);
                break;
            case 'x':
                idioma = atoi(optarg);
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
                    fprintf(stderr, "Error. No se pudo abrir el archivo de lectura.\n");
                    out = NULL;
                    error = true;
                }
                break;
            case 'h':
                fprintf(stderr, "%s", help_str);
                cleanup(in, out, input_str, output_str, k, NULL, l, NULL);
                exit(EXIT_SUCCESS);
            default:
                cleanup(in, out, input_str, output_str, k, NULL, l, NULL);
                exit(EXIT_FAILURE);
        }
    }
    if (mode == NONE){
        fprintf(stderr, "Error. No se especificó modo de ejecución.\n");
        error = true;
    }

    if (l < 1){
        fprintf(stderr, "Error. Valor inválido para la l.\n");
        error = true;
    }

    if (idioma != 0 && idioma != 1){
        fprintf(stderr, "Error. Idioma inválido.\n");
        error = true;
    }

    if (error){
        cleanup(in, out, input_str, output_str, k, NULL, l, NULL);
        exit(EXIT_FAILURE);
    }


    double **f = NULL, ic = 0;
    int index;
    double p_real[2][LANG_SIZE] = {{0.1196, 0.0092, 0.0292, 0.0687, 0.1678, 0.0052, 0.0073, 0.0089, 0.0415, 0.0030, 0.0000, 0.0837, 0.0212, 0.0701, 0.0869, 0.0277, 0.0153, 0.0494, 0.0788, 0.0331, 0.0480, 0.0039, 0.0000, 0.0006, 0.0154, 0.0015}, 
                            {0.0804, 0.0154, 0.0306, 0.0399, 0.1251, 0.0230, 0.0196, 0.0549, 0.0726, 0.0016, 0.0067, 0.0414, 0.0253, 0.0709, 0.0760, 0.0200, 0.0011, 0.0612, 0.0654, 0.0925, 0.0271, 0.0099, 0.0192, 0.0019, 0.0173, 0.0019}};
    int *vector_len = NULL;

    // Se reserva memoria para los array
    vector_len = (int*)malloc(l*sizeof(int));
    f = (double**)malloc(l*sizeof(double*));

    if (!f || !vector_len){
        fprintf(stderr, "Error. Error al alocar memoria.\n");
        cleanup(in, out, input_str, output_str, k, f, l, vector_len);
        exit(EXIT_FAILURE);
    }

    for (int i = 0; i < l; ++i){
        f[i] = (double*)malloc(LANG_SIZE*sizeof(double));
        if (!(f[i])){
            fprintf(stderr, "Error. Error al alocar memoria.\n");
            cleanup(in, out, input_str, output_str, k, f, l, vector_len);
            exit(EXIT_FAILURE);
        }
    } 

    // Se inicializan los array
    for (int i = 0; i < l; ++i){
        vector_len[i] = 0;
        for (int j = 0; j < LANG_SIZE; ++j){ 
            f[i][j] = 0;
        }
    }

    if (mode == LENGTH){
        fprintf(stdout, "Aplicando IC para averiguar tamaño de clave. Probando l = %d.\n", l);
    }else{
        fprintf(stdout, "Aplicando IC para averiguar componentes de la clave. Probando l = %d, k = \"%s\"\n", l, k);
    }

    // Se calcula el índice de coincidencia real del idioma
    for (int i = 0; i < LANG_SIZE; ++i){
        ic += (p_real[idioma][i]*p_real[idioma][i]);
    }

    fprintf(stdout, "IC real del idioma = %lf\n\n", ic);

    int k_pos = 0;
    string_transform(k);

    while (file_read(input_str, BUFFER_SIZE, in) > 0){
        for (int j = 0; j < strlen(input_str); ++j, k_pos = ((k_pos+1)%l)){
            // Se encuentra tratando un caracter del vector k_pos
            vector_len[k_pos] += 1;
          
            if (mode == LENGTH){
                index = input_str[j] - 'A';
            }else{
                // Si se está probando la clave, se descifra primero.
                index = input_str[j] - k[k_pos];
                if (index < 0) index += LANG_SIZE;
            }
            f[k_pos][index] += 1;
        }
    }

    // Se convierten las frecuencias a probabilidades

    for (int i = 0; i < l; ++i){
        for (int j = 0; j < LANG_SIZE; ++j){ 
            f[i][j] /= vector_len[i];
        }
    }

    // Se calcula el IC
    for (int i = 0; i < l; ++i){
        ic = 0;
        for (int j = 0; j < LANG_SIZE; ++j){ 
            if (mode == LENGTH){
                ic += (f[i][j]*f[i][j]);
            }else{
                ic += (p_real[idioma][j]*f[i][j]);
            }
        }

        sprintf(output_str, "IC[%d] = %lf\n", i, ic);
        file_write(output_str, out);
    }

    fprintf(stdout, "Finished.\n");
    cleanup(in, out, input_str, output_str, k, f, l, vector_len);
    return 0;
}