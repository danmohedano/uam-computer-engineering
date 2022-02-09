#include <stdio.h>
#include <stdlib.h>
#include "symbol_table.h"


int main(int argc, char **argv){
    /*
    char str1[]="uno", str2[]="dos", str3[]="funcion1", str4[]="uno", str5[]="funcion1", str6[]="tres", str7[]="uno";
    DATA *e1, *e2, *e3, *e4, *e5, *e6, *e7;
    e1 = data_create(str1, 1);
    */
    FILE *f1, *f2;
    char *line = NULL;
    size_t len = 0;
    ssize_t read;
    int n;

    int type, res;
    char id[101];
    DATA *search_res, *d;

    if (argc < 3){
        fprintf(stderr, "Usage: ./prueba_tabla <input_file> <output_file>\n");
        return -1;
    }
    symbol_table *table = symbol_create();
    
    f1 = fopen(argv[1], "r");
    if (f1 == NULL) {
        printf("Couldnt find input file\n");
        return -1;
    }
    f2 = fopen(argv[2], "w");
    if (f2 == NULL) {
        printf("Couldnt fopen output file\n");
        return -1;
    }

    while ((read = getline(&line, &len, f1)) != -1) {
        n = sscanf(line, "%s %d", id, &type);
        if (n==1){
            // fprintf(stdout, "Searching for %s\n", id);
            search_res = symbol_search(table, id);
            if (search_res == NULL) {
                fprintf(f2, "%s -1\n", id);
            } else {
                data_print(f2, search_res);
            }
        } else if (n==2){
            // fprintf(stdout, "Inserting %s %d\n", id, type);
            d = data_create(id, type);
            res = symbol_insert(table, d);
            if (res == 0) fprintf(f2, "%s\n", id);
            else fprintf(f2, "-1 %s\n", id);
        } else {
            // printf("\tError: Invalid line.\n");
        }
    }
    
    // free resources
    free(line);
    symbol_destroy(table);
    fclose(f1);
    fclose(f2);

    return 0;
}
