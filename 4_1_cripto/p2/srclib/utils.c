#include "../includes/utils.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "../includes/constants.h"

int euclides_extended(mpz_t m, mpz_t a, mpz_t inverse_a){
    /* Aplicando el teorema de Bezout como:
        ri = m x ui + a x vi
    */
    mpz_t old_r, r, old_u, u, old_v, v, qi, temp;
    int gcd1 = 0;

    mpz_init_set(old_r, m); mpz_init_set(r, a);
    mpz_init_set_ui(old_u, 1); mpz_init_set_ui(u, 0);
    mpz_init_set_ui(old_v, 0); mpz_init_set_ui(v, 1);
    mpz_init(qi);
    mpz_init(temp);

    // Bucle para calcular qi y actualizar los valores
    while(mpz_cmp_ui(r, 0)){
        // Cálculo de qi
        mpz_tdiv_q(qi, old_r, r);

        // Actualizar r(i+1) = r(i-1) - q(i)r(i)
        mpz_set(temp, r);
        mpz_mul(r, qi, r);
        mpz_sub(r, old_r, r);
        mpz_set(old_r, temp);

        // Actualizar u(i+1) = u(i-1) - q(i)u(i)
        mpz_set(temp, u);
        mpz_mul(u, qi, u);
        mpz_sub(u, old_u, u);
        mpz_set(old_u, temp);

        // Actualizar v(i+1) = v(i-1) - q(i)v(i)
        mpz_set(temp, v);
        mpz_mul(v, qi, v);
        mpz_sub(v, old_v, v);
        mpz_set(old_v, temp);
    }

    // Guardar el inverso de a
    if (mpz_cmp_ui(old_v, 0) < 0) mpz_add(old_v, old_v, m);
    mpz_set(inverse_a, old_v);

    if (mpz_cmp_ui(old_r, 1) == 0) gcd1 = 1;

    mpz_clear(old_r); mpz_clear(r);
    mpz_clear(old_u); mpz_clear(u);
    mpz_clear(old_v); mpz_clear(v);
    mpz_clear(qi); mpz_clear(temp);

    return gcd1;
}

int rand_equiprobable(int m){
    int result;
    int block_limit = (RAND_MAX / m) * m;
    do{
        result = rand();
    } while (result >= block_limit);

    return result % m;
}

void afin_key_equiprobable(mpz_t a, mpz_t b){
    int pos = rand_equiprobable(N_CLAVES_AFIN);

    mpz_set_ui(a, AFIN_CLAVES[pos][0]);
    mpz_set_ui(b, AFIN_CLAVES[pos][1]);
}

void afin_key_noequiprobable(mpz_t a, mpz_t b){
    int pos = 1;

    pos = rand_equiprobable(N_CLAVES_AFIN);
    
    if (pos % 5){
        pos += 1;
    }

    mpz_set_ui(a, AFIN_CLAVES[pos][0]);
    mpz_set_ui(b, AFIN_CLAVES[pos][1]);
}

void string_transform(char *string){
    long len = strlen(string);
    long correct_chars = 0;
    
    for (long i = 0; i < len; ++i){
        if ('a' <= string[i] && string[i] <= 'z') string[i] += 'A' - 'a';
        if ('A' <= string[i] && string[i] <= 'Z'){
            string[correct_chars++] = string[i];
        }
    }
    string[correct_chars] = '\0';
}