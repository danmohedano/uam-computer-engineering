#include "hash_data.h"
#include <string.h>


DATA *data_create(char *id, int type){
    DATA *data = NULL;
    char *id_copy = NULL;

    // Check that the id provided is a valid one
    if (!id){
        fprintf(stderr, "Error creating data. Null pointer.\n");
        return NULL;
    }

    // Allocate memory for the data
    data = (DATA*)malloc(sizeof(DATA));
    if (!data){
        fprintf(stderr, "Error creating data. Unable to allocate memory.\n");
        return NULL;
    }

    // Copy the identifier provided
    id_copy = strdup(id);
    if (!id_copy){
        fprintf(stderr, "Error creating data. Unable to copy identifier.\n");
        data_destroy(data);
        return NULL;
    }

    data->id = id_copy;
    data->type = type;

    return data;
}


void data_destroy(DATA *data){
    //If the data is null then there's no data to destroy
    if(data == NULL) return;

    if (data->id){
        free(data->id);
    }
    free(data);
}


DATA *data_copy(DATA *data){
    if (!data){
        fprintf(stderr, "Error copying the data. Null pointer.\n");
        return NULL;
    }

    return data_create(data->id, data->type);
}


int data_cmp(DATA *data1, DATA *data2){
    if (!data1 || !data2){
        fprintf(stderr, "Error comparing data. Null pointer.\n");
        return 1;
    }
    return strcmp(data1->id, data2->id);
}


int data_cmp_id(DATA *data1, char *id2){
    if (!data1 || !id2){
        fprintf(stderr, "Error comparing data. Null pointer.\n");
        return 1;
    }

    return strcmp(data1->id, id2);
}


void data_print(FILE *pf, DATA *data){
    if(!pf) return;
    fprintf(pf, "%s %d\n", data->id, data->type);   
}


unsigned long data_hash(DATA *data){
    return hash_str(data->id);
}

unsigned long hash_str(unsigned char *str){
    unsigned long hash = 0;
    int c;

    while (c = *str++){
        hash = c + (hash << 6) + (hash << 16) - hash;
    }

    return hash;
}

int data_get_type(DATA *data){
    if (!data) return 0;
    return data->type;
}