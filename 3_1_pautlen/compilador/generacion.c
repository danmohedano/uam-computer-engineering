#include <stdio.h>
#include <stdlib.h>
#include "generacion.h"

#define NAME_STACK_POINTER  "__esp"
#define NAME_ERR_DIV0       "div0"
#define NAME_ERR_IOB        "iob"

#define TAG_ERR_DIV0    "err_div0"
#define TAG_ERR_IOB     "err_iob"

#define MSG_ERR_DIV0    "Run Time Error: Division by zero"
#define MSG_ERR_IOB     "Run Time Error: Index out of bounds"

void escribir_cabecera_bss(FILE* fpasm){
    fprintf(fpasm, "\n; Escribir cabecera\n");
    fprintf(fpasm, "segment .bss\n"
                        "\t%s resd 1\n", NAME_STACK_POINTER);
}

void escribir_subseccion_data(FILE* fpasm) {
    fprintf(fpasm, "\n; Escribir subseccion data\n");
    fprintf(fpasm, "segment .data\n"
                        "\t%s dd \"%s\", 0\n"
                        "\t%s dd \"%s\", 0\n", NAME_ERR_DIV0, MSG_ERR_DIV0, NAME_ERR_IOB, MSG_ERR_IOB);
}

void declarar_variable(FILE* fpasm, char * nombre, int tipo, int tamano){
    fprintf(fpasm, "\n; Declarar variable\n");
    fprintf(fpasm, "\t_%s resd %d\n", nombre, tamano);

}

void escribir_segmento_codigo(FILE* fpasm){
    fprintf(fpasm, "\n; Escribir segmento codigo\n");
    fprintf(fpasm,  "segment .text\n"
                    "global main\n"
                    "extern scan_int, scan_boolean, print_blank, print_endofline, print_string, print_int, print_boolean\n");
}

void escribir_inicio_main(FILE* fpasm){
    fprintf(fpasm, "\n; Escribir inicio main\n");
    fprintf(fpasm, "main:\n"
                        "\tmov DWORD [%s], esp\n", NAME_STACK_POINTER);

}

void escribir_fin(FILE* fpasm){
    fprintf(fpasm, "\n; Escribir fin\n");
    fprintf(fpasm, "fin:\n"
                        "\tmov DWORD esp, [%s]\n"
                        "\tmov DWORD eax, 0\n"
                        "\tret\n"
                    "%s:\n"
                        "\tpush DWORD %s\n"
                        "\tcall print_string\n"
                        "\tadd esp, 4\n"
                        "\tcall print_endofline\n"
                        "\tjmp near fin\n"
                    "%s:\n"
                        "\tpush DWORD %s\n"
                        "\tcall print_string\n"
                        "\tadd esp, 4\n"
                        "\tcall print_endofline\n"
                        "\tjmp near fin\n", NAME_STACK_POINTER, TAG_ERR_DIV0, NAME_ERR_DIV0, TAG_ERR_IOB, NAME_ERR_IOB);
}


void escribir_operando(FILE* fpasm, char* nombre, int es_variable){
    fprintf(fpasm, "\n; Escribir operando\n");
    if (es_variable)
    {
        fprintf(fpasm,"\tpush DWORD _%s\n", nombre);
    }
    else
    {
        fprintf(fpasm,"\tpush DWORD %s\n", nombre);
    }
}


void asignar(FILE* fpasm, char* nombre, int es_variable){
    fprintf(fpasm, "\n; Asignar\n");
    fprintf(fpasm, "\tpop DWORD eax\n");
    if (es_variable)
    {
        fprintf(fpasm, "\tmov DWORD eax, [eax]\n");
    }
    fprintf(fpasm, "\tmov DWORD [_%s], eax\n", nombre);
}

void sumar(FILE* fpasm, int es_variable_1, int es_variable_2){
    fprintf(fpasm, "\n; Sumar\n");
    fprintf(fpasm, "\tpop DWORD edx\n");
    if (es_variable_2)
    {
        fprintf(fpasm, "\tmov DWORD edx, [edx]\n");
    }
    fprintf(fpasm, "\tpop DWORD eax\n");
    if (es_variable_1)
    {
        fprintf(fpasm, "\tmov DWORD eax, [eax]\n");
    }
    fprintf(fpasm,  "\tadd eax, edx\n"
                    "\tpush DWORD eax\n");
}

