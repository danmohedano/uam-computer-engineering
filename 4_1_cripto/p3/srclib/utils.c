#include "../includes/utils.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>
#include "../includes/constants.h"

void residuos_mr_cleanup(mpz_t result, mpz_t p_1, mpz_t i, mpz_t k_2);


void potenciacion_modular_optima(mpz_t base, mpz_t exp, mpz_t m, mpz_t result){
    size_t l = mpz_sizeinbase(exp, 2);

    mpz_set_ui(result, 1);
    for (int i = l - 1; i >= 0; --i){
        mpz_mul(result, result, result);
        if (mpz_tstbit(exp, i) == 1){
            mpz_mul(result, result, base);
        }
        mpz_mod(result, result, m);
    }
}

void candidato_aleatorio(mpz_t p, gmp_randstate_t rstate, int n){
    mpz_urandomb(p, rstate, n);
    mpz_setbit(p, n - 1);
    mpz_setbit(p, 0);
}

void residuos_mr_cleanup(mpz_t result, mpz_t p_1, mpz_t i, mpz_t k_2){
    mpz_clear(result); mpz_clear(p_1); mpz_clear(i); mpz_clear(k_2);
}

bool residuos_mr(mpz_t a, mpz_t k, mpz_t m, mpz_t p){
    mpz_t result, p_1, i, k_2;

    mpz_init(result); mpz_init(p_1); mpz_init(i); mpz_init(k_2);
    mpz_sub_ui(p_1, p, 1); mpz_sub_ui(k_2, k, 2);

    // Iteración 1: a^m mod p
    mpz_powm(result, a, m, p);
    if (mpz_cmp_ui(result, 1) == 0 || mpz_cmp(result, p_1) == 0){
        residuos_mr_cleanup(result, p_1, i, k_2);
        return false;
    }

    for (mpz_set_ui(i, 0); mpz_cmp(i, k_2) < 0; mpz_add_ui(i, i, 1)){
        mpz_powm_ui(result, result, 2, p);
        if (mpz_cmp_ui(result, 1) == 0){
            residuos_mr_cleanup(result, p_1, i, k_2);
            return true;
        }else if (mpz_cmp(result, p_1) == 0){
            residuos_mr_cleanup(result, p_1, i, k_2);
            return false;
        }
    }

    // Iteración k: a^2^k-1 * m
    mpz_powm_ui(result, result, 2, p);
    if (mpz_cmp_ui(result, 1) == 0){
        residuos_mr_cleanup(result, p_1, i, k_2);
        return true;
    }else if (mpz_cmp(result, p_1) == 0){
        residuos_mr_cleanup(result, p_1, i, k_2);
        return false;
    }else{
        residuos_mr_cleanup(result, p_1, i, k_2);
        return true;
    }

}

bool miller_rabin(mpz_t p, int iter){
    mpz_t prime_i, p_1, k, m, aux_gmp, a;

    mpz_init(prime_i);

    // 1. Comprobar los primeros 2000 primos.
    for (int i = 0; i < 2000; ++i){
        mpz_set_ui(prime_i, PRIMOS[i]);
        if (mpz_divisible_p(p, prime_i) != 0){
            mpz_clear(prime_i);
            return true;
        }
    }

    mpz_clear(prime_i);

    // 2. Calcular iteraciones de residuos
    // 2a. p-1 = 2^k * m
    mpz_init(p_1); mpz_init(k); mpz_init(m); mpz_init(aux_gmp); mpz_init(a);
    
    mpz_sub_ui(p_1, p, 1);
    mpz_set_ui(k, 0);
    mpz_set(aux_gmp, p_1);

    while (mpz_divisible_ui_p(aux_gmp, 2) != 0) {
        mpz_add_ui(k, k, 1);
        mpz_divexact_ui(aux_gmp, aux_gmp, 2);
    }

    mpz_set(m, aux_gmp);

    // 2b. Iteraciones de residuos para base a
    for (int i = 0; i < iter; ++i){
        // mpz_urandomm 
        mpz_init_set_ui(a, 2 + i);
        if (residuos_mr(a, k, m, p) == true){
            mpz_clear(p_1); mpz_clear(k); mpz_clear(m); mpz_clear(aux_gmp); mpz_clear(a);
            return true;
        }
    }

    return false;
}

