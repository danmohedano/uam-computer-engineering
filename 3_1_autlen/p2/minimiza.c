#include "minimiza.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct _Tabla_Equivalencia{
    int *claseold;
    int *clasenew;
    int nclases;
    int nestados;
}Tabla_Equivalencia;

/**
 * Función: simplificar
 * ------------------
 * Simplifica un autómata eliminando los estados inaccesibles
 * 
 * p_afnd: puntero al autómata original
 * 
 * returns: nuevo autómata simplificado
 */
AFND *simplificar(AFND *p_afnd);

/**
 * Función: contiene
 * ------------------
 * Comprueba si un array de longitud n contiene un elemento a
 * 
 * x: array
 * n: longitud de x
 * a: elemento que se busca
 * 
 * returns: 1 si lo contiene, 0 si no
 */
int contiene(int *x, int n, int a);

/**
 * Función: construir
 * ------------------
 * A partir de las clases de equivalencia calculadas se construye el nuevo autómata minimizado
 * 
 * p_afnd: puntero al autómata simplificado
 * teq: puntero a la tabla de equivalencia
 * 
 * returns: el autómata construido
 */
AFND *construir(AFND* p_afnd, Tabla_Equivalencia *teq);

/**
 * Función: generarNombre
 * ------------------
 * Genera el nombre de una clase de equivalencia concatenando los nombres de los estados que la forman
 * 
 * p_afnd: puntero al autómata simplificado
 * teq: puntero a la tabla de equivalencia
 * clase: índice de la clase de equivalencia de la que se quiere obtener el nombre
 * 
 * returns: el nombre (se debe liberar la memoria después de usarlo)
 */
char * generarNombre(AFND * p_afnd, Tabla_Equivalencia *teq, int clase);

/**
 * Función: EQNuevo()
 * ------------------
 * Crea la estructura intermedia para implementar el algoritmo de minimización
 * 
 * nestados: numero de estados
 * 
 * returns: La tabla de equivalencia
 */
Tabla_Equivalencia *EQNuevo(int nestados);

/**
 * Función: EQElimina()
 * ------------------
 * Libera memoria reservada para la estructura intermedia
 * 
 * t: libera la estructura
 */
void EQElimina(Tabla_Equivalencia *t);

/**
 * Función: EQImprimir()
 * ------------------
 * Imprime la tabla de equivalencia
 * 
 * t: pointer a la tabla de equivalencia
 * pf: pointer al fichero
 */
void EQImprimir(FILE* pf, Tabla_Equivalencia *t);

/**
 * Función: EQNuevoPaso()
 * ------------------
 * Actualiza la estructura intermedia pasando la tabla actual a la antigua y reseteando la actual.
 * 
 * t: pointer a la tabla de equivalencia
 */
void EQNuevoPaso(Tabla_Equivalencia *t);

/**
 * Función: EQCambios()
 * ------------------
 * Comprueba si ha habido cambios en las clases en la última iteración del algoritmo.
 * 
 * t: pointer a la tabla de equivalencia
 * 
 * returns: 1 si ha habido cambios, 0 si no los ha habido
 */
int EQCambios(Tabla_Equivalencia *t);

/**
 * Función: EQIteracion
 * ------------------
 * Ejecuta una iteración del algoritmo de estados equivalentes.
 * 
 * t: pointer a la tabla de equivalencia
 * p_afnd: pointer al AFD del que se parte
 * 
 * returns: 0 si todo va bien, cualquier otra cosa en caso de error
 */
int EQIteracion(Tabla_Equivalencia *t, AFND *p_afnd);

/**
 * Función: EQRepresentante
 * ------------------
 * Busca el representante de una clase de equivalencia (el primer estado que pertenece
 * a esa clase)
 * 
 * t: pointer a la tabla de equivalencia
 * clase: la clase de la que se busca el representante
 * 
 * returns: índice del estado representante
 */
