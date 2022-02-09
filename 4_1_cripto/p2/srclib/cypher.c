#include "../includes/cypher.h"
#include "../includes/utils.h"
#include <stdio.h>
#include <stdlib.h>

void afin_cifrado(mpz_t x, mpz_t a, mpz_t b, mpz_t m, mpz_t y){
    mpz_mul(y, a, x);
    mpz_add(y, y, b);
    mpz_mod(y, y, m);
}

void afin_descifrado(mpz_t y, mpz_t a_inv, mpz_t b, mpz_t m, mpz_t x){
    mpz_sub(x, y, b);
    mpz_mul(x, x, a_inv);
    mpz_mod(x, x, m);
}