void restar(FILE* fpasm, int es_variable_1, int es_variable_2){
    fprintf(fpasm, "\n; Restar\n");
    fprintf(fpasm, "\tpop DWORD edx\n");
    if (es_variable_2)
    {
        fprintf(fpasm, "\tmov DWORD edx, [edx]\n");
    }
    fprintf(fpasm, "\tpop DWORD eax\n");
    if (es_variable_1)
    {
        fprintf(fpasm, "\tmov DWORD eax, [eax]\n");
    }
    fprintf(fpasm,  "\tsub eax, edx\n"
                    "\tpush DWORD eax\n");
}

void multiplicar(FILE* fpasm, int es_variable_1, int es_variable_2){
    fprintf(fpasm, "\n; Multiplicar\n");
    fprintf(fpasm, "\tpop DWORD ecx\n");
    if (es_variable_2)
    {
        fprintf(fpasm, "\tmov DWORD ecx, [ecx]\n");
    }
    fprintf(fpasm, "\tpop DWORD eax\n");
    if (es_variable_1)
    {
        fprintf(fpasm, "\tmov DWORD eax, [eax]\n");
    }
    fprintf(fpasm,  "\timul eax, ecx\n"
                    "\tpush DWORD eax\n");
}

void dividir(FILE* fpasm, int es_variable_1, int es_variable_2){
    fprintf(fpasm, "\n; Dividir\n");
    fprintf(fpasm, "\tpop DWORD ecx\n");
    if (es_variable_2)
    {
        fprintf(fpasm, "\tmov DWORD ecx, [ecx]\n");
    }
    fprintf(fpasm, "\tpop DWORD eax\n");
    if (es_variable_1)
    {
        fprintf(fpasm, "\tmov DWORD eax, [eax]\n");
    }
    fprintf(fpasm,  "\tcmp ecx, DWORD 0\n"
                    "\tje near %s\n"
                    "\tcdq\n"
                    "\tidiv ecx\n"
                    "\tpush DWORD eax\n", TAG_ERR_DIV0);
}

void o(FILE* fpasm, int es_variable_1, int es_variable_2){
    fprintf(fpasm, "\n; o\n");
    fprintf(fpasm, "\tpop DWORD edx\n");
    if (es_variable_2)
    {
        fprintf(fpasm, "\tmov DWORD edx, [edx]\n");
    }
    fprintf(fpasm, "\tpop DWORD eax\n");
    if (es_variable_1)
    {
        fprintf(fpasm, "\tmov DWORD eax, [eax]\n");
    }
    fprintf(fpasm,  "\tor eax, edx\n"
                    "\tpush DWORD eax\n");
}

void y(FILE* fpasm, int es_variable_1, int es_variable_2){
    fprintf(fpasm, "\n; y\n");
    fprintf(fpasm, "\tpop DWORD edx\n");
    if (es_variable_2)
    {
        fprintf(fpasm, "\tmov DWORD edx, [edx]\n");
    }
    fprintf(fpasm, "\tpop DWORD eax\n");
    if (es_variable_1)
    {
        fprintf(fpasm, "\tmov DWORD eax, [eax]\n");
    }
    fprintf(fpasm,  "\tand eax, edx\n"
                    "\tpush DWORD eax\n");
}

void cambiar_signo(FILE* fpasm, int es_variable){
    fprintf(fpasm, "\n; Cambiar signo\n");
    fprintf(fpasm, "\tpop DWORD eax\n");
    if (es_variable)
    {
        fprintf(fpasm, "\tmov DWORD eax, [eax]\n");
    }
    fprintf(fpasm, "\tneg eax\n");
    fprintf(fpasm, "\tpush DWORD eax\n");
}

void no(FILE* fpasm, int es_variable, int cuantos_no){
    fprintf(fpasm, "\n; No\n");
    fprintf(fpasm, "\tpop DWORD eax\n");
    if (es_variable)
    {
        fprintf(fpasm, "\tmov DWORD eax, [eax]\n");
    }
    fprintf(fpasm,      "\tor eax, eax\n"
                        "\tjz near negar_falso%d\n"
                        "\tmov DWORD eax, 0\n"
                        "\tjmp near fin_negacion%d\n"
                    "negar_falso%d:\n"
                        "\tmov DWORD eax, 1\n"
                    "fin_negacion%d:\n"
                        "\tpush DWORD eax\n", cuantos_no, cuantos_no, cuantos_no, cuantos_no);
}

