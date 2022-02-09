

#ifndef DES_H
#define DES_H

#include <stdint.h>
#include <stdlib.h>
#include <stdbool.h>


void set_bit(uint64_t orig, uint64_t *dest, unsigned short orig_pos, unsigned short dest_pos);

void key_round(uint64_t *key, uint64_t *future_key, int round);

void des_round(uint64_t *block, uint64_t key);

void f_des(uint64_t data, uint64_t *result, uint64_t key);

void des_full(uint64_t input, uint64_t *output, uint64_t seed, bool cipher);

bool key_check(uint64_t key);

#endif