#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "symbol_table.h"
#include "hash_table.h"

#define SCOPE_CLOSE "cierre"
#define SCOPE_CLOSE_VALUE -999


symbol_table *symbol_create(void){
    symbol_table *table = (symbol_table*)malloc(sizeof(symbol_table));
    if (!table){
        fprintf(stderr, "Error creating symbol table.\n");
        return NULL;
    }

    table->global = hash_create();
    if (!(table->global)){
        symbol_destroy(table);
        return NULL;
    }

    table->local = NULL;
    return table;
}

void symbol_destroy(symbol_table *table){
    if (!table) return;
    if (table->global) hash_destroy(table->global);
    if (table->local) hash_destroy(table->local);
    free(table);
}

int symbol_insert(symbol_table *table, DATA *data){
    if (!table || !data){
        fprintf(stderr, "Error inserting DATA into symbol table.\n");
        return -1;
    }

    // Check if there is a local scope opened
    if (table->local){
        return hash_insert(table->local, data);
    }
    else{
        return hash_insert(table->global, data);
    }
}

int symbol_open_scope(symbol_table *table, DATA *data){
    if (!table || !data){
        fprintf(stderr, "Error opening scope.\n");
        return -1;
    }

    /* Check if the local scope already exists */
    if (table->local){
        fprintf(stderr, "Error opening scope. Scope already exists\n");
        return SCOPE_ALREADY_OPEN;
    }

    /* Check if the function already is defined */
    if (symbol_search(table, data->id) != NULL){
        return DUPLICATED_DECLARATION;
    }

    // Opening new scope and inserting function in both scopes
    if (hash_insert(table->global, data) != 0) return -1;
    table->local = hash_create();
    if (!(table->local)) return -1;
    if (hash_insert(table->local, data_copy(data)) != 0) return -1;

    return 0;
}

int symbol_close_scope(symbol_table *table){
    if(!table) return -1;

    // Check if the scope is already closed
    if (!(table->local)){
        fprintf(stderr, "Scope already closed\n");
        return SCOPE_ALREADY_CLOSED;
    }

    hash_destroy(table->local);
    table->local = NULL;

    return 0;
}

DATA *symbol_search(symbol_table *table, char *id){
    DATA *res;
    if(!table || !id) return NULL;
    
    if(table->local){
        res = hash_search(table->local, id);
        if (res != NULL) return res; // It found something
    }
    return hash_search(table->global, id);
}