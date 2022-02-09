#include "transforma.h"
#include <stdlib.h>
#include <string.h>

struct _TransformData {
    int ** f;           /*Tabla para la función de transición*/
    int ** contenido;   /*Array que asocia cada estado del AFD con que estados contiene del AFND
                            contenido[i][j] = 1 si el estado con índice i de AFD contiene al 
                                                estado con índice j de AFND*/
    int num_estados;
};

/*Inicializa la estructura intermedia*/
TransformData * TDNuevo(AFND * p_afnd); 

/*Libera la memoria reservada para la estructura intermedia*/
void TDElimina(TransformData * td); 

/*Calcula el estado inicial del autómata determinista*/
void TDEstadoInicial(TransformData * td, AFND * p_afnd);

/*Comprueba si el estado formado por los estados con casillas activadas en q_aux existe ya en la estructura intermedia*/
int TDIndiceEstado(TransformData * td, AFND * p_afnd, int * q_aux);

/*Crea un nuevo estado formado por los estados indicados en q_aux*/
int TDCrearEstado(TransformData * td, AFND * p_afnd, int * q_aux);

/*Imprime la estructura intermedia*/
void TDImprimir(FILE * pf, TransformData * td, AFND * p_afnd);

/*Genera el nombre del estado que ocupa la fila indice en la tabla contenido*/
char * generarNombre(AFND * p_afnd, TransformData * td, int indice);

/*Comprueba si el estado que ocupa la fila indice en la tabla contenido contiene algún estado que era final en el autómata original*/
int contieneEstadoFinal(AFND * p_afnd, TransformData * td, int indice);

AFND * AFNDTransforma(AFND * p_afnd){
    TransformData * td = NULL;
    AFND * p_afd = NULL;
    int q_actual, q_trans, sim, i, j, k;
    int * q_aux = NULL;
    int vacio;
    char * nombre = NULL;

    if (!p_afnd){
        fprintf(stdout, "Error. Automata nulo.\n");
        return NULL;
    }

    q_aux = (int*)malloc(AFNDNumEstados(p_afnd)*sizeof(int));
    if (!q_aux){
        fprintf(stdout, "Error creando array para estado auxiliar.\n");
        return NULL;
    }

    td = TDNuevo(p_afnd);
    if (!td){
        free(q_aux);
        fprintf(stdout, "Error creando la estructura intermedia.\n");
        return NULL;
    }

    /*1. Calcular estado inicial*/
    TDEstadoInicial(td, p_afnd);

    /*2. Comenzamos a rellenar la tabla de transiciones*/
    for (q_actual = 0; q_actual < td->num_estados; q_actual++){
        /*Calculamos la transición para cada símbolo del alfabeto de entrada*/
        for (sim = 0; sim < AFNDNumSimbolos(p_afnd); sim++){
            /*Inicializamos el estado auxiliar que almacena las transiciones hechas*/
            for (k = 0; k < AFNDNumEstados(p_afnd); k++){ q_aux[k] = 0;}

            /*Calculamos las transiciones asociadas a cada estado que se incluye en el estado actual*/
            for (i = 0; i < AFNDNumEstados(p_afnd); i++){
                if (td->contenido[q_actual][i] == 1){
                    /*Si el estado i pertenece al estado actual, calculamos las transiciones con el símbolo sim*/
                    for (j = 0; j < AFNDNumEstados(p_afnd); j++){
                        if (AFNDTransicionIndicesEstadoiSimboloEstadof(p_afnd, i, sim, j) == 1) { q_aux[j] = 1;}
                    }
                }
            }

            /*Calcular las transiciones lambda posibles desde los estados a los que se transita*/
            for (i = 0; i < AFNDNumEstados(p_afnd); i++){
                if (q_aux[i] == 1){
                    /*Si el estado i pertenece al estado actual, calculamos las transiciones con el símbolo sim*/
                    for (j = 0; j < AFNDNumEstados(p_afnd); j++){
                        if (AFNDCierreLTransicionIJ(p_afnd, i, j) == 1) { q_aux[j] = 1;}
                    }
                }
            }

            vacio = 1;
            /*Comprobar que se realiza transición (que no es el conjunto vacío)*/
            for (i = 0; i < AFNDNumEstados(p_afnd); i++){
                if (q_aux[i] == 1){ vacio = 0;}
            }

            if (!vacio){
                /*Comprobar si el estado existe o debe ser creado*/
                q_trans = TDIndiceEstado(td, p_afnd, q_aux);
                if (q_trans == -1){
                    /*El estado no existe todavía*/
                    td->f[q_actual][sim] = td->num_estados;
                    if(TDCrearEstado(td, p_afnd, q_aux)){
                        free(q_aux);
                        TDElimina(td);
                        fprintf(stdout, "Error creando nuevo estado.\n");
                        return NULL;
                    }
                }
                else{
                    /*El estado ya existe en la estructura intermedia*/
                    td->f[q_actual][sim] = q_trans;
                }
            }
            
        }
    }


    /* Crear el AFD a partir de la información creada con el algoritmo */
    p_afd = AFNDNuevo("determinista", td->num_estados, AFNDNumSimbolos(p_afnd));

    /* Insertar los símbolos en el autómata */
    for (i = 0; i < AFNDNumSimbolos(p_afnd); i++){
        p_afd = AFNDInsertaSimbolo(p_afd, AFNDSimboloEn(p_afnd, i));
    }

    /* Insertar los estados generados en el autómata */
    /* Insertar estado inicial */
    nombre = generarNombre(p_afnd, td, 0);
    if (!nombre){
        fprintf(stdout, "Error creando nombre para estado %d", 0);
        free(q_aux);
        TDElimina(td);
        return NULL;
    }
    if (contieneEstadoFinal(p_afnd, td, 0)){
        p_afd = AFNDInsertaEstado(p_afd, nombre, INICIAL_Y_FINAL);
    }
    else{
        p_afd = AFNDInsertaEstado(p_afd, nombre, INICIAL);
    }
    free(nombre);
    /* Insertar el resto de estados */
    for (i = 1; i < td->num_estados; i++){
        nombre = generarNombre(p_afnd, td, i);
        if (!nombre){
            fprintf(stdout, "Error creando nombre para estado %d", i);
            free(q_aux);
            TDElimina(td);
            return NULL;
        }
        if (contieneEstadoFinal(p_afnd, td, i)){
            p_afd = AFNDInsertaEstado(p_afd, nombre, FINAL);
        }
        else{
            p_afd = AFNDInsertaEstado(p_afd, nombre, NORMAL);
        }
        free(nombre);
    }

    /* Insertar las transiciones */
    for (i = 0; i < td->num_estados; i++){
        for (j = 0; j < AFNDNumSimbolos(p_afd); j++){
            if (td->f[i][j] != -1){
                p_afd = AFNDInsertaTransicion(p_afd, AFNDNombreEstadoEn(p_afd, i), AFNDSimboloEn(p_afd, j), AFNDNombreEstadoEn(p_afd, td->f[i][j]));
            }
        }
    }

    /*p_afd = AFNDCierraLTransicion(p_afd);*/
    free(q_aux);
    TDElimina(td);
    return p_afd;
}