int EQRepresentante(Tabla_Equivalencia *t, int clase);

/**
 * Función: EQEquivalentes
 * ------------------
 * Comprueba si dos estados son equivalentes 
 * 
 * t: pointer a la tabla de equivalencia
 * p_afnd: pointer al AFD del que se parte
 * e1: estado 1
 * e2: estado 2
 * 
 * returns: 1 si son equivalentes, 0 si no lo son
 */
int EQEquivalentes(Tabla_Equivalencia *t, AFND *p_afnd, int e1, int e2);

/**
 * Función: EQTransicion
 * ------------------
 * Busca al estado al que se transiciona desde un estado dado y leyendo un símbolo dado 
 * 
 * p_afnd: pointer al AFD del que se parte
 * estado: estado del que se parte
 * simbolo: símbolo que se lee
 * 
 * returns: el estado al que se transiciona desde 'estado' leyendo 'simbolo'
 */
int EQTransicion(AFND *p_afnd, int estado, int simbolo);

/**
 * Función: EQTipoClase
 * ------------------
 * Calcula que tipo de estado es una clase de equivalencia 
 * 
 * p_afnd: pointer al AFD del que se parte
 * teq: pointer a la tabla de equivalencia
 * clase: indice de la clase de equivalencia
 * 
 * returns: el tipo del estado
 */
int EQTipoClase(AFND *p_afnd, Tabla_Equivalencia *teq, int clase);
/*-----------------------------------------------------------------------------------*/

AFND *AFNDMinimiza(AFND *p_afnd){
    int i, cambios = 1;
    Tabla_Equivalencia *teq = NULL;
    AFND * p_simp = NULL, *min = NULL;
    if (!p_afnd){
        fprintf(stderr, "No se pudo minimizar el autómata. Puntero inválido.\n");
        return NULL;
    }
    /* ----Simplificar---- */
    p_simp = simplificar(p_afnd);

    if (!p_simp) return NULL;

    /* ----Estados equivalentes---- */
    /* Inicializar la tabla de equivalencia con los estados finales y no finales*/
    teq = EQNuevo(AFNDNumEstados(p_simp));
    if (!teq) return NULL;
    for (i = 0; i < teq->nestados; i++){
        if (AFNDTipoEstadoEn(p_simp, i) == FINAL || AFNDTipoEstadoEn(p_simp, i) == INICIAL_Y_FINAL){
            /* Clase 1 <=> Estados Finales */
            teq->claseold[i] = 1;
        }
        else{ /* Clase 0 <=> Estados no finales */
            teq->claseold[i] = 0;
        }
    }
    teq->nclases = 2;

    /* Mientras haya cambios en cada iteración, se sigue ejecutando el algoritmo */
    while (cambios){
        if (EQIteracion(teq, p_simp)){
            EQElimina(teq);
            return NULL;
        }
        cambios = EQCambios(teq);
        EQNuevoPaso(teq);
    }

    /*-----Construir el nuevo autómata a partir de las clases de equivalencia calculadas------*/
    min = construir(p_simp, teq);


    EQElimina(teq);
    AFNDElimina(p_simp);
    return min;
}