void gen_rsa(int bits, double prob, mpz_t p, mpz_t q, mpz_t n, mpz_t e, mpz_t d, gmp_randstate_t rstate){
    double aux;
    int iter;
    mpz_t euler_n, aux_gmp, gcd;

    mpz_init(euler_n); mpz_init(aux_gmp); mpz_init(gcd);

    // Calcular cantidad de tests necesarios para asegurar probabilidad de error
    aux = log(bits/2*log(2)*((1 / prob) - 1)) / log(4);
    iter = ceil(aux);

    // 1. Generar número aleatorio P y Q primos
    candidato_aleatorio(p, rstate, bits/2);
    while (miller_rabin(p, iter)){
        mpz_add_ui(p, p, 2);
    }
    
    candidato_aleatorio(q, rstate, bits/2);
    while (miller_rabin(q, iter)){
        mpz_add_ui(q, q, 2);
    }

    // 2. Calcular Euler(n)
    mpz_mul(n, p, q);
    mpz_sub_ui(p, p, 1); mpz_sub_ui(q, q, 1);
    mpz_mul(euler_n, p, q);
    mpz_add_ui(p, p, 1); mpz_add_ui(q, q, 1);

    // 3. Generar e con mcd(e, euler_n) == 1
    mpz_sub_ui(aux_gmp, euler_n, 3);

    bool flag_mcd = true;
    while(flag_mcd){
        mpz_urandomm(e, rstate, aux_gmp);
        mpz_add_ui(e, e, 2);
        mpz_gcd(gcd, e, euler_n);
        if (mpz_cmp_ui(gcd, 1) == 0) flag_mcd = false;
    }

    // 4. Generar d = e^-1 
    mpz_invert(d, e, euler_n);

    mpz_clear(euler_n); mpz_clear(aux_gmp); mpz_clear(gcd);
}

bool residuos_vegas(mpz_t w, mpz_t t, mpz_t m, mpz_t n, mpz_t x){
    mpz_t aux, n_1, i;
    mpz_init(aux); mpz_init(n_1); mpz_init(i);
    mpz_sub_ui(n_1, n, 1);

    // 1. Iteración 1
    mpz_powm(x, w, m, n);

    if (mpz_cmp_ui(x, 1) == 0 || mpz_cmp(x, n_1) == 0){
        mpz_clear(aux); mpz_clear(n_1); mpz_clear(i);
        return false;
    }

    mpz_set(aux, x);
    // 2. Iteraciones hasta t-1
    for (mpz_set_ui(i, 2); mpz_cmp(i, t) < 0; mpz_add_ui(i, i, 1)){
        mpz_powm_ui(aux, aux, 2, n);
        if (mpz_cmp_ui(aux, 1) == 0){
            mpz_clear(aux); mpz_clear(n_1); mpz_clear(i);
            return true;
        }else if (mpz_cmp(aux, n_1) == 0){
            mpz_clear(aux); mpz_clear(n_1); mpz_clear(i);
            return false;
        }
        mpz_set(x, aux);
    }

    // Iteración t: a^2^t-1 * m
    mpz_powm_ui(aux, aux, 2,  n);
    if (mpz_cmp_ui(aux, 1) == 0){
        mpz_clear(aux); mpz_clear(n_1); mpz_clear(i);
        return true;
    }else if (mpz_cmp(aux, n_1) == 0){
        mpz_clear(aux); mpz_clear(n_1); mpz_clear(i);
        return false;
    }else{
        mpz_clear(aux); mpz_clear(n_1); mpz_clear(i);
        return true;
    }
}

void vegas(mpz_t n, mpz_t e, mpz_t d, mpz_t result_1, mpz_t result_2, gmp_randstate_t rstate){
    mpz_t t, m, w, aux, gcd, x;

    mpz_init(t); mpz_init(m); mpz_init(w); mpz_init(aux); mpz_init(gcd); mpz_init(x);

    // 1. ed - 1 = 2^t * m
    mpz_mul(aux, e, d);
    mpz_sub_ui(aux, aux, 1);
    mpz_set_ui(t, 0);

    while (mpz_divisible_ui_p(aux, 2) != 0) {
        mpz_add_ui(t, t, 1);
        mpz_divexact_ui(aux, aux, 2);
    }
    mpz_set(m, aux);

    
    bool flag_loop = true;
    while (flag_loop){
        // 2. Elegir base aleatoria 1 < w < n - 1
        mpz_sub_ui(n, n, 4);
        mpz_urandomm(w, rstate, n);
        mpz_add_ui(w, w, 2); mpz_add_ui(n, n, 4);

        // 3. Comprobar si mcd(w, n) != 1
        mpz_gcd(gcd, w, n);
        if (mpz_cmp_ui(gcd, 1) != 0){
            flag_loop = false;
            mpz_set(result_1, w);
            mpz_divexact(result_2, n, w);
        }else{
            // 4. Se calculan los residuos
            if (residuos_vegas(w, t, m, n, x)){
                flag_loop = false;
                mpz_add_ui(x, x, 1);
                mpz_gcd(result_1, x, n);
                mpz_sub_ui(x, x, 2);
                mpz_gcd(result_2, x, n);
            }
        }
    }

    mpz_clear(t); mpz_clear(m); mpz_clear(w); mpz_clear(aux); mpz_clear(gcd); mpz_clear(x);
}