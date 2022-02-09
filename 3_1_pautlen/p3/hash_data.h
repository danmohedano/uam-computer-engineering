/**
 * 18/11/2020
 * Module: hash_data
 * -----------------
 * Authors:
 * - Alejandro Benimeli <alejandro.benimeli@estudiante.uam.es>
 * - Daniel Mohedano    <daniel.mohedano@estudiante.uam.es>
 * - Silvia Sopeña      <silvia.sopenna@estudiante.uam.es>
 * -----------------------------------------------------------
 * This module manages the data stored in the hash table by module hash_table.h
 */

#ifndef HASH_DATA_H
#define HASH_DATA_H
#include <stdlib.h>
#include <stdio.h>

typedef struct _DATA{
    char* id;
    int type;
} DATA;

/**
 * Function: data_create
 * ---------------------
 * Creates the DATA structure
 * 
 * id: String with the identifier
 * type: type to store with the identifier
 * 
 * returns: the DATA structure created
 */
DATA *data_create(char *id, int type);

/**
 * Function: data_destroy
 * ---------------------
 * Frees all the memory associated with a DATA structure
 * 
 * data: the data to be freed
 */
void data_destroy(DATA *data);

/**
 * Function: data_copy
 * ---------------------
 * Creates a copy of a given DATA structure
 * 
 * data: the data to be copied
 * 
 * returns: the DATA structure created
 */
DATA *data_copy(DATA *data);

/**
 * Function: data_cmp
 * ---------------------
 * Compares two DATA structures
 * 
 * data1: first DATA to compare
 * data2: second DATA to compare
 * 
 * returns: the result of the comparison
 */
int data_cmp(DATA *data1, DATA *data2);

/**
 * Function: data_cmp_id
 * ---------------------
 * Compares a DATA structure with a given identifier
 * 
 * data1: DATA to compare
 * id2: identifier to compare
 * 
 * returns: the result of the comparison
 */
int data_cmp_id(DATA *data1, char *id2);

/**
 * Function: data_print
 * ---------------------
 * Prints the data structure using the given file pointer
 * 
 * pf: file pointer
 */
void data_print(FILE *pf, DATA *data);

/**
 * Function: data_hash
 * ---------------------
 * Hashes the data
 * 
 * data: data to be hashed
 * 
 * returns: the hash value
 */
unsigned long data_hash(DATA *data);

/**
 * Function: hash_str
 * ---------------------
 * Hashes a string
 * 
 * str: string to be hashed
 * 
 * returns: the hash value
 */
unsigned long hash_str(unsigned char *str);


/**
 * Function: data_get_type
 * ---------------------
 * Returns the type of the DATA structure
 * 
 * data: the DATA structure
 * 
 * returns: the type (int)
 */
int data_get_type(DATA *data);
#endif