/*----------------- SIMPLIFICAR ---------------------------*/
AFND *simplificar(AFND *p_afnd){
    int *estados_accesibles = NULL;
    int n_estados, n_accesibles = 0, i, s, transicion;
    AFND * simp = NULL;

    if (!p_afnd){
            fprintf(stderr, "No se pudo simplificar el autómata. Puntero inválido.\n");
        return NULL;
    }

    n_estados = AFNDNumEstados(p_afnd);
    estados_accesibles=(int*)malloc(n_estados*sizeof(int));
    if (!estados_accesibles) return NULL;

    for (i = 0; i < n_estados; i++) estados_accesibles[i] = -1;

    /* Se marca el estado inicial como accesible */
    estados_accesibles[n_accesibles++] = AFNDIndiceEstadoInicial(p_afnd); 

    /* Se siguen buscando estados accesibles */
    for (i = 0; i < n_accesibles; i++){
        for (s = 0; s < AFNDNumSimbolos(p_afnd); s++){
            /* Obtenemos a que estado transiciona con cada simbolo */
            transicion = EQTransicion(p_afnd, estados_accesibles[i], s);
            /* Si no está marcado como accesible, se marca*/
            if (!contiene(estados_accesibles, n_accesibles, transicion)){
                estados_accesibles[n_accesibles++] = transicion;
            }
        }
    }

    /* Se construye el nuevo autómata solo con los estados accesibles */
    simp = AFNDNuevo("simp", n_accesibles, AFNDNumSimbolos(p_afnd));
    if (!simp) return NULL;
    /* Se insertan los símbolos */
    for (s = 0; s < AFNDNumSimbolos(p_afnd); s++){
        AFNDInsertaSimbolo(simp, AFNDSimboloEn(p_afnd, s));
    }

    /* Se insertan los estados accesibles */
    for (i = 0; i < n_accesibles; i++){
        AFNDInsertaEstado(simp, AFNDNombreEstadoEn(p_afnd, estados_accesibles[i]), AFNDTipoEstadoEn(p_afnd, estados_accesibles[i]));
    }

    /* Se insertan las transiciones */
    for (i = 0; i < n_accesibles; i++){
        for (s = 0; s < AFNDNumSimbolos(p_afnd); s++){
            AFNDInsertaTransicion(simp, AFNDNombreEstadoEn(p_afnd, estados_accesibles[i]), AFNDSimboloEn(p_afnd, s), AFNDNombreEstadoEn(p_afnd, EQTransicion(p_afnd, estados_accesibles[i], s)));
        }
    }

    free(estados_accesibles);
    return simp;
}

int contiene(int *x, int n, int a){
    int i;
    for (i = 0; i < n; i++){
        if (x[i] == a) return 1;
    }
    return 0;
}


AFND *construir(AFND* p_afnd, Tabla_Equivalencia *teq){
    AFND *min = NULL;
    int s, i;
    int tipo, final;
    char *nombre = NULL;

    if (!p_afnd || !teq) return NULL;

    min = AFNDNuevo("min", teq->nclases, AFNDNumSimbolos(p_afnd));
    if (!min) return NULL;

    /* Se insertan los símbolos */
    for (s = 0; s < AFNDNumSimbolos(p_afnd); s++) AFNDInsertaSimbolo(min, AFNDSimboloEn(p_afnd, s));

    /* Se insertan los estados (las clases de equivalencia) */
    for (i = 0; i < teq->nclases; i++){
        nombre = generarNombre(p_afnd, teq, i);
        tipo = EQTipoClase(p_afnd, teq, i);
        AFNDInsertaEstado(min, nombre, tipo);
        free(nombre);
    }

    /* Se insertan las transiciones */
    for (i = 0; i < teq->nclases; i++){
        for (s = 0; s < AFNDNumSimbolos(p_afnd); s++){
            /* Se busca la clase a la que pertenece el estado al que se transiciona desde el representante de la clase i */
            final = teq->claseold[EQTransicion(p_afnd, EQRepresentante(teq, i), s)];
            AFNDInsertaTransicion(min, AFNDNombreEstadoEn(min, i), AFNDSimboloEn(min, s), AFNDNombreEstadoEn(min, final));
        }
    }

    return min;
}

