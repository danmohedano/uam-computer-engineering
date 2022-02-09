#include "../includes/utils.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int euclides_extended(mpz_t m, mpz_t a, mpz_t inverse_a){
    /* Aplicando el teorema de Bezout como:
        ri = m x ui + a x vi
    */
    mpz_t old_r, r, old_u, u, old_v, v, qi, temp;
    int gcd1 = 0;

    mpz_init_set(old_r, m); mpz_init_set(r, a);
    mpz_init_set_ui(old_u, 1); mpz_init_set_ui(u, 0);
    mpz_init_set_ui(old_v, 0); mpz_init_set_ui(v, 1);
    mpz_init(qi);
    mpz_init(temp);

    // Bucle para calcular qi y actualizar los valores
    while(mpz_cmp_ui(r, 0)){
        // Cálculo de qi
        mpz_tdiv_q(qi, old_r, r);

        // Actualizar r(i+1) = r(i-1) - q(i)r(i)
        mpz_set(temp, r);
        mpz_mul(r, qi, r);
        mpz_sub(r, old_r, r);
        mpz_set(old_r, temp);

        // Actualizar u(i+1) = u(i-1) - q(i)u(i)
        mpz_set(temp, u);
        mpz_mul(u, qi, u);
        mpz_sub(u, old_u, u);
        mpz_set(old_u, temp);

        // Actualizar v(i+1) = v(i-1) - q(i)v(i)
        mpz_set(temp, v);
        mpz_mul(v, qi, v);
        mpz_sub(v, old_v, v);
        mpz_set(old_v, temp);
    }

    // Guardar el inverso de a
    if (mpz_cmp_ui(old_v, 0) < 0) mpz_add(old_v, old_v, m);
    mpz_set(inverse_a, old_v);

    if (mpz_cmp_ui(old_r, 1) == 0) gcd1 = 1;

    mpz_clear(old_r); mpz_clear(r);
    mpz_clear(old_u); mpz_clear(u);
    mpz_clear(old_v); mpz_clear(v);
    mpz_clear(qi); mpz_clear(temp);

    return gcd1;
}

int* matrix_modular_mul(int *x, int **k, int n, int m){
    int *result = NULL;

    if (!x || !k || n <= 0 || m <= 0){
        fprintf(stderr, "Error. Argumentos de multiplicación de matriz incorrectos.\n");
        return NULL;
    }

    // Reserva e inicialización del resultado
    result = (int*)malloc(n * sizeof(int));
    if (!result){
        fprintf(stderr, "Error reservando memoria para multiplicación de matrices.\n");
        return NULL;
    }

    for (int i = 0; i < n; ++i){
        result[i] = 0;
    }

    // Multiplicación de las matrices en aritmética modular
    for (int i = 0; i < n; ++i){
        for (int j = 0; j < n; ++j){
            result[i] += ((x[j] * k[j][i]) % m);
        }
    }

    for (int i = 0; i < n; ++i){
        for (int j = 0; j < n; ++j){
            result[i] = (result[i] % m);
            if (result[i] < 0) result += m;
        }
    }

    return result;
}

int matrix_modular_det(int **k, int n, int m){
    int **minor;
    int determinant = 0;

    if (!k || n < 1 || m < 1){
        fprintf(stderr, "Error. Argumentos de multiplicación de matriz inválidos.\n");
        return -1;
    }
    if (n == 1){
        determinant = k[0][0];
    }else if (n == 2){
        determinant = ((k[0][0]*k[1][1]) - (k[0][1]*k[1][0]));
    }else{
        // Inicializar matriz auxiliar
        minor = allocate_matrix(n-1, n-1);
        if (!minor){
            fprintf(stderr, "Error. Error reservando memoria para determinante.\n");
            return -1;
        }

        // Iteramos por la primera fila
        for (int j = 0; j < n; ++j){
            // Copiamos en la matriz auxiliar la menor
            minor_matrix(k, minor, n, 0, j);

            determinant += ((j % 2 ? -1 : 1))*((k[0][j]*matrix_modular_det(minor, n-1, m)) % m);
        }

        free_matrix(minor, n-1);
    }

    determinant = determinant % m;

    if (determinant < 0) determinant += m;

    return determinant;
}

int** matrix_modular_inv(int **k, int n, int m){
    int determinant, inv_determinant, temp;
    int **inv_matrix = NULL;
    int **minor = NULL;
    mpz_t aux_m, aux_det, aux_inv_det;

    if (!k || n < 1 || m < 1){
        fprintf(stderr, "Error. Argumentos de inversión de matriz incorrectos.\n");
        return NULL;
    }

    // Realizar comprobaciones necesarias: det(k) != 0 && mcd(m, det(k)) == 1
    determinant = matrix_modular_det(k, n, m);

    if (determinant == 0){
        fprintf(stderr, "Error en inversión. Determinante == 0.\n");
        return NULL;
    }

    mpz_init_set_ui(aux_m, m);
    mpz_init_set_ui(aux_det, determinant);
    mpz_init(aux_inv_det);

    if (euclides_extended(aux_m, aux_det, aux_inv_det) == 0){
        mpz_clear(aux_m); mpz_clear(aux_det); mpz_clear(aux_inv_det);
        fprintf(stderr, "Error en inversión. No existe inverso multiplicativo del determinante.\n");
        return NULL;
    }

    inv_determinant = mpz_get_ui(aux_inv_det);

    mpz_clear(aux_m); mpz_clear(aux_det); mpz_clear(aux_inv_det);

    // Si se ha comprobado todo, se procede a calcular la matriz adjunta
    inv_matrix = allocate_matrix(n, n);
    minor = allocate_matrix(n-1, n-1);
    if (!inv_matrix || !minor){
        free_matrix(inv_matrix, n);
        free_matrix(minor, n-1);
        fprintf(stderr, "Error en inversión. Error reservando memoria.\n");
        return NULL;
    }

    // Para calcular la matriz adjunta, primero se calcula la matriz de cofactores
    for (int i = 0; i < n; ++i){
        for (int j = 0; j < n; ++j){
            // Se copia la menor en la matrix auxiliar
            minor_matrix(k, minor, n, i, j);

            inv_matrix[i][j] = (((i+j) % 2) ? -1 : 1)*(matrix_modular_det(minor, n-1, m));
        }
    }

    // Una vez calculada la matriz de cofactores, se calcula la matriz traspuesta de esta (la adjunta)
    for (int i = 0; i < n; ++i){
        for (int j = 0; j < i; ++j){
            temp = inv_matrix[i][j];
            inv_matrix[i][j] = inv_matrix[j][i];
            inv_matrix[j][i] = temp;
        }
    }

    // La matriz adjunta se multiplica por el inverso multiplicativo del determinante
    for (int i = 0; i < n; ++i){
        for (int j = 0; j < n; ++j){
            inv_matrix[i][j] = (inv_matrix[i][j]*inv_determinant) % m;
            if (inv_matrix[i][j] < 0) inv_matrix[i][j] += m;
        }
    }

    free_matrix(minor, n-1);

    return inv_matrix;
}

void minor_matrix(int **x, int **m, int n, int i, int j){
    int aux_i, aux_j;

    if (!x || !m || n < 1 || i < 0 || i >= n || j < 0 || j >= n){
        fprintf(stderr, "Error. Argumentos de matriz menor incorrectos\n");
        return;
    }

    for (int mi = 0; mi < n; ++mi){
        for (int mj = 0; mj < n; ++mj){
            if (mi != i && mj != j){
                aux_i = (mi < i) ? mi : mi-1;
                aux_j = (mj < j) ? mj : mj-1;
                m[aux_i][aux_j] = x[mi][mj];
            }
        }
    }
}

int **allocate_matrix(int m, int n){
    int **matrix = NULL;

    matrix = (int**)malloc(m*sizeof(int*));
    if (!matrix) return NULL;

    for (int i = 0; i < m; ++i){
        matrix[i] = (int*)malloc(n*sizeof(int));
        if (!(matrix[i])){
            free_matrix(matrix, m);
            return NULL;
        }
    }

    return matrix;
}

void free_matrix(int **matrix, int m){
    if (matrix){
        for (int i = 0; i < m; ++i) if (matrix[i]) free(matrix[i]);
        free(matrix);
    }
}

int** matrix_swap_rows(int **x, int *k, int m, int n){
    int **matrix = NULL;

    if(!x || !k || n < 1 || m < 1){
        fprintf(stderr, "Error al permutar filas. Argumentos no válidos.\n");
        return NULL;
    }
    
    matrix = allocate_matrix(m, n);
    
    if(!matrix){
        fprintf(stderr, "Error al permutar filas. Error alocando memoria.\n");
        return NULL;
    }

    // Se permuta cada fila a su posición nueva
    for (int i = 0; i < m; ++i){
        for (int j = 0; j < n; ++j){
            matrix[k[i]][j] = x[i][j];
        }
    }

    return matrix;
}

int** matrix_swap_columns(int **x, int *k, int m, int n){
    int **matrix = NULL;

    if(!x || !k || n < 1 || m < 1){
        fprintf(stderr, "Error al permutar columnas. Argumentos no válidos.\n");
        return NULL;
    }
    
    matrix = allocate_matrix(m, n);
    
    if(!matrix){
        fprintf(stderr, "Error al permutar columnas. Error alocando memoria.\n");
        return NULL;
    }

    // Se permuta cada columna a su posición nueva
    for (int j = 0; j < n; ++j){
        for (int i = 0; i < m; ++i){
            matrix[i][k[j]] = x[i][j];
        }
    }

    return matrix;
}

void matrix_print(FILE* pf, int **matrix, int m, int n){
    for (int i = 0; i < m; ++i){
        for (int j = 0; j < n; ++j){
            fprintf(pf, "%d\t", matrix[i][j]);
        }
        fprintf(pf, "\n");
    }
}

uint64_t key_generator(uint64_t state){
    uint64_t bit;

    for (int i = 0; i < 64; ++i){
        bit = ((state >> 0) ^ (state >> 1) ^ (state >> 3) ^ (state >> 4)) & 1u;
        state = (state >> 1) | (bit << 63);
    }
    return state;
}

void string_transform(char *string){
    long len = strlen(string);
    long correct_chars = 0;
    
    for (long i = 0; i < len; ++i){
        if ('a' <= string[i] && string[i] <= 'z') string[i] += 'A' - 'a';
        if ('A' <= string[i] && string[i] <= 'Z'){
            string[correct_chars++] = string[i];
        }
    }
    string[correct_chars] = '\0';
}