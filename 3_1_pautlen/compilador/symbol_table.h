/**
 * 18/11/2020
 * Module: symbol_table
 * --------------------
 * Authors:
 * - Alejandro Benimeli <alejandro.benimeli@estudiante.uam.es>
 * - Daniel Mohedano    <daniel.mohedano@estudiante.uam.es>
 * - Silvia Sopeña      <silvia.sopenna@estudiante.uam.es>
 * -----------------------------------------------------------
 * This module manages the symbol table for the compiler
 */

#ifndef SYMBOL_TABLE_H
#define SYMBOL_TABLE_H
#include "hash_data.h"
#include "hash_table.h"

#define SCOPE_ALREADY_OPEN -2
#define DUPLICATED_DECLARATION -3
#define SCOPE_ALREADY_CLOSED -4

typedef struct{
    hash_table *global;
    hash_table *local;
} symbol_table;


/**
 * Function: symbol_create
 * ------------------
 * Creates a symbol table ADT
 * 
 * returns: the created symbol table
 */
symbol_table *symbol_create(void);

/**
 * Function: symbol_destroy
 * ------------------
 * Frees memory allocated to the symbol table
 * 
 * table: Pointer to the table thats going to be freed
 */
void symbol_destroy(symbol_table *table);

/**
 * Function: symbol_insert
 * ------------------
 * Inserts a DATA element in the table
 * 
 * table: Pointer to the symbol table
 * data: Data to be inserted
 */
int symbol_insert(symbol_table *table, DATA *data);

/**
 * Function: symbol_open_scope
 * ------------------
 * Opens a local scope in the symbol table
 * 
 * data: hash_data object with the information of the function that will be parsed
 */
int symbol_open_scope(symbol_table *table, DATA *data);

/**
 * Function: symbol_open_scope
 * ------------------
 * Closes the local scope in the symbol table
 */
int symbol_close_scope(symbol_table *table);

/**
 * Function: symbol_search
 * ------------------
 * Searches for an identifier in the table
 * 
 * table: the symbol table
 * id: identifier to look for
 * 
 * returns: the DATA structure if it is found,
 *          NULL otherwise
 */
DATA *symbol_search(symbol_table *table, char *id);

#endif /* SYMBOL_TABLE_H */