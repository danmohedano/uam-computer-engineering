#ifndef ALFA_H
#define ALFA_H

#define MAX_LONG_ID 100
#define MAX_SIZE_VECTOR 64

/* Category of the element */
#define VARIABLE 1
#define PARAMETRO 2
#define FUNCION 3
/* Basic data types */
#define BOOLEAN 1
#define INT 2
/* Variable class */
#define ESCALAR 1
#define VECTOR 2
/* When a field is not used */
#define NU -1
/* Declaration of the maximum number of labels of the compiler */
#define MAX_ETIQUETAS 1000
/* Return value when error */
#define ERROR -1;
/* Flags for yes or no */
#define YES 1
#define NO 0


typedef struct{
    char lexema[MAX_LONG_ID + 1];
    int tipo;
    int valor_entero;
    int es_direccion;
    int etiqueta;
} tipo_atributos;

#endif /* ALFA_H */