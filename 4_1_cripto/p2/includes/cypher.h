/**
 * 07/10/2021
 * Módulo: cypher
 * -----------------
 * Autores:
 * - Daniel Mohedano    <daniel.mohedano@estudiante.uam.es>
 * - Silvia Sopeña      <silvia.sopenna@estudiante.uam.es>
 * -----------------------------------------------------------
 * Este módulo alberga las funciones encargadas de cifrado y descifrado.
 */

#ifndef CYPHER_H
#define CYPHER_H

#include <gmp.h>
#include <stdint.h>

/**
 * afin_cifrado
 * 
 * Aplica la operación de cifrado del cifrado Afín: y = x*a + b mod m.
 * 
 * Inputs:
 *      x (mpz_t): Valor a cifrar.
 *      a (mpz_t): Clave multiplicativa.
 *      b (mpz_t): Clave aditiva.
 *      m (mpz_t): Módulo a aplicar.
 * Outputs:
 *      y (mpz_t): Resultado del cifrado.
 */
void afin_cifrado(mpz_t x, mpz_t a, mpz_t b, mpz_t m, mpz_t y);

/**
 * afin_descifrado
 * 
 * Aplica la operación de descifrado del cifrado Afín: x = (y-b)*a^-1 mod m.
 * 
 * Inputs:
 *      y (mpz_t): Valor a descifrar.
 *      a_inv (mpz_t): Clave multiplicativa inversa.
 *      b (mpz_t): Clave aditiva.
 *      m (mpz_t): Módulo a aplicar.
 * Outputs:
 *      x (mpz_t): Resultado del descifrado.
 */
void afin_descifrado(mpz_t y, mpz_t a_inv, mpz_t b, mpz_t m, mpz_t x);

#endif