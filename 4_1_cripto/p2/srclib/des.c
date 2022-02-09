#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include "../includes/constants.h"
#include "../includes/des.h"

void set_bit(uint64_t orig, uint64_t *dest, unsigned short orig_pos, unsigned short dest_pos){
    // Solo necesario hacer set si el bit es 1
    if ((orig << orig_pos & FIRST_BIT) != 0){
        *dest |= (FIRST_BIT >> dest_pos);
    }
}

void key_round(uint64_t *key, uint64_t *future_key, int round){
    uint64_t key_left = 0;
    uint64_t key_right = 0; 

    // 1. Aplicar PC-1 si la ronda es la primera, simplemente dividir en mitades si no
    if (round == 0){
        for (int i = 0; i < BITS_IN_PC1 / 2; ++i){
            set_bit(*key, &key_left, PC1[i] - 1, i);
        }
        for (int i = 0; i < BITS_IN_PC1 / 2; ++i){
            set_bit(*key, &key_right, PC1[BITS_IN_PC1 + i] - 1, i);
        }
    }else{
        key_left = (*key) & LEFT_KEY;
        key_right = ((*key) & RIGHT_KEY) << (BITS_IN_PC1 / 2);
    }

    // 2. Left Circular Shifts
    for (int n_shifts = 0; n_shifts < ROUND_SHIFTS[round]; ++n_shifts){
        set_bit(key_left, &key_left, 0, (BITS_IN_PC1 / 2));
        set_bit(key_right, &key_right, 0, (BITS_IN_PC1 / 2));
        key_left <<= 1;
        key_right <<= 1;
    }

    // 3. Juntar de nuevo las dos mitades
    *future_key = key_left | (key_right >> BITS_IN_PC1 / 2);

    // 4. Aplicar PC-2
    for (int i = 0; i < BITS_IN_PC2; ++i){
        set_bit(*future_key, key, PC2[i] - 1, i);
    }
}

void des_round(uint64_t *block, uint64_t key){
    uint64_t old_left = 0, old_right = 0, new_left = 0, new_right = 0;
    uint64_t f_result = 0;

    // 1. Dividir el bloque en dos mitades
    old_left = (*block) & LEFT_BLOCK;
    old_right = ((*block) & RIGHT_BLOCK) << (BITS_IN_DES / 2);

    // 2. Aplicar función F
    f_des(old_right, &f_result, key);

    // 3. Asignar nuevas mitades
    new_right = old_left ^ f_result;
    new_left = old_right;

    // 4. Juntamos las mitades
    *block = new_left | (new_right >> (BITS_IN_DES / 2));
}

void f_des(uint64_t data, uint64_t *result, uint64_t key){
    uint64_t expansion_result = 0, sub_input = 0, sub_result = 0;

    // 1. Aplicar expansión E
    for (int i = 0; i < BITS_IN_E; ++i){
        set_bit(data, &expansion_result, E[i] - 1, i);
    }

    // 2. XOR con Ki
    sub_input = expansion_result ^ key;

    // 3. Aplicar sustituciones S
    uint64_t group_bits, box_result;
    int s_box_x, s_box_y;

    for (int i = 0; i < NUM_S_BOXES; ++i){
        group_bits = 0; s_box_x = 0; s_box_y = 0; box_result = 0;

        group_bits = (sub_input << (i*6)) & MASK_6_BIT;

        s_box_x = (group_bits & FIRST_BIT) != 0 ? 2 : 0;
        if (((group_bits << 5) & FIRST_BIT) != 0){
            s_box_x += 1;
        }

        for (int j = 1; j < 5; ++j){
            s_box_y *= 2;
            if (((group_bits << j) & FIRST_BIT) != 0){
                ++s_box_y;
            }
        }

        box_result += S_BOXES[i][s_box_x][s_box_y];
        sub_result |= (box_result << (60 - i*4));
    }

    // 4. Aplicar permutación P
    for (int i = 0; i < BITS_IN_P; ++i){
        set_bit(sub_result, result, P[i] - 1, i);
    }
}

void des_full(uint64_t input, uint64_t *output, uint64_t seed, bool cipher){
    uint64_t sub_key[16], future_key = 0;

    // 1. Generación de las subclaves para cada ronda
    sub_key[0] = seed;
    for (int i = 0; i < 16; ++i){
        key_round(&sub_key[i], &future_key, i);
        if (i < 15){
            sub_key[i + 1] = future_key;
        }   
    }

    // 2. Aplicar IP
    uint64_t ip_result = 0;
    for (int i = 0; i < BITS_IN_IP; ++i){
        set_bit(input, &ip_result, IP[i] - 1, i);
    }

    // 3. Aplicar 16 rondas Feistel
    uint64_t round_result = ip_result;
    for (int i = 0; i < 16; ++i){
        if (cipher == true) des_round(&round_result, sub_key[i]);
        else des_round(&round_result, sub_key[15 - i]);
    }

    // 4. Swap de bits
    round_result = (round_result << (BITS_IN_DES / 2)) | (round_result >> (BITS_IN_DES / 2));

    // 5. Aplicar IP_INV
    for (int i = 0; i < BITS_IN_IP; ++i){
        set_bit(round_result, output, IP_INV[i] - 1, i);
    }
}

bool key_check(uint64_t key){
    uint64_t ones;

    // Se comprueba cada grupo de 8b
    for (int group = 0; group < 8; ++group){
        ones = 1;
        // Se cuenta la cantidad de 1s en cada grupo
        for (int i = 0; i < 7; ++i){
            if (((key << (group*8 + i)) & FIRST_BIT) != 0) ++ones;
        }

        // Se comprueba que el 8o bit concuerde con la cuenta
        ones = ones % 2;

        if ((ones << 63) != ((key << (group*8 + 7)) & FIRST_BIT)) return false;
    }

    return true;
}
