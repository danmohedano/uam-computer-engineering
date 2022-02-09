/**
 * 08/12/2021
 * Módulo: utils
 * -----------------
 * Autores:
 * - Daniel Mohedano    <daniel.mohedano@estudiante.uam.es>
 * - Silvia Sopeña      <silvia.sopenna@estudiante.uam.es>
 * -----------------------------------------------------------
 * Este módulo alberga funciones auxiliares.
 */

#ifndef UTILS_H
#define UTILS_H

#include <gmp.h>
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

void potenciacion_modular_optima(mpz_t base, mpz_t exp, mpz_t m, mpz_t result);

void candidato_aleatorio(mpz_t p, gmp_randstate_t rstate, int n);

bool residuos_mr(mpz_t a, mpz_t k, mpz_t m, mpz_t p);

bool miller_rabin(mpz_t p, int iter);

void gen_rsa(int bits, double prob, mpz_t p, mpz_t q, mpz_t n, mpz_t e, mpz_t d, gmp_randstate_t rstate);

bool residuos_vegas(mpz_t w, mpz_t t, mpz_t m, mpz_t n, mpz_t x);

void vegas(mpz_t n, mpz_t e, mpz_t d, mpz_t result_1, mpz_t result_2, gmp_randstate_t rstate);
#endif