void igual(FILE* fpasm, int es_variable1, int es_variable2, int etiqueta){
    fprintf(fpasm, "\n; Igual\n");
    fprintf(fpasm, "\tpop DWORD edx\n");
    if (es_variable2)
    {
        fprintf(fpasm, "\tmov DWORD edx, [edx]\n");
    }
    fprintf(fpasm, "\tpop DWORD eax\n");
    if (es_variable1)
    {
        fprintf(fpasm, "\tmov DWORD eax, [eax]\n");
    }
    fprintf(fpasm,      "\tcmp eax, edx\n"
                        "\tje near igual%d\n"
                        "\tpush DWORD 0\n"
                        "\tjmp near fin_igual%d\n"
                    "igual%d:\n"
                        "\tpush DWORD 1\n"
                    "fin_igual%d:\n", etiqueta, etiqueta, etiqueta, etiqueta);
}
void distinto(FILE* fpasm, int es_variable1, int es_variable2, int etiqueta){
    fprintf(fpasm, "\n; Distinto\n");
    fprintf(fpasm, "\tpop DWORD edx\n");
    if (es_variable2)
    {
        fprintf(fpasm, "\tmov DWORD edx, [edx]\n");
    }
    fprintf(fpasm, "\tpop DWORD eax\n");
    if (es_variable1)
    {
        fprintf(fpasm, "\tmov DWORD eax, [eax]\n");
    }
    fprintf(fpasm,      "\tcmp eax, edx\n"
                        "\tjne near distinto%d\n"
                        "\tpush DWORD 0\n"
                        "\tjmp near fin_distinto%d\n"
                    "distinto%d:\n"
                        "\tpush DWORD 1\n"
                    "fin_distinto%d:\n", etiqueta, etiqueta, etiqueta, etiqueta);
}
void menor_igual(FILE* fpasm, int es_variable1, int es_variable2, int etiqueta){
    fprintf(fpasm, "\n; Menor Igual\n");
    fprintf(fpasm, "\tpop DWORD edx\n");
    if (es_variable2)
    {
        fprintf(fpasm, "\tmov DWORD edx, [edx]\n");
    }
    fprintf(fpasm, "\tpop DWORD eax\n");
    if (es_variable1)
    {
        fprintf(fpasm, "\tmov DWORD eax, [eax]\n");
    }
    fprintf(fpasm,      "\tcmp eax, edx\n"
                        "\tjle near menorigual%d\n"
                        "\tpush DWORD 0\n"
                        "\tjmp near fin_menorigual%d\n"
                    "menorigual%d:\n"
                        "\tpush DWORD 1\n"
                    "fin_menorigual%d:\n", etiqueta, etiqueta, etiqueta, etiqueta);
}
void mayor_igual(FILE* fpasm, int es_variable1, int es_variable2, int etiqueta){
    fprintf(fpasm, "\n; Mayor Igual\n");
    fprintf(fpasm, "\tpop DWORD edx\n");
    if (es_variable2)
    {
        fprintf(fpasm, "\tmov DWORD edx, [edx]\n");
    }
    fprintf(fpasm, "\tpop DWORD eax\n");
    if (es_variable1)
    {
        fprintf(fpasm, "\tmov DWORD eax, [eax]\n");
    }
    fprintf(fpasm,      "\tcmp eax, edx\n"
                        "\tjge near mayorigual%d\n"
                        "\tpush DWORD 0\n"
                        "\tjmp near fin_mayorigual%d\n"
                    "mayorigual%d:\n"
                        "\tpush DWORD 1\n"
                    "fin_mayorigual%d:\n", etiqueta, etiqueta, etiqueta, etiqueta);
}
void menor(FILE* fpasm, int es_variable1, int es_variable2, int etiqueta){
    fprintf(fpasm, "\n; Menor\n");
    fprintf(fpasm, "\tpop DWORD edx\n");
    if (es_variable2)
    {
        fprintf(fpasm, "\tmov DWORD edx, [edx]\n");
    }
    fprintf(fpasm, "\tpop DWORD eax\n");
    if (es_variable1)
    {
        fprintf(fpasm, "\tmov DWORD eax, [eax]\n");
    }
    fprintf(fpasm,      "\tcmp eax, edx\n"
                        "\tjl near menor%d\n"
                        "\tpush DWORD 0\n"
                        "\tjmp near fin_menor%d\n"
                    "menor%d:\n"
                        "\tpush DWORD 1\n"
                    "fin_menor%d:\n", etiqueta, etiqueta, etiqueta, etiqueta);
}
void mayor(FILE* fpasm, int es_variable1, int es_variable2, int etiqueta){
    fprintf(fpasm, "\n; Mayor\n");
    fprintf(fpasm, "\tpop DWORD edx\n");
    if (es_variable2)
    {
        fprintf(fpasm, "\tmov DWORD edx, [edx]\n");
    }
    fprintf(fpasm, "\tpop DWORD eax\n");
    if (es_variable1)
    {
        fprintf(fpasm, "\tmov DWORD eax, [eax]\n");
    }
    fprintf(fpasm,      "\tcmp eax, edx\n"
                        "\tjg near mayor%d\n"
                        "\tpush DWORD 0\n"
                        "\tjmp near fin_mayor%d\n"
                    "mayor%d:\n"
                        "\tpush DWORD 1\n"
                    "fin_mayor%d:\n", etiqueta, etiqueta, etiqueta, etiqueta);
}

void leer(FILE* fpasm, int tipo){
    fprintf(fpasm, "\n; Leer\n");
    if (tipo == INT)
    {
        fprintf(fpasm, "\tcall scan_int\n");
    }
    else
    {
        fprintf(fpasm, "\tcall scan_boolean\n");
    }
    fprintf(fpasm, "\tadd esp, 4\n");
}
void escribir(FILE* fpasm, int es_variable, int tipo){
    fprintf(fpasm, "\n; Escribir\n");
    if (es_variable)
    {
        fprintf(fpasm,  "\tpop DWORD eax\n"
                        "\tmov DWORD eax, [eax]\n"
                        "\tpush DWORD eax\n");
    }
    if (tipo == INT)
    {
        fprintf(fpasm, "\tcall print_int\n");
    }
    else
    {
        fprintf(fpasm, "\tcall print_boolean\n");
    }
    fprintf(fpasm,  "\tadd esp, 4\n"
                    "\tcall print_endofline\n");
}



/* ---------------------- Part 2 ---------------------------------------*/
void ifthenelse_inicio(FILE * fpasm, int exp_es_variable, int etiqueta){
    fprintf(fpasm, "\n; Inicio de if then, else\n");
    fprintf(fpasm, "\tpop eax\n");
    if (exp_es_variable == 1){
        fprintf(fpasm, "\tmov eax, [eax]\n");
    }

    fprintf(fpasm,  "\tcmp eax, 0\n"
                    "\tje near fin_then%d\n", etiqueta);
}

void ifthen_inicio(FILE * fpasm, int exp_es_variable, int etiqueta){
    fprintf(fpasm, "\n; Inicio de if then\n");
    fprintf(fpasm, "\tpop eax\n");
     if (exp_es_variable == 1){
        fprintf(fpasm, "\tmov eax, [eax]\n");
    }

    fprintf(fpasm,  "\tcmp eax, 0\n"
                    "\tje near fin_then%d\n", etiqueta);
}

void ifthen_fin(FILE * fpasm, int etiqueta){
    fprintf(fpasm, "\n; Fin de if then\n");
    fprintf(fpasm, "fin_then%d:\n", etiqueta);
}

void ifthenelse_fin_then( FILE * fpasm, int etiqueta){
    fprintf(fpasm, "\n; Fin de if then, else, then\n");
    fprintf(fpasm,  "\tjmp near fin_ifelse%d\n"
                    "fin_then%d:\n", etiqueta, etiqueta);
}

void ifthenelse_fin( FILE * fpasm, int etiqueta){
    fprintf(fpasm, "\n; If then else fin\n");
    fprintf(fpasm,  "fin_ifelse%d:\n", etiqueta);
}

void while_inicio(FILE * fpasm, int etiqueta){ 
    fprintf(fpasm, "\n; While inicio\n");
    fprintf(fpasm, "inicio_while%d:\n", etiqueta);
}

void while_exp_pila (FILE * fpasm, int exp_es_variable, int etiqueta){
    fprintf(fpasm, "\n; While exp pila\n");
    fprintf(fpasm, "\tpop eax\n");
    if (exp_es_variable > 0){
        fprintf(fpasm, "\tmov eax, [eax]\n");
    }
    fprintf(fpasm,  "\tcmp eax, 0\n"
                    "\tje near fin_while%d\n", etiqueta);
}

void while_fin( FILE * fpasm, int etiqueta){
    fprintf(fpasm, "\n; While fin\n");
    fprintf(fpasm,  "\tjmp near inicio_while%d\n"
                    "fin_while%d:\n", etiqueta, etiqueta);
}

void escribir_elemento_vector(FILE * fpasm,char * nombre_vector, int tam_max, int exp_es_direccion){
    fprintf(fpasm, "\n; Escribir elemento vector\n");
    fprintf(fpasm, "\tpop DWORD eax\n");
    if (exp_es_direccion == 1){
        fprintf(fpasm, "\tmov DWORD eax, [eax]\n");
    }
    fprintf(fpasm,  "\tcmp eax, 0\n"
                    "\tjl near %s\n"
                    "\tcmp eax, %d\n"
                    "\tjg near %s\n"
                    "\tmov DWORD edx, _%s\n"
                    "\tlea eax, [edx + eax*4]\n"
                    "\tpush DWORD eax\n", TAG_ERR_IOB, tam_max-1, TAG_ERR_IOB, nombre_vector);
}

void declararFuncion(FILE * fpasm, char * nombre_funcion, int num_var_loc){
    fprintf(fpasm, "\n; Declarar funcion\n");
    fprintf(fpasm,  "_%s:\n"
                        "\tpush ebp\n"
                        "\tmov ebp, esp\n"
                        "\tsub esp, %d\n", nombre_funcion, 4*num_var_loc);
}

void retornarFuncion(FILE * fpasm, int es_variable){
    fprintf(fpasm, "\n; Retornar funcion\n");
    fprintf(fpasm, "\tpop eax\n");
    if(es_variable== 1){
        fprintf(fpasm, "\tmov DWORD eax, [eax]\n");
    }
    fprintf(fpasm,  "\tmov esp, ebp\n"
                    "\tpop ebp\n"
                    "\tret\n");
}

void escribirParametro(FILE* fpasm, int pos_parametro, int num_total_parametros){
    fprintf(fpasm, "\n; Escribir parametro\n");
    fprintf(fpasm,  "\tlea eax, [ebp + %d]\n"
                    "\tpush DWORD eax\n", 4 * ( 1 + (num_total_parametros - pos_parametro)));
}

void escribirVariableLocal(FILE* fpasm, int posicion_variable_local){
    fprintf(fpasm, "\n; Escribir variable local\n");
    fprintf(fpasm,  "\tlea eax, [ebp - %d]\n"
                    "\tpush DWORD eax\n", 4 * posicion_variable_local);
}

void asignarDestinoEnPila(FILE* fpasm, int es_variable){
    fprintf(fpasm, "\n; Asignar destino en pila\n");
    fprintf(fpasm,  "\tpop DWORD ebx\n"
                    "\tpop DWORD eax\n");
    if (es_variable){
        fprintf(fpasm, "\tmov DWORD eax, [eax]\n");
    }
    fprintf(fpasm, "\tmov DWORD [ebx], eax\n"); 
}

void asignarElementoVector(FILE* fpasm, int es_variable){
    fprintf(fpasm, "\n; Asignar destino en pila\n");
    fprintf(fpasm,  "\tpop DWORD eax\n"
                    "\tpop DWORD ebx\n");
    if (es_variable){
        fprintf(fpasm, "\tmov DWORD eax, [eax]\n");
    }
    fprintf(fpasm, "\tmov DWORD [ebx], eax\n"); 
}

void operandoEnPilaAArgumento(FILE * fpasm, int es_variable){
    fprintf(fpasm, "\n; Operando en pila a argumento\n");
    if(es_variable){
        fprintf(fpasm,  "\tpop eax\n"
                        "\tmov eax, [eax]\n"
                        "\tpush eax\n");  
    }
}

void llamarFuncion(FILE * fpasm, char * nombre_funcion, int num_argumentos){
    fprintf(fpasm, "\n; Llamar funcion\n");
    fprintf(fpasm,  "\tcall _%s\n", nombre_funcion);
    limpiarPila(fpasm, num_argumentos);
    fprintf(fpasm, "\tpush DWORD eax\n");
}

void limpiarPila(FILE * fpasm, int num_argumentos){
    fprintf(fpasm, "\n; Limpiar pila\n");
    fprintf(fpasm, "\tadd esp, %d\n", 4*num_argumentos);
}
