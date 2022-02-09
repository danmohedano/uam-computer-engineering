/**
 * 18/11/2020
 * Module: hash_table
 * ------------------
 * Authors:
 * - Alejandro Benimeli <alejandro.benimeli@estudiante.uam.es>
 * - Daniel Mohedano    <daniel.mohedano@estudiante.uam.es>
 * - Silvia Sopeña      <silvia.sopenna@estudiante.uam.es>
 * -----------------------------------------------------------
 * Module that manages the hash table used by the symbol table for the scopes
 */
#ifndef HASH_TABLE_H
#define HASH_TABLE_H

#include "hash_data.h"

#define TABLE_SIZE 127 // Should be a prime number

typedef struct _hash_table hash_table;

/**
 * Function: hash_create
 * ------------------
 * Creates a hash table ADT
 * 
 * returns: the created hash table
 */
hash_table *hash_create(void);

/**
 * Function: hash_destroy
 * ------------------
 * Frees memory allocated to the hash table
 * 
 * table: Pointer to the table thats going to be freed
 */
void hash_destroy(hash_table *table);

/**
 * Function: hash_insert
 * ------------------
 * Inserts a DATA element in the table
 * 
 * table: Pointer to the hash table
 * data: Data to be inserted
 */
int hash_insert(hash_table *table, DATA *data);

/**
 * Function: hash_search
 * ------------------
 * Searches for an identifier in the table
 * 
 * table: the hash table
 * id: identifier to look for
 * 
 * returns: the DATA structure if it is found,
 *          NULL otherwise
 */
DATA *hash_search(hash_table *table, char *id);

/**
 * PRIVATE function EXCLUSIVELY MADE FOR DEBUGGING the hash table
 * Please dont use
 */
int hash_print(hash_table *table);

#endif