#include "../includes/io.h"
#include <string.h>

long file_len(FILE* pf){
    long len;

    if (!pf){
        fprintf(stderr, "Error longitud de archivo. Puntero inválido.\n");
        return -1;
    }
    if (fseek(pf, 0, SEEK_END)){ 
        fprintf(stderr, "Error longitud de archivo. Error al buscar final de archivo.\n");
        return -1;
    }

    len = ftell(pf);
    rewind(pf);
    return len;
}

size_t file_read(char *str, int size, FILE *file){
    if (!str || !file){
        fprintf(stderr, "Error leyendo archivo. Argumentos inválidos.\n");
        return 0;
    }

    size_t read = 0;

    if (file == stdin){
        fprintf(stdout, "Input: ");
        str = fgets(str, size + 1, file);
        if (!str) return 0;
        if (strlen(str) == 1 && str[0] == '\n') return 0;
        return strlen(str);
    }else{
        read = fread(str, 1, size, file);
        str[read] = '\0';
        return read;
    }
}

size_t file_write(char *str, FILE *file){
    if (!str || !file){
        fprintf(stderr, "Error escribiendo archivo. Argumentos inválidos.\n");
        return 0;
    }

    size_t written;

    written = fwrite(str, 1, strlen(str), file);

    if (file == stdout){
        fprintf(stdout, "\n");
    }

    return written;
}

bool load_matrix(FILE *pf, int **matrix, int m, int n){
    char *string = malloc(BUFFER_SIZE + 1);
    char *str1, *str2;
    char *saveptr1, *saveptr2;
    char *token, *subtoken;
    int i, j;

    if (file_read(string, BUFFER_SIZE, pf) == 0){
        fprintf(stdout, "Error. No se leyó nada del archivo de clave.\n");
        return false;
    }

    for (i = 0, str1 = string; ; i++, str1 = NULL) {
        token = strtok_r(str1, "\n", &saveptr1);
        if (token == NULL)
            break;

        for (j = 0, str2 = token; ; j++, str2 = NULL) {
            subtoken = strtok_r(str2, " ", &saveptr2);
            if (subtoken == NULL)
                break;
            matrix[i][j] = atoi(subtoken);
        }
    }

    free(string);
    return (i == m) && (j == n);
}

bool load_vector(FILE *pf, int *vector, int size){
    char *string = malloc(BUFFER_SIZE + 1);
    char *str1;
    char *token;
    int i;

    if (file_read(string, BUFFER_SIZE, pf) == 0){
        fprintf(stdout, "Error. No se leyó nada del archivo de permutación.\n");
        return false;
    }

    for (i = 0, str1 = string; ; i++, str1 = NULL) {
        token = strtok(str1, " ");
        if (token == NULL)
            break;
        vector[i] = atoi(token);
    }
        
    free(string);
    return i == size;
}
