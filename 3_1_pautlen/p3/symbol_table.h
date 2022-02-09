/**
 * 18/11/2020
 * Module: symbol_table
 * --------------------
 * Authors:
 * - Alejando Bewnimeli <alejandro.benimeli@estudiante.uam.es>
 * - Daniel Mohedano    <daniel.mohedano@estudiante.uam.es>
 * - Silvia Sopeña      <silvia.sopenna@estudiante.uam.es>
 * -----------------------------------------------------------
 * This module manages the symbol table for the compiler
 */

#ifndef SYMBOL_TABLE_H
#define SYMBOL_TABLE_H
#include "hash_data.h"

typedef struct _symbol_table symbol_table;


symbol_table *symbol_create(void);

void symbol_destroy(symbol_table *table);

int symbol_insert(symbol_table *table, DATA *data);

DATA *symbol_search(symbol_table *table, char *id);

#endif /* SYMBOL_TABLE_H */