TransformData * TDNuevo(AFND * p_afnd){
    TransformData * td = NULL;
    int i;
    /*Se reserva memoria para la estructura*/
    td = (TransformData *)malloc(sizeof(TransformData));
    if (!td){
        fprintf(stdout, "Error creando TransformData.\n");
        return NULL;
    }
    /*El número de estados inicialmente es 1 (estado inicial)*/
    td->num_estados = 1;

    /*Se reserva memoria para la tabla de la función de transición (por ahora solo tendrá una fila)*/
    td->f = (int**)malloc(1*sizeof(int*));
    if (!(td->f)){
        TDElimina(td);
        fprintf(stdout, "Error creando f.\n");
        return NULL;
    }
    /*Se reserva memoria para la primera fila de la tabla f*/
    td->f[0] = (int*)malloc(AFNDNumSimbolos(p_afnd)*sizeof(int));
    if (!(td->f[0])){
        TDElimina(td);
        fprintf(stdout, "Error creando f[0].\n");
        return NULL;
    }
    /*Se inicializan las transiciones a -1 (ningún estado)*/
    for (i = 0; i < AFNDNumSimbolos(p_afnd); i++){
        td->f[0][i] = -1;
    }

    /*Se reserva memoria para la tabla contenido (por ahora solo tendrá una fila)*/
    td->contenido = (int**)malloc(1*sizeof(int*));
    if (!(td->contenido)){
        TDElimina(td);
        fprintf(stdout, "Error creando contenido.\n");
        return NULL;
    }
    /*Se reserva memoria para la primera fila de la tabla contenido*/
    td->contenido[0] = (int*)malloc(AFNDNumEstados(p_afnd)*sizeof(int));
    if (!(td->contenido[0])){
        TDElimina(td);
        fprintf(stdout, "Error creando contenido[0].\n");
        return NULL;
    }
    /*Se inicializan a 0 las posiciones (el estado inicial no está formado por ninguno por ahora)*/
    for (i = 0; i < AFNDNumEstados(p_afnd); i++){
        td->contenido[0][i] = 0;
    }

    return td;
}


void TDElimina(TransformData * td){
    int i;
    if (td) { 
        if (td->f){
            for (i = 0; i < td->num_estados; i++){
                if (td->f[i]) {free(td->f[i]);}
            }
            free(td->f);
        }
        if (td->contenido){
            for (i = 0; i < td->num_estados; i++){
                if (td->contenido[i]) {free(td->contenido[i]);}
            }
            free(td->contenido);
        }
        free(td);
    }
}


int TDIndiceEstado(TransformData * td, AFND * p_afnd, int * q_aux){
    int i, j; 
    int counter;

    for (i = 0; i < td->num_estados; i++){
        counter = 0;
        for (j = 0; j < AFNDNumEstados(p_afnd); j++){
            if (td->contenido[i][j] == q_aux[j]){
                counter++;
            }
            else{
                break;
            }
        }
        /*Si están formados por exactamente los mismos estados devolvemos el índice*/
        if (counter == AFNDNumEstados(p_afnd)){
            return i;
        }
    }
    /*Si el estado no existe todavía devolvemos -1*/
    return -1;
}


void TDEstadoInicial(TransformData * td, AFND * p_afnd){
    int i;
    int estado_inicial;
    /*Marcar el estado inicial original*/
    estado_inicial = AFNDIndiceEstadoInicial(p_afnd);
    td->contenido[0][estado_inicial] = 1;

    /*Calcular el cierre*/
    for (i = 0; i < AFNDNumEstados(p_afnd); i++){
        if (AFNDCierreLTransicionIJ(p_afnd, estado_inicial, i) == 1){
            td->contenido[0][i] = 1;
        }
    }
}


int TDCrearEstado(TransformData * td, AFND * p_afnd, int * q_aux){
    int i;

    (td->num_estados)++;
    td->f = (int **)realloc(td->f, (td->num_estados)*sizeof(int*));
    if (!(td->f)){ return 1;}

    td->f[td->num_estados-1] = (int*)malloc(AFNDNumSimbolos(p_afnd)*sizeof(int));
    if (!(td->f[td->num_estados-1])){ return 2;}
    for (i = 0; i < AFNDNumSimbolos(p_afnd); i++){
        td->f[td->num_estados-1][i] = -1;
    }

    td->contenido = (int **)realloc(td->contenido, (td->num_estados)*sizeof(int*));
    if (!(td->contenido)){ return 3;}
    td->contenido[td->num_estados-1] = (int*)malloc(AFNDNumEstados(p_afnd)*sizeof(int));
    if (!(td->contenido[td->num_estados-1])){ return 4;}
    for (i = 0; i < AFNDNumEstados(p_afnd); i++){
        td->contenido[td->num_estados-1][i] = q_aux[i];
    }

    return 0;
}


void TDImprimir(FILE * pf, TransformData * td, AFND * p_afnd){
    int i, j;
    fprintf(pf, "NÚMERO DE ESTADOS: %d\n", td->num_estados);
    fprintf(pf, "TABLA DE TRANSICIONES:\n");
    for (i = 0; i < td->num_estados; i++){
        for (j = 0; j < AFNDNumSimbolos(p_afnd); j++){
            fprintf(pf, "%d\t", td->f[i][j]);
        }
        fprintf(pf, "\n");
    }

    fprintf(pf, "\nTABLA DE CONTENIDO:\n");
    for (i = 0; i < td->num_estados; i++){
        for (j = 0; j < AFNDNumEstados(p_afnd); j++){
            fprintf(pf, "%d\t", td->contenido[i][j]);
        }
        fprintf(pf, "\n");
    }
}


char * generarNombre(AFND * p_afnd, TransformData * td, int indice){
    char * nombre = NULL;
    int j;

    for (j = 0; j < AFNDNumEstados(p_afnd); j++){
        if (td->contenido[indice][j]){
            if (!nombre){
                nombre = (char *)malloc(strlen(AFNDNombreEstadoEn(p_afnd, j)) + 1);
                if (!nombre){
                    return NULL;
                }
                strcpy(nombre, AFNDNombreEstadoEn(p_afnd, j));
            }
            else{
                nombre = (char *)realloc(nombre, strlen(nombre) + strlen(AFNDNombreEstadoEn(p_afnd, j)) + 1);
                if (!nombre){
                    return NULL;
                }
                strcat(nombre, AFNDNombreEstadoEn(p_afnd, j));
            }
        }
    }

    return nombre;
}


int contieneEstadoFinal(AFND * p_afnd, TransformData * td, int indice){
    int j;
    for (j = 0; j < AFNDNumEstados(p_afnd); j++){
        if (td->contenido[indice][j] && (AFNDTipoEstadoEn(p_afnd, j) == FINAL || AFNDTipoEstadoEn(p_afnd, j) == INICIAL_Y_FINAL)){
            return 1;
        }
    }
    return 0;
}
