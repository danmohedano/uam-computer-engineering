#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "symbol_table.h"
#include "hash_table.h"

#define SCOPE_CLOSE "cierre"
#define SCOPE_CLOSE_VALUE -999

struct _symbol_table{
    hash_table *global;
    hash_table *local;
};

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

    if (table->local){
        if (data_cmp_id(data, SCOPE_CLOSE) == 0 && data_get_type(data) == SCOPE_CLOSE_VALUE){
            // Closing local scope
            data_destroy(data);
            hash_destroy(table->local);
            table->local = NULL;
            return 0;
        }
        return hash_insert(table->local, data);
    }

    if (data_get_type(data) < 0){
        // Opening new scope
        if (hash_insert(table->global, data) != 0) return -1;
        table->local = hash_create();
        if (!(table->local)) return -1;
        return hash_insert(table->local, data_copy(data));
    }
    return hash_insert(table->global, data);
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