char * generarNombre(AFND * p_afnd, Tabla_Equivalencia *teq, int clase){
    char * nombre = NULL;
    int j, rep;

    /* Se crea el nombre original con el nombre del representante de la clase */
    rep = EQRepresentante(teq, clase);
    nombre = (char *)malloc(strlen(AFNDNombreEstadoEn(p_afnd, rep)) + 1);
    if (!nombre){
        return NULL;
    }
    strcpy(nombre, AFNDNombreEstadoEn(p_afnd, rep));

    for (j = rep+1; j < teq->nestados; j++){
        /* Se comprueban el resto de estados y aquellos que pertenezcan a la clase de equivalencia se añaden al nombre */
        if (teq->claseold[j] == clase){
            nombre = (char *)realloc(nombre, strlen(nombre) + strlen(AFNDNombreEstadoEn(p_afnd, j)) + 1);
            if (!nombre){
                return NULL;
            }
            strcat(nombre, AFNDNombreEstadoEn(p_afnd, j));
        }
    }

    return nombre;
}

/*----------------- MANEJO DE LA ESTRUCTURA INTERMEDIA ---------------------------*/
Tabla_Equivalencia *EQNuevo(int nestados){
    int i;
    Tabla_Equivalencia *t = NULL;
    if (nestados < 1){
        fprintf(stderr, "Error creando estructura intermedia. Tamaño no válido.\n");
        return NULL;
    }
    
    /* Reservar memoria para la estructura */
    t = (Tabla_Equivalencia*)malloc(sizeof(Tabla_Equivalencia));
    if (!t){
        fprintf(stderr, "Error creando estructura intermedia. No se pudo reservar memoria.\n");
        return NULL;
    }

    /* Reservar memoria para los dos arrays */
    t->claseold = (int*)malloc(nestados*sizeof(int));
    if(!(t->claseold)) {
        fprintf(stderr, "Error creando estructura intermedia. No se pudo reservar memoria auxiliar.\n");
        EQElimina(t);
        return NULL;
    }

    t->clasenew = (int*)malloc(nestados*sizeof(int));
    if(!(t->clasenew)){
        fprintf(stderr, "Error creando estructura intermedia. No se pudo reservar memoria auxiliar.\n");
        EQElimina(t);
        return NULL;
    }

    /* Inicializar los valores de las tablas */
    for (i = 0; i < nestados; i++){
        t->claseold[i] = -1;
        t->clasenew[i] = -1;
    }

    /* Inicializar las variables auxiliares de la estructura intermedia */
    t->nclases = 0;
    t->nestados = nestados;

    return t;
}


void EQElimina(Tabla_Equivalencia *t){
    if(!t) return;
    if(t->claseold) free(t->claseold);
    if(t->clasenew) free(t->clasenew);
    free(t);
}


void EQImprimir(FILE* pf, Tabla_Equivalencia *t){
    int i;
    fprintf(pf, "#Clases: %d\n", t->nclases);
    fprintf(pf, "EQn:   ");
    for (i = 0; i < t->nestados; i++){
        fprintf(pf, "%d|", t->claseold[i]);
    }
    fprintf(pf, "\nEQn+1: ");
    for (i = 0; i < t->nestados; i++){
        fprintf(pf, "%d|", t->clasenew[i]);
    }
    fprintf(pf, "\n");
}


void EQNuevoPaso(Tabla_Equivalencia *t){
    int i;
    if (!t){
        fprintf(stderr, "Error creando nuevo paso. Puntero nulo.\n");
        return;
    }
    
    for(i = 0; i < t->nestados; i++){
        t->claseold[i] = t->clasenew[i];
        t->clasenew[i] = -1;
    }
}


int EQCambios(Tabla_Equivalencia *t){
    int i;
    if(!t){
        fprintf(stderr, "Cambio no posible. Puntero nulo. \n");
        return -1;
    }
    for(i = 0; i < t->nestados; i++){
        if(t->clasenew[i] != t->claseold[i]) return 1;
    }
    return 0;
}


