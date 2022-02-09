/**
 * 23/09/2021
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

/**--------------------------------------------------------------------------**/
/**-------------------------------UTILIDAD MCD-------------------------------**/
/**--------------------------------------------------------------------------**/
/**
 * euclides_extended
 * 
 * Aplica el algoritmo de Euclides extendido para calcular tanto el mcd(m,a) 
 * como el inverso multiplicativo de a.
 * 
 * Inputs:
 *      m (mpz_t): Número m.
 *      a (mpz_t): Número a.
 * Outputs:
 *      inverse_a (mpz_t): Inverso multiplicativo de a en Zm (valor real solo 
 *                         si mcd(m,a)==1).
 *      (int): 1 si mcd(m,a) == 1, 0 en cualquier otro caso.
 */
int euclides_extended(mpz_t m, mpz_t a, mpz_t inverse_a);

/**--------------------------------------------------------------------------**/
/**-----------------------------UTILIDAD RANDOM------------------------------**/
/**--------------------------------------------------------------------------**/
int rand_equiprobable(int m);
void afin_key_equiprobable(mpz_t a, mpz_t b);
void afin_key_noequiprobable(mpz_t a, mpz_t b);

/**--------------------------------------------------------------------------**/
/**-----------------------------UTILIDAD STRINGS-----------------------------**/
/**--------------------------------------------------------------------------**/
/**
 * string_transform
 * 
 * Transforma la string proporcionada para convertir los caracteres a mayúscula
 * y elimina cualquier caracter no alfabético.
 * 
 * Inputs:
 *      string (char*): String que transformar. Debe finalizar con '\0'.
 */
void string_transform(char *string);


#endif