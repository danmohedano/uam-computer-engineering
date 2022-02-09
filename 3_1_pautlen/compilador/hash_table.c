#include <stdlib.h>
#include <stdio.h>
#include "hash_table.h"

typedef struct _node {
    DATA *data;
    struct _node *next;
} node;

struct _hash_table {
    node *positions[TABLE_SIZE];
};

node *node_create(DATA *data);
void node_destroy(node *n);



hash_table *hash_create(void){
    hash_table *table = (hash_table *)malloc(sizeof(hash_table));
    if (table == NULL){
        fprintf(stderr, "Error creating a hash table.\n");
        return NULL;
    }
    // The first node of every linked list is the head and doesnt contain data
    for (int i=0; i<TABLE_SIZE; ++i){
        table->positions[i] = node_create(NULL);
    }
    return table;
}


void hash_destroy(hash_table *table){
    if(table == NULL) return;
    for (int i=0; i<TABLE_SIZE; ++i){
        node_destroy(table->positions[i]);
    }
    free(table);
}

int hash_insert(hash_table *table, DATA *data){
    if (table == NULL || data == NULL){
        fprintf(stderr, "Error inserting an element in the hash table. 'table' or 'data' is NULL.\n");
        return -1;
    }
    node *ptr = table->positions[(data_hash(data) % TABLE_SIZE)];
    while (ptr->next != NULL){
        ptr = ptr->next;
        if (data_cmp(ptr->data, data) == 0){
            data_destroy(data);
            return -3; // The element is already inside the table
        }
    }

    ptr->next = node_create(data);

    return 0;
}

DATA *hash_search(hash_table *table, char *id){
    node *head = NULL;
    if (!table || !id){
        fprintf(stderr,"Error searching for identifier. Null pointer.\n");
        return NULL;
    }
    
    head = table->positions[hash_str(id) % TABLE_SIZE];
    while (head->next != NULL){
        head = head->next;
        if (data_cmp_id(head->data, id) == 0){
            return head->data;
        }
    }
    return NULL;
}

int hash_print(hash_table *table){
    printf("Hash Table:\n");

    for (int i=0; i<TABLE_SIZE; ++i){
        printf("\t%d: ", i);
        node *ptr = table->positions[i]->next;
        while (ptr != NULL){
            printf(" --> ");
            data_print(stdout, ptr->data);
            ptr = ptr->next;
        }
        printf(" --> NULL\n");
    }
}


/**
 * Function: node_create
 * ------------------
 * Creates a node structure
 * 
 * data: the data pointer
 * 
 * returns: the created node
 */
node *node_create(DATA *data){
    node *n = (node *)malloc(sizeof(node));
    if (n == NULL){
        fprintf(stderr, "Error creating a node.\n");
        return NULL;
    }
    n->data = data;
    n->next = NULL;
    return n;
}

/**
 * Function: node_destroy
 * ------------------
 * Frees a node structure
 * 
 * n: Pointer to the node that will be deleted
 */
void node_destroy(node *n){
    if (n == NULL) {
        return;
    }
    node_destroy(n->next);
    data_destroy(n->data);
    free(n);
}