int EQIteracion(Tabla_Equivalencia *t, AFND *p_afnd){
    int c, rep, i, counter = 0;
    if (!t || !p_afnd){
        fprintf(stderr, "Iteracion no posible. Puntero nulo.\n");
        return -1;
    }

    /* Buscar los estados que se mantienen en la misma clase de equivalencia */
    for (c = 0; c < t->nclases; c++){
        rep = EQRepresentante(t, c);
        if (rep == -1) return -1;

        /* El representante se mantiene en la misma clase */
        t->clasenew[rep] = c;
        counter++;

        /* Ir viendo cuales se mantienen en la clase del representante */
        for (i = rep+1; i < t->nestados; i++){
            if (t->claseold[i] == c){
                if (EQEquivalentes(t, p_afnd, rep, i)){
                    t->clasenew[i] = c;
                    counter++;
                } 
            }
        }
    }

    /* Generar nuevas clases de equivalencia para aquellos que no se han mantenido*/
    while (counter != t->nestados){
        /* Nueva clase de equivalencia */
        c = t->nclases;
        (t->nclases)++;

        /* Buscar el primer estado sin clase */
        for (i = 0; i < t->nestados; i++){
            if (t->clasenew[i] == -1){
                rep = i;
                t->clasenew[i] = c;
                counter++;
                break;
            }
        }

        if (counter == t->nestados) break;

        /* Buscar estados sin clase que pertenezcan a esta nueva clase de equivalencia */
        for (i = rep+1; i < t->nestados; i++){
            if (t->clasenew[i] == -1){
                if (EQEquivalentes(t, p_afnd, rep, i)){
                    t->clasenew[i] = c;
                    counter++;
                } 
            }
        }
    }
    return 0;
}


int EQRepresentante(Tabla_Equivalencia *t, int clase){
    int i;
    if (!t || clase < 0){
        fprintf(stderr, "Error buscando representante.\n");
        return -1;
    }

    /* Buscar el primer estado que pertenezca a la clase*/
    for (i = 0; i < t->nestados; i++){
        if (t->claseold[i] == clase) return i;
    }

    return -1;
}

int EQEquivalentes(Tabla_Equivalencia *t, AFND *p_afnd, int e1, int e2){
    int s;
    if (!t || !p_afnd || e1 < 0 || e2 < 0){
        fprintf(stderr, "Error comprobando equivalencia.\n");
        return -1;
    }

    /* Comprobamos que las transiciones con todos los simbolos llevan a estados de la misma clase*/
    for (s = 0; s < AFNDNumSimbolos(p_afnd); s++){
        if (t->claseold[EQTransicion(p_afnd, e1, s)] != t->claseold[EQTransicion(p_afnd, e2, s)]) return 0;
    }

    return 1;
}

int EQTransicion(AFND *p_afnd, int estado, int simbolo){
    int i;
    if (!p_afnd){
        fprintf(stderr, "Error buscando transición.\n");
        return -1;
    }
    /* Se busca el estado i al que se transiciona desde "estado" con el simbolo "simbolo" */
    for (i = 0; i < AFNDNumEstados(p_afnd); i++){
        if (AFNDTransicionIndicesEstadoiSimboloEstadof(p_afnd, estado, simbolo, i)) return i;
    }

    return -1;
}

int EQTipoClase(AFND *p_afnd, Tabla_Equivalencia *teq, int clase){
    int i, inicial = 0, final = 0;

    if (!p_afnd || !teq || clase < 0){
        return -1;
    }

    for (i = 0; i < teq->nestados; i++){
        /* Si pertenece el estado a la clase, se comprueba el tipo de estado que es */
        if (teq->claseold[i] == clase){
            if (AFNDTipoEstadoEn(p_afnd, i) == INICIAL) inicial = 1;
            else if (AFNDTipoEstadoEn(p_afnd, i) == FINAL) final = 1;
            else if (AFNDTipoEstadoEn(p_afnd, i) == INICIAL_Y_FINAL){
                inicial = 1;
                final = 1;
            }
        }
    }

    if (inicial && final) return INICIAL_Y_FINAL;
    else if (inicial) return INICIAL;
    else if (final) return FINAL;
    return NORMAL;
}