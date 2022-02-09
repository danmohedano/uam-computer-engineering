/**
 * 11/11/2020
 * Módulo: sbox_aes.c
 * -----------------
 * Authors:
 * - Daniel Mohedano    <daniel.mohedano@estudiante.uam.es>
 * - Silvia Sopeña      <silvia.sopenna@estudiante.uam.es>
 * -----------------------------------------------------------
 * Este módulo calcula la S-BOX para el AES.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>
#include <stdint.h>
#include "../includes/constants.h"

void cleanup(FILE *out){
    if (out && out != stdout) fclose(out);
}

int degree(uint16_t x){
    int deg = -1;
    for (int i = 0; i < 16; ++i){
        // Se comprueba el bit i por la derecha
        if (((x >> i) & 1u) != 0) deg = i;
    }

    return deg;
}

void division(uint16_t m, uint16_t a, uint8_t *q, uint8_t *r){
    int dm = degree(m), da = degree(a), dr = 0;
    uint16_t aux = 0u; 
    *q = 1u; *r = 1u;

    if (da > dm){
        *q = 0u;
        *r = m;
        return;
    } else if (a == 0){
        *q = m;
        *r = 0u;
    }

    while (dm >= da){
        aux = a << (dm - da);
        *r = m ^ aux;
        dr = degree(*r);

        if (dr >= da){
            *q = (*q << (dm - dr)) + 1;
        }else{
            *q = *q << (dm - da);
        }
        
        if (*r == 0) return;
        m = *r;
        dm = degree(m);
    }

    return;
}

uint8_t xtime(uint8_t x){
    if ((x & 0b10000000) != 0){
        return 0x1B ^ (x << 1);
    }else{
        return x << 1;
    }
}

uint8_t multiplicacion(uint8_t x, uint8_t y){
    uint8_t xtimes[8];
    uint8_t result = 0u;

    xtimes[0] = x;
    for (int i = 1; i < 8; ++i){
        xtimes[i] = xtime(xtimes[i-1]);
    }

    for (int i = 0; i < 8; ++i){
        if (((y >> i) & 1u) != 0){
            result = result ^ xtimes[i];
        } 
    }
    return result;
}

void euclides_extendido(uint16_t m, uint8_t a, uint8_t *inv_a){
    /* Aplicando el teorema de Bezout como:
        ri = m x ui + a x vi
    */
    uint16_t old_r;
    uint8_t r, old_u, u, old_v, v, qi, temp;

    if (a == 0u){
        *inv_a = 0u;
        return;
    }

    old_r = m; r = a;
    old_u = 1u; u = 0u;
    old_v = 0u; v = 1u;
    qi = 0u; temp = 0u;

    while (r != 0u){
        // Cálculo de qi
        division(old_r, r, &qi, &temp);

        // Actualizar r(i+1) = r(i-1) XOR q(i)r(i)
        old_r = r;
        r = temp;
        
        // Actualizar u(i+1) = u(i-1) XOR q(i)u(i)
        temp = u;
        u = old_u ^ multiplicacion(qi, u);
        old_u = temp;

        // Actualizar v(i+1) = v(i-1) XOR q(i)v(i)
        temp = v;
        v = old_v ^ multiplicacion(qi, v);
        old_v = temp;
    }

    *inv_a = old_v;
    return;
}

void transformacion_afin(uint8_t a, uint8_t *b, bool direct, uint16_t m){

    if (direct) euclides_extendido(m, a, &a);

    // Multiplicación del byte por la matriz
    uint8_t mul = 0;
    uint8_t x;
    int ones = 0; 
    *b = 0u;

    if (direct){
        x = 0b11110001;
    }else{
        x = 0b10100100;
    }

    for (int i = 0; i < 8; ++i){
        mul = x & a;

        // Comprobar si el bit vale 1 o 0
        ones = 0;
        for (int j = 0; j < 8; ++j){
            if (((mul >> j) & 1u) != 0) ++ones;
        }

        if (ones % 2){
            *b = *b | (1u << i);
        }

        // Rotación a la izquierda de x
        x = (x << 1) | (x >> 7);
    }

    // Suma de la constante
    if (direct){
        *b = *b ^ 0b01100011;
    }else{
        *b = *b ^ 0b00000101;
        euclides_extendido(m, *b, b);
    }
    return;
}

int main(int argc, char **argv)
{
    int c;
    FILE *out = stdout;
    enum {CYPHER, DECYPHER, NONE} mode = NONE;
    char* help_str = "Uso: sbox_aes.exe {-C | -D} [-o fileout]\n";
    bool error = false; 

    // Parseo de argumentos
    while ((c = getopt (argc, argv, "CDo:h")) != -1){
        switch (c){
            case 'C':
                mode = CYPHER;
                break;
            case 'D':
                mode = DECYPHER;
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
                cleanup(out);
                exit(EXIT_SUCCESS);
            default:
                cleanup(out);
                exit(EXIT_FAILURE);
        }
    }

    if (mode == NONE){
        fprintf(stderr, "Error. No se especificó modo de operación.\n");
        error = true;
    }

    if (error){
        cleanup(out);
        exit(EXIT_FAILURE);
    }

    uint16_t m = 0b0000000100011011; // x^8+x^4+x^3+x+1
    uint8_t result;
    uint8_t sbox[256];

    if (mode == CYPHER){
        printf("Calculando AES SBOX Directa:\n");
    }else{
        printf("Calculando AES SBOX Inversa:\n");
    }

    for (uint a = 0; a < 256u; ++a){
        transformacion_afin(a, &result, mode == CYPHER, m);
        sbox[a] = result;
    }

    for (int i = 0; i < 16; ++i){
        for (int j = 0; j < 16; ++j){
            fprintf(out, "%02X ", sbox[i*16 + j]);
        }
        fprintf(out, "\n");
    }

    cleanup(out);    
    
    return 0;
}