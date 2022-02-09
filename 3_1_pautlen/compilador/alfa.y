%{
#include <stdio.h>
#include <string.h>
#include "alfa.h"
#include "hash_data.h"
#include "symbol_table.h"
#include "generacion.h"

extern int line;
extern int total_length;
extern int start_line;
extern int flex_error;

extern FILE *yyin;
extern FILE *yyout;
extern int yylex(void);

/* User defined functions */
int yyerror(char *s);
DATA *create_global_var(char *lexema);
DATA *create_local_var(char *lexema);
DATA *create_param(char *lexema);
DATA *create_function(char *lexema);

/* Definition of the symbol table as global */
symbol_table *table = NULL;

/*------Global Variables------*/
/* For horizontal inheritance */
int tipo_actual;
int clase_actual;
int tamanio_vector_actual;
/* Used in function creation */
int pos_variable_local_actual = 0;
int num_variables_locales_actual;
int pos_parametro_actual;
int num_parametros_actual;
/* Used in function call */
int num_parametros_llamada_actual;
int en_explist = 0;
/* Counter for number of tags in asm file */
int etiqueta = 1;
/* Auxiliary variables related to functions */
int tipo_funcion_actual;
int return_exists = NO;
/* Auxiliary variable for horizontal inheritance of a vector error (to print the name) */
int error_vector = 0;
%}

%union {
    tipo_atributos attributes;
}

/* Reserved Words */ 
%token TOK_MAIN
%token TOK_INT
%token TOK_BOOLEAN
%token TOK_ARRAY
%token TOK_FUNCTION
%token TOK_IF
%token TOK_ELSE
%token TOK_WHILE
%token TOK_SCANF
%token TOK_PRINTF
%token TOK_RETURN


/* Symbols */
%token TOK_PUNTOYCOMA
%token TOK_COMA
%token TOK_PARENTESISIZQUIERDO
%token TOK_PARENTESISDERECHO
%token TOK_CORCHETEIZQUIERDO
%token TOK_CORCHETEDERECHO
%token TOK_LLAVEIZQUIERDA
%token TOK_LLAVEDERECHA
%token TOK_ASIGNACION
%token TOK_MAS
%token TOK_MENOS
%token TOK_DIVISION
%token TOK_ASTERISCO
%token TOK_AND 
%token TOK_OR
%token TOK_NOT
%token TOK_IGUAL
%token TOK_DISTINTO
%token TOK_MENORIGUAL
%token TOK_MAYORIGUAL
%token TOK_MENOR
%token TOK_MAYOR


/* Identifiers  */
%token <attributes> TOK_IDENTIFICADOR

/* Constants */ 
%token <attributes> TOK_CONSTANTE_ENTERA
%token TOK_TRUE
%token TOK_FALSE

/* Error Token */
%token TOK_ERROR

/* Precedence definition */
%left TOK_MENOR TOK_MAYOR TOK_IGUAL TOK_DISTINTO TOK_MENORIGUAL TOK_MAYORIGUAL
%left TOK_MAS TOK_MENOS TOK_OR
%left TOK_ASTERISCO TOK_DIVISION TOK_AND
%right TOK_NOT MENOSU

/* Non-terminals with attributes */
%type <attributes> condicional
%type <attributes> comparacion
%type <attributes> elemento_vector
%type <attributes> exp
%type <attributes> constante
%type <attributes> constante_entera
%type <attributes> constante_logica
%type <attributes> identificador
%type <attributes> idf_llamada_funcion
%type <attributes> if_exp
%type <attributes> if_exp_sentencias
%type <attributes> ifelse_exp_sentencias
%type <attributes> while_inicio
%type <attributes> while_exp
%type <attributes> fn_name
%type <attributes> fn_declaration
%%

programa:   inicioTabla TOK_MAIN TOK_LLAVEIZQUIERDA escritura_bss declaraciones escritura_data_text funciones escritura_main sentencias TOK_LLAVEDERECHA 
            {
                /* Prints to the asm file the closing of the main function when the whole program has been matched by the parser */
                escribir_fin(yyout);
                //fprintf(yyout, ";R1:\t<programa> ::= main { <declaraciones> <funciones> <sentencias> }\n"); 
            }

inicioTabla: /* EMPTY */    
            {
                /* Creation of the symbol table at the start */
                table = symbol_create();
                if (!table){
                    fprintf(stderr, "Error creating the symbol table\n");
                    return ERROR;
                }
            }

escritura_bss: /* EMPTY */
                {
                    /* Prints the bss header to the asm file */
                    escribir_cabecera_bss(yyout);         
                }

escritura_data_text: /* EMPTY */ 
                    {
                        /* Writes the data header (and content) and then the text header */
                        escribir_subseccion_data(yyout);
                        escribir_segmento_codigo(yyout);
                    }

escritura_main:     /* EMPTY */
                    {
                        /* Prints the main tag to the asm file */
                        escribir_inicio_main(yyout);
                    }

declaraciones:  declaracion               
                {
                    //fprintf(yyout, ";R2:\t<declaraciones> ::= <declaracion>\n");
                }
                | declaracion declaraciones 
                {
                    //fprintf(yyout, ";R3:\t<declaraciones> ::= <declaracion> <declaraciones>\n");
                }

declaracion:    clase identificadores TOK_PUNTOYCOMA 
                {
                    //fprintf(yyout, ";R4:\t<declaracion> ::= <clase> <identificadores> ;\n");
                }

clase:  clase_escalar
        {
            clase_actual = ESCALAR;
            //fprintf(yyout, ";R5:\t<clase> ::= <clase_escalar>\n");
        }
        | clase_vector
        {   
            clase_actual = VECTOR;
            //fprintf(yyout, ";R7:\t<clase> ::= <clase_vector>\n");
        }

clase_escalar:  tipo 
                {
                    //fprintf(yyout, ";R9:\t<clase_escalar> ::= <tipo>\n");
                }

tipo:   TOK_INT
        {
            /* Saves the type of the declaration to a global variable to propagate it */
            tipo_actual = INT;
            //fprintf(yyout, ";R10:\t<tipo> ::= int\n");
        }
        | TOK_BOOLEAN     
        {
            /* Saves the type of the declaration to a global variable to propagate it */
            tipo_actual = BOOLEAN;
            //fprintf(yyout, ";R11:\t<tipo> ::= boolean\n");
        }

clase_vector:   TOK_ARRAY tipo TOK_CORCHETEIZQUIERDO TOK_CONSTANTE_ENTERA TOK_CORCHETEDERECHO 
                {
                    /* Check if the vector is correct */
                    tamanio_vector_actual = $4.valor_entero;
                    if (tamanio_vector_actual < 1 || tamanio_vector_actual > MAX_SIZE_VECTOR){
                        /* Global that will be checked when we parse the vector name to print the 
                         * name in the error message */
                        error_vector = 1;
                    }
                    //fprintf(yyout, ";R15:\t<clase_vector> ::= array <tipo> [ <constante_entera> ]\n");
                }

identificadores:    identificador                          
                    {
                        //fprintf(yyout, ";R18:\t<identificadores> ::= <identificador>\n");
                    }
                    | identificador TOK_COMA identificadores  
                    {
                        //fprintf(yyout, ";R19:\t<identificadores> ::= <identificador> , <identificadores>\n");
                    }

funciones:  funcion funciones    
            {
                //fprintf(yyout, ";R20:\t<funciones> ::= <funcion> <funciones>\n");
            }
            | /* EMPTY */                    
            {
               //fprintf(yyout, ";R21:\t<funciones> ::= \n");
            }

funcion:    fn_declaration sentencias TOK_LLAVEDERECHA 
            {
                
                /* Close scope */
                symbol_close_scope(table);
                DATA *obj = symbol_search(table, $1.lexema);
                /* Check that the identifier exists in the symbol table */
                if (!obj){
                    fprintf(stderr, "This shouldn't happen.\n");
                    return ERROR;
                }
                /* Check that the function has at least 1 return call */
                if (return_exists == NO){
                    fprintf(stderr, "****Semantic Error in line %d: Function (%s) without return statement.\n", line, $1.lexema);
                    return ERROR;
                }
                obj->n_param = num_parametros_actual;
                obj->n_local_var = num_variables_locales_actual;
                //fprintf(yyout, ";R22:\t<funcion> ::= funcion <tipo> <identificador> ( <parametros_funcion ) { <declaraciones_funcion> <sentencias> }\n");
            }

fn_declaration: fn_name TOK_PARENTESISIZQUIERDO parametros_funcion TOK_PARENTESISDERECHO TOK_LLAVEIZQUIERDA declaraciones_funcion
                {
                    DATA *obj = symbol_search(table, $1.lexema);
                    /* Check that the identifier exists in the symbol table */
                    if (!obj){
                        fprintf(stderr, "****Semantic Error in line %d: Accessing non-declared function (%s).\n", line, $1.lexema);
                        return ERROR;
                    }
                    obj->n_param = num_parametros_actual;
                    obj->n_local_var = num_variables_locales_actual;
                    return_exists = NO;
                    strcpy($$.lexema, $1.lexema);
                    declararFuncion(yyout, $1.lexema, num_variables_locales_actual);
                }

fn_name:    TOK_FUNCTION tipo TOK_IDENTIFICADOR
            {
                int ret;
                /*Create the function*/
                DATA *obj = create_function($3.lexema);
                /*Check if  the object exists*/
                if (!obj) return ERROR;
                ret = symbol_open_scope(table, obj);
                /*Check if there's an error with the declaration*/
                if (ret == DUPLICATED_DECLARATION){
                    fprintf(stderr, "****Semantic Error in line %d: Duplicated declaration\n", line);
                    return ERROR;
                }
                else if (ret == -1){
                    fprintf(stderr, "Error inserting\n");
                    return ERROR;
                }
                else if (ret == SCOPE_ALREADY_OPEN){
                    fprintf(stderr, "THIS SHOULDNT HAPPEN.\n");
                    return ERROR;
                }
                num_variables_locales_actual = 0;
                pos_variable_local_actual = 1;
                num_parametros_actual = 0;
                pos_parametro_actual = 0;
                tipo_funcion_actual = tipo_actual;
                strcpy($$.lexema, $3.lexema);
            }

parametros_funcion: parametro_funcion resto_parametros_funcion 
                    {
                        //fprintf(yyout, ";R23:\t<parametros_funcion> ::= <parametro_funcion> <resto_parametros_funcion>\n");
                    }
                    | /* EMPTY */
                    {
                        //fprintf(yyout, ";R24:\t<parametros_funcion> ::= \n");
                    }
resto_parametros_funcion:   TOK_PUNTOYCOMA parametro_funcion resto_parametros_funcion     
                            {
                                //fprintf(yyout, ";R25:\t<resto_parametros_funcion> ::= ; <parametro_funcion> <resto_parametros_funcion>\n");
                            }
                            | /* EMPTY */                                                      
                            {
                                //fprintf(yyout, ";R26:\t<resto_parametros_funcion> ::= <>\n");
                            }

parametro_funcion:  tipo idpf 
                    {
                        //fprintf(yyout, ";R27:\t<parametro_funcion> ::= <tipo> <identificador>\n");
                    }

idpf:   TOK_IDENTIFICADOR
        {
            /* Checks if there is a function scope opened */
            if (!(table->local)){
                fprintf(stderr, "Oops, local scope should be open. This shouldnt happen\n");
                return ERROR;
            }

            /* Creates a hash_data of type param */
            DATA *dt = create_param($1.lexema);
            if (!dt){
                fprintf(stderr, "Couldnt malloc a hash_data structure\n");
                return ERROR;
            }

            /* Inserts the param into the symbol table (the local one, because we are inside a function) */
            int res = symbol_insert(table, dt);
            if (res == DUPLICATED_DECLARATION){
                fprintf(stderr, "****Semantic Error in line %d: Duplicated declaration\n", line);
                return ERROR;
            }
            /* Updates some global variables that will be used to determine the number of params of the function and the pos of each */
            pos_parametro_actual++;
            num_parametros_actual++;
        }

declaraciones_funcion:  declaraciones    
                        {
                            //fprintf(yyout, ";R28:\t<declaraciones_funcion> ::= <declaraciones>\n");
                        }
                        | /* EMPTY */
                        {
                            //fprintf(yyout, ";R29:\t<declaraciones_funcion> ::= <>\n");
                        }

sentencias: sentencia                   
            {
                //fprintf(yyout, ";R30:\t<sentencias> ::= <sentencia>\n");
            }
            | sentencia sentencias        
            {
                //fprintf(yyout, ";R31:\t<sentencias> ::= <sentencia> <sentencias>\n");
            }

sentencia:  sentencia_simple TOK_PUNTOYCOMA      
            {
                //fprintf(yyout, ";R32:\t<sentencia> ::= <sentencia_simple> ;\n");
            }
            | bloque                               
            {
                //fprintf(yyout, ";R33:\t<sentencia> ::= <bloque>\n");
            }

sentencia_simple:   asignacion            
                    {
                        //fprintf(yyout, ";R34:\t<sentencia_simple> ::= <asignacion>\n");
                    }
                    | lectura               
                    {
                        //fprintf(yyout, ";R35:\t<sentencia_simple> ::= <lectura>\n");
                    }
                    | escritura             
                    {
                        //fprintf(yyout, ";R36:\t<sentencia_simple> ::= <escritura>\n");
                    }
                    | retorno_funcion       
                    {
                        //fprintf(yyout, ";R38:\t<sentencia_simple> ::= <retorno_funcion>\n");
                    }
                  
bloque: condicional     
        {
            //fprintf(yyout, ";R40:\t<bloque> ::= <condicional>\n");
        }
        | bucle           
        {
            //fprintf(yyout, ";R41:\t<bloque> ::= <bucle>\n");
        }
        
asignacion: TOK_IDENTIFICADOR TOK_ASIGNACION exp
            {
                /* Checks if the variable exists in the symbol table */
                DATA *obj = symbol_search(table, $1.lexema);
                /* Check that the identifier exists in the symbol table */
                if (!obj){
                    fprintf(stderr, "****Semantic Error in line %d: Accessing non-declared variable (%s).\n", line, $1.lexema);
                    return ERROR;
                }
                
                /* Checks that the variable is not a function, nor a vector or that it is assigning an element of a different type */
                if (obj->category == FUNCION){
                    fprintf(stderr, "****Semantic Error in line %d: Using function (%s) as variable.\n", line, $1.lexema);
                    return ERROR;
                }
                if (obj->clase == VECTOR){
                    fprintf(stderr, "****Semantic Error in line %d: Using vector (%s) as variable.\n", line, $1.lexema);
                    return ERROR;
                }
                if (obj->type != $3.tipo){
                    fprintf(stderr, "****Semantic Error in line %d: Incompatible assignment.\n", line);
                    return ERROR;
                }
                
                /* Depending on the type of the variable (global, local or param) it inserts it into the stack in a different way */
                if (obj->pos_param != NU){
                    /* Check if it is a parameter*/
                    escribirParametro(yyout, obj->pos_param, num_parametros_actual);
                    asignarDestinoEnPila(yyout, $3.es_direccion);
                }else if (obj->pos_local_var != NU){
                    /* Check if it is a local variable */
                    escribirVariableLocal(yyout, obj->pos_local_var);
                    asignarDestinoEnPila(yyout, $3.es_direccion);
                }
                else{
                    asignar(yyout, $1.lexema, $3.es_direccion);
                }
                //fprintf(yyout, ";R43:\t<asignacion> ::= <identificador> = <exp>\n");
            }
            | elemento_vector TOK_ASIGNACION exp 
            {
                /* Checks if the types of the vector and exp are the same. If so, it saves it into the vector */
                if ($1.tipo != $3.tipo){
                    return ERROR;
                }
                asignarElementoVector(yyout, $3.es_direccion);
                //fprintf(yyout, ";R44:\t<asignacion> ::= <elemento_vector> = <exp>\n");
            }
            
elemento_vector: TOK_IDENTIFICADOR TOK_CORCHETEIZQUIERDO exp TOK_CORCHETEDERECHO    
                {
                    /* Checks if the vector exists and is of class vector. Also checks we index with an integer expression */
                    DATA *obj = symbol_search(table, $1.lexema);
                    /* Check that the identifier exists in the symbol table */
                    if (!obj){
                        fprintf(stderr, "****Semantic Error in line %d: Accessing non-declared variable (%s).\n", line, $1.lexema);
                        return ERROR;
                    }
                    if (obj->clase != VECTOR){
                        fprintf(stderr, "****Semantic Error in line %d: Trying to index non-vector variable.\n", line);
                        return ERROR;
                    }
                    if ($3.tipo != INT){
                        fprintf(stderr, "****Semantic Error in line %d: Index must be integer type.\n", line);
                        return ERROR;
                    }
                    /* Propagates some values and writes the memory address of t he vector element to the stack */
                    $$.tipo = obj->type;
                    $$.es_direccion = 1;
                    escribir_elemento_vector(yyout, $1.lexema, obj->size, $3.es_direccion);
                    //fprintf(yyout, ";R48:\t<elemento_vector> ::= <identificador> [ <exp> ]\n");
                }

condicional:    if_exp_sentencias 
                {
                    //fprintf(yyout, ";R50:\t<condicional> ::= if ( <exp> ) { <sentencias> }\n");
                }
                | ifelse_exp_sentencias TOK_LLAVEIZQUIERDA sentencias TOK_LLAVEDERECHA 
                {
                    /* Closes the else of an if else in the asm file */
                    ifthenelse_fin(yyout, $1.etiqueta);
                    //fprintf(yyout, ";R51:\t<condicional> ::= if ( <exp> ) { <sentencias> } else { <sentencias> }\n");
                }

if_exp_sentencias:  if_exp sentencias TOK_LLAVEDERECHA
                    {
                        /* Closes the if of an if then in the asm file */
                        $$.etiqueta = $1.etiqueta;
                        ifthen_fin(yyout, $$.etiqueta);
                    }

ifelse_exp_sentencias:  if_exp sentencias TOK_LLAVEDERECHA TOK_ELSE
                        {
                            /* Closes the if of an if else in the asm file */
                            $$.etiqueta = $1.etiqueta;
                            ifthenelse_fin_then(yyout, $$.etiqueta);
                        }

if_exp: TOK_IF TOK_PARENTESISIZQUIERDO exp TOK_PARENTESISDERECHO TOK_LLAVEIZQUIERDA
        {
            /* Checks that the expression inside the if condition is boolean */
            if ($3.tipo != BOOLEAN){
                fprintf(stderr, "****Semantic Error in line %d: Conditional with condition of type int.\n", line);
                return ERROR;
            }
            /* Saves the tag so its the same when we close the if and open and close the else and then increases it */
            $$.etiqueta = etiqueta++;
            ifthen_inicio(yyout, $3.es_direccion, $$.etiqueta);
        }

bucle:  while_exp sentencias TOK_LLAVEDERECHA 
        {
            /* Closes the while */
            while_fin(yyout, $1.etiqueta);
            //fprintf(yyout, ";R52:\t<bucle> ::= while ( <exp> ) { <sentencias> }\n");
        }

while_inicio:   TOK_WHILE TOK_PARENTESISIZQUIERDO
                {
                    /* Opens the while in the asm */
                    $$.etiqueta = etiqueta++;
                    while_inicio(yyout, $$.etiqueta);
                }

while_exp:  while_inicio exp TOK_PARENTESISDERECHO TOK_LLAVEIZQUIERDA
            {
                /* Checks that the expression inside the while is a boolean and writes it into the asm */
                if ($2.tipo != BOOLEAN){
                    fprintf(stderr, "****Semantic Error in line %d: Conditional with condition of type int.\n", line);
                    return ERROR;
                }
                $$.etiqueta = $1.etiqueta;
                while_exp_pila(yyout, $2.es_direccion, $$.etiqueta);
            }

lectura:    TOK_SCANF TOK_IDENTIFICADOR 
            {   
                DATA *obj = symbol_search(table, $2.lexema);
                /* Check that the identifier exists in the symbol table */
                if (!obj){
                    fprintf(stderr, "****Semantic Error in line %d: Accessing non-declared variable (%s).\n", line, $2.lexema);
                    return ERROR;
                }
                if (obj->clase != ESCALAR){
                    fprintf(stderr, "****Semantic Error in line %d: Trying to use vector as reading parameter.\n", line);
                    return ERROR;
                }
                /* Introduce direction to write into the stack */
                if (obj->pos_param != NU){
                    /* Check if it is a parameter*/
                    escribirParametro(yyout, obj->pos_param, num_parametros_actual);
                }else if (obj->pos_local_var != NU){
                    /* Check if it is a local variable */
                    escribirVariableLocal(yyout, obj->pos_local_var);
                }else{
                    /* The variable is global */
                    escribir_operando(yyout, $2.lexema, 1);
                }
                /* Call the code generation function */
                leer(yyout, obj->type);
                //fprintf(yyout, ";R54:\t<lectura> ::= scanf <identificador>\n");
            }

escritura:  TOK_PRINTF exp
            {
                escribir(yyout, $2.es_direccion, $2.tipo);
                //fprintf(yyout, ";R56:\t<escritura> ::= printf <exp>\n");
            }

retorno_funcion:    TOK_RETURN exp 
                    {
                        if (!(table->local)){
                            fprintf(stderr, "****Semantic Error in line %d: Return outside of function body.\n", line);
                            return ERROR;
                        }
                        if ($2.tipo != tipo_funcion_actual){
                            fprintf(stderr, "****Semantic Error in line %d: Return of wrong type.\n", line);
                            return ERROR;
                        }
                        /* Activate flag to indicate a return was found in the function */
                        return_exists = YES;
                        retornarFuncion(yyout, $2.es_direccion);
                        //fprintf(yyout, ";R61:\t<retorno_funcion> ::= return <exp>\n");
                    }

exp:  exp TOK_MAS exp           
    {
        /*Check if there's a semantic error*/
        if ($1.tipo != INT || $3.tipo != INT){
            fprintf(stderr, "****Semantic Error in line %d: Arithmetic operation with boolean operand.\n", line);
            return ERROR;
        }
        $$.tipo = INT;
        $$.es_direccion = 0;
        /*Generate code for the sum*/
        sumar(yyout, $1.es_direccion, $3.es_direccion);
        //fprintf(yyout, ";R72:\t<exp> ::= <exp> + <exp>\n");
    }
    | exp TOK_MENOS exp         
    {
        /*Check if there's a semantic error*/
        if ($1.tipo != INT || $3.tipo != INT){
            fprintf(stderr, "****Semantic Error in line %d: Arithmetic operation with boolean operand.\n", line);
            return ERROR;
        }
        $$.tipo = INT;
        $$.es_direccion = 0;
        /*Generate code for the substraction*/
        restar(yyout, $1.es_direccion, $3.es_direccion);
        //fprintf(yyout, ";R73:\t<exp> ::= <exp> - <exp>\n");
    }
    | exp TOK_DIVISION exp      
    {
        /*Check if there's a semantic error*/
        if ($1.tipo != INT || $3.tipo != INT){
            fprintf(stderr, "****Semantic Error in line %d: Arithmetic operation with boolean operand.\n", line);
            return ERROR;
        }
        $$.tipo = INT;
        $$.es_direccion = 0;
        /*Generate code for the division*/
        dividir(yyout, $1.es_direccion, $3.es_direccion);
        //fprintf(yyout, ";R74:\t<exp> ::= <exp> / <exp>\n");
    }
    | exp TOK_ASTERISCO exp    
    {
        /*Check if there's a semantic error*/
        if ($1.tipo != INT || $3.tipo != INT){
            fprintf(stderr, "****Semantic Error in line %d: Arithmetic operation with boolean operand.\n", line);
            return ERROR;
        }
        $$.tipo = INT;
        $$.es_direccion = 0;
        /*Generate code for the multiplication*/
        multiplicar(yyout, $1.es_direccion, $3.es_direccion);
        //fprintf(yyout, ";R75:\t<exp> ::= <exp> * <exp>\n");
    }
    | TOK_MENOS exp %prec MENOSU      
    {
        /*Check if there's a semantic error*/
        if ($2.tipo != INT){
            fprintf(stderr, "****Semantic Error in line %d: Arithmetic operation with boolean operand.\n", line);
            return ERROR;
        }
        $$.tipo = INT;
        $$.es_direccion = 0;
        /*Generate code for the sign changing*/
        cambiar_signo(yyout, $2.es_direccion);
        //fprintf(yyout, ";R76:\t<exp> ::= - <exp>\n");
    }
    | exp TOK_AND exp           
    {
        if ($1.tipo != BOOLEAN || $3.tipo != BOOLEAN){
            fprintf(stderr, "****Semantic Error in line %d: Logical operation with integer operand.\n", line);
            return ERROR;
        }
        $$.tipo = BOOLEAN;
        $$.es_direccion = 0;
        /*Generate code for the logical operation AND*/
        y(yyout, $1.es_direccion, $3.es_direccion);
        //fprintf(yyout, ";R77:\t<exp> ::= <exp> && <exp>\n");
    }
    | exp TOK_OR exp            
    {
        /*Check if there's a semantic error*/
        if ($1.tipo != BOOLEAN || $3.tipo != BOOLEAN){
            fprintf(stderr, "****Semantic Error in line %d: Logical operation with integer operand.\n", line);
            return ERROR;
        }
        $$.tipo = BOOLEAN;
        $$.es_direccion = 0;
        /*Generate code for the logical operation OR*/
        o(yyout, $1.es_direccion, $3.es_direccion);
        //fprintf(yyout, ";R78:\t<exp> ::= <exp> || <exp>\n");
    }
    | TOK_NOT exp               
    {   
        /*Check if there's a semantic error*/
        if ($2.tipo != BOOLEAN){
            fprintf(stderr, "****Semantic Error in line %d: Logical operation with integer operand.\n", line);
            return ERROR;
        }
        $$.tipo = BOOLEAN;
        $$.es_direccion = 0;
        /*Generate code for the logical operation NOT*/
        no(yyout, $2.es_direccion, etiqueta++);
        //fprintf(yyout, ";R79:\t<exp> ::= ! <exp>\n");
    }
    | TOK_IDENTIFICADOR             
    {
        DATA *obj = symbol_search(table, $1.lexema);
        /* Check that the identifier exists in the symbol table */
        if (!obj){
            fprintf(stderr, "****Semantic Error in line %d: Accessing non-declared variable (%s).\n", line, $1.lexema);
            return ERROR;
        }
        /* Check if it is a function */
        if (obj->category == FUNCION){
            fprintf(stderr, "****Semantic Error in line %d: Using function (%s) as variable.\n", line, $1.lexema);
            return ERROR;
        }
        /* Check if it is a vector */
        if (obj->clase == VECTOR){
            fprintf(stderr, "****Semantic Error in line %d: Using vector (%s) as variable.\n", line, $1.lexema);
            return ERROR;
        }
        /* Synthesize relevant information */
        $$.tipo = obj->type;
        $$.es_direccion = 1;
        
        if (obj->pos_param != NU){
            /* Check if it is a parameter*/
            escribirParametro(yyout, obj->pos_param, num_parametros_actual);
        }else if (obj->pos_local_var != NU){
            /* Check if it is a local variable */
            escribirVariableLocal(yyout, obj->pos_local_var);
        }
        else{
            /* The variable is global */
            escribir_operando(yyout, $1.lexema, 1);
        }

        /* If we are calling a function, turn variable into parameter value */
        if (en_explist){
            operandoEnPilaAArgumento(yyout, $$.es_direccion);
            $$.es_direccion = 0;
        }
        //fprintf(yyout, ";R80:\t<exp> ::= <identificador>\n");
    }
    | constante                 
    {
        /* Synthesize relevant information */
        $$.tipo = $1.tipo;
        $$.es_direccion = $1.es_direccion;
        //fprintf(yyout, ";R81:\t<exp> ::= <constante>\n");
    }
    | TOK_PARENTESISIZQUIERDO exp TOK_PARENTESISDERECHO         
    {
        /*Synthesize the information*/
        $$.tipo = $2.tipo;
        $$.es_direccion = $2.es_direccion;
        //fprintf(yyout, ";R82:\t<exp> ::= ( <exp> )\n");
    }
    | TOK_PARENTESISIZQUIERDO comparacion TOK_PARENTESISDERECHO 
    {
        /*Synthesize the information*/
        $$.tipo = $2.tipo;
        $$.es_direccion = $2.es_direccion;
        //fprintf(yyout, ";R83:\t<exp> ::= ( <comparacion> )\n");
    }
    | elemento_vector           
    {
        $$.tipo = $1.tipo;
        $$.es_direccion = $1.es_direccion;
        /* If we are calling a function, turn variable into parameter value */
        if (en_explist){
            operandoEnPilaAArgumento(yyout, $$.es_direccion);
            $$.es_direccion = 0;
        }
        //fprintf(yyout, ";R85:\t<exp> ::= <elemento_vector>\n");
    }
    | idf_llamada_funcion TOK_PARENTESISIZQUIERDO lista_expresiones TOK_PARENTESISDERECHO     
    {
        /* Obtain the object for the function stored in the symbol table */
        DATA *obj = symbol_search(table, $1.lexema);
        if (!obj){
            fprintf(stderr, "****Semantic Error in line %d: Accessing non-declared function (%s).\n", line, $1.lexema);
            return ERROR;
        }
        /* Check that the amount of parameters in the call is correct */
        if (num_parametros_llamada_actual != obj->n_param){
            fprintf(stderr, "****Semantic Error in line %d: Incorrect number of parameters in function call.\n", line);
            return ERROR;
        }
        /* Synthesize relevant information */
        $$.tipo = obj->type;
        $$.es_direccion=0;
        /* Deactivate flag for parameter list */
        en_explist = 0;
        /* Generate code for function call */
        llamarFuncion(yyout, $1.lexema, obj->n_param);
        //fprintf(yyout, ";R88:\t<exp> ::= <identificador> ( <lista_expresiones> )\n");
    }

idf_llamada_funcion:    TOK_IDENTIFICADOR
                        {
                            /* Search for the function name in the symbol table */
                            DATA *obj = symbol_search(table, $1.lexema);
                            if (!obj){
                                fprintf(stderr, "****Semantic Error in line %d: Accessing non-declared variable (%s).\n", line, $1.lexema);
                                return ERROR;
                            }
                            /* Check that it is indeed a function */
                            if (obj->category != FUNCION){
                                fprintf(stderr, "****Semantic Error in line %d: Using variable (%s) as function.\n", line, $1.lexema);
                                return ERROR;
                            }
                            /* Check that the call is not being made inside of another function call */
                            if (en_explist == 1){
                                fprintf(stderr, "****Semantic Error in line %d: Usage of function calls as parameters of another function call not allowed.\n", line);
                                return ERROR;
                            }
                            /* Initialize relevant variables */
                            num_parametros_llamada_actual = 0;
                            en_explist = 1;
                            /* Synthesize relevant information */
                            strcpy($$.lexema, $1.lexema);
                        }

lista_expresiones:  exp resto_lista_expresiones 
                    {
                        /* Update parameter counter */
                        num_parametros_llamada_actual++;
                        //fprintf(yyout, ";R89:\t<lista_expresiones> ::= <exp> <resto_lista_expresiones>\n");
                    }
                    | /* VACIO */
                    {
                        //fprintf(yyout, ";R90:\t<lista_expresiones> ::= \n");
                    }
                    
resto_lista_expresiones:    TOK_COMA exp resto_lista_expresiones 
                            {
                                /* Update parameter counter */
                                num_parametros_llamada_actual++;
                                //fprintf(yyout, ";R91:\t<resto_lista_expresiones> ::= , <exp> <resto_lista_expresiones>\n");
                            }
                            | /* VACIO */
                            {
                                //fprintf(yyout, ";R92:\t<resto_lista_expresiones> ::= \n");
                            }
                        
comparacion:  exp TOK_IGUAL exp         
            {
                /* Check that both types are integer */
                if ($1.tipo != INT || $3.tipo != INT){
                    fprintf(stderr, "****Semantic Error in line %d: Comparison with boolean operand.\n", line);
                    return ERROR;
                }
                /* Synthesize relevant information */
                $$.tipo = BOOLEAN;
                $$.es_direccion = 0;
                /* Generate code for the comparison */
                igual(yyout, $1.es_direccion, $3.es_direccion, etiqueta++);
                //fprintf(yyout, ";R93:\t<comparacion> ::= <exp> == <exp>\n");
            }
            | exp TOK_DISTINTO exp      
            {
                /* Check that both types are integer */
                if ($1.tipo != INT || $3.tipo != INT){
                    fprintf(stderr, "****Semantic Error in line %d: Comparison with boolean operand.\n", line);
                    return ERROR;
                }
                /* Synthesize relevant information */
                $$.tipo = BOOLEAN;
                $$.es_direccion = 0;
                /* Generate code for the comparison */
                distinto(yyout, $1.es_direccion, $3.es_direccion, etiqueta++);
                //fprintf(yyout, ";R94:\t<comparacion> ::= <exp> != <exp>\n");
            }
            | exp TOK_MENORIGUAL exp    
            {
                /* Check that both types are integer */
                if ($1.tipo != INT || $3.tipo != INT){
                    fprintf(stderr, "****Semantic Error in line %d: Comparison with boolean operand.\n", line);
                    return ERROR;
                }
                /* Synthesize relevant information */
                $$.tipo = BOOLEAN;
                $$.es_direccion = 0;
                /* Generate code for the comparison */
                menor_igual(yyout, $1.es_direccion, $3.es_direccion, etiqueta++);
                //fprintf(yyout, ";R95:\t<comparacion> ::= <exp> <= <exp>\n");
            }
            | exp TOK_MAYORIGUAL exp    
            {
                /* Check that both types are integer */
                if ($1.tipo != INT || $3.tipo != INT){
                    fprintf(stderr, "****Semantic Error in line %d: Comparison with boolean operand.\n", line);
                    return ERROR;
                }
                /* Synthesize relevant information */
                $$.tipo = BOOLEAN;
                $$.es_direccion = 0;
                /* Generate code for the comparison */
                mayor_igual(yyout, $1.es_direccion, $3.es_direccion, etiqueta++);
                //fprintf(yyout, ";R96:\t<comparacion> ::= <exp> >= <exp>\n");
            }
            | exp TOK_MENOR exp         
            {
                /* Check that both types are integer */
                if ($1.tipo != INT || $3.tipo != INT){
                    fprintf(stderr, "****Semantic Error in line %d: Comparison with boolean operand.\n", line);
                    return ERROR;
                }
                /* Synthesize relevant information */
                $$.tipo = BOOLEAN;
                $$.es_direccion = 0;
                /* Generate code for the comparison */
                menor(yyout, $1.es_direccion, $3.es_direccion, etiqueta++);
                //fprintf(yyout, ";R97:\t<comparacion> ::= <exp> < <exp>\n");
            }
            | exp TOK_MAYOR exp         
            {
                /* Check that both types are integer */
                if ($1.tipo != INT || $3.tipo != INT){
                    fprintf(stderr, "****Semantic Error in line %d: Comparison with boolean operand.\n", line);
                    return ERROR;
                }
                /* Synthesize relevant information */
                $$.tipo = BOOLEAN;
                $$.es_direccion = 0;
                /* Generate code for the comparison */
                mayor(yyout, $1.es_direccion, $3.es_direccion, etiqueta++);
                //fprintf(yyout, ";R98:\t<comparacion> ::= <exp> > <exp>\n");
            }

constante:  constante_logica  
            {
                /* Synthesize relevant information */
                $$.tipo = $1.tipo;
                $$.es_direccion = $1.es_direccion;
                //fprintf(yyout, ";R99:\t<constante> ::= <constante_logica>\n");
            }
            | constante_entera  
            {
                /* Synthesize relevant information */
                $$.tipo = $1.tipo;
                $$.es_direccion = $1.es_direccion;
                //fprintf(yyout, ";R100:\t<constante> ::= <constante_entera>\n");
            }

constante_logica:   TOK_TRUE  
                    {
                        /* Synthesize relevant information */
                        $$.tipo = BOOLEAN;
                        $$.es_direccion = 0;
                        /* Generate code to store the constant in the stack */
                        escribir_operando(yyout, "1", 0);
                        //fprintf(yyout, ";R102:\t<constante_logica> ::= true\n");
                    }
                    | TOK_FALSE 
                    {
                        /* Synthesize relevant information */
                        $$.tipo = BOOLEAN;
                        $$.es_direccion = 0;
                        /* Generate code to store the constant in the stack */
                        escribir_operando(yyout, "0", 0);
                        //fprintf(yyout, ";R103:\t<constante_logica> ::= false\n");
                    }

constante_entera:   TOK_CONSTANTE_ENTERA 
                    {
                        /* Synthesize relevant information */
                        $$.tipo = INT;
                        $$.es_direccion = 0;
                        /* Convert integer value of the constant to string */
                        char value[100];
                        sprintf(value, "%d", $1.valor_entero);
                        /* Generate code to store the constant in the stack */
                        escribir_operando(yyout, value, 0);
                        //fprintf(yyout, ";R104:\t<constante_entera> ::= TOK_CONSTANTE_ENTERA\n");
                    }

identificador:  TOK_IDENTIFICADOR
                { 
                    if (error_vector){
                        fprintf(stderr, "****Semantic Error in line %d: The size of the vector <%s> exceeds the allowed limits (1,%d)\n", line, $1.lexema, MAX_SIZE_VECTOR);
                        return ERROR;
                    }
                    DATA *dt = NULL;
                    int result;
                    if (!(table->local)){
                        /* Global Variable */
                        dt = create_global_var($1.lexema);
                    }
                    else{
                        /* Local Variable */
                        /* Check if trying to create a local vector (not allowed) */
                        if (clase_actual == VECTOR){
                            fprintf(stderr, "****Semantic Error in line %d: Local variable of non-scalar type\n", line);
                            return ERROR;
                        }
                        dt = create_local_var($1.lexema);
                        /* Update the auxiliary counters for function definitions */
                        pos_variable_local_actual++;
                        num_variables_locales_actual++;
                    }
                    if (!dt) return ERROR;
                    result = symbol_insert(table, dt);
                    if (result == DUPLICATED_DECLARATION){
                        fprintf(stderr, "****Semantic Error in line %d: Duplicated declaration\n", line);
                        return ERROR;
                    }
                    else if (result == -1){
                        fprintf(stderr, "Error inserting identifier.\n");
                        return ERROR;
                    }

                    /* If the variable is global, generate code for the declaration */
                    if (!(table->local)){
                        if (clase_actual == VECTOR) declarar_variable(yyout, $1.lexema, tipo_actual, tamanio_vector_actual);
                        else declarar_variable(yyout, $1.lexema, tipo_actual, 1);
                    }
                    //fprintf(yyout, ";R108:\t<identificador> ::= TOK_IDENTIFICADOR\n");
                }

%%

int yyerror(char *s)
{
    if (flex_error == 0){
        fprintf(stderr, "****Syntactical error in [lin %d, col %d]\n", line, total_length - start_line);
    }
    
    return 0;
}

/**
 * Function: create_global_var
 * ---------------------
 * Creates the DATA structure stored in the symbol table for a global variable
 * 
 * lexema: String with the identifier
 * 
 * returns: the DATA structure created
 */
DATA *create_global_var(char *lexema){
    DATA *data = NULL;
    int size_v = NU;
    /* If the variable is a vector, use the size argument */
    if (clase_actual == VECTOR) size_v = tamanio_vector_actual;
    data = data_create(lexema, VARIABLE, tipo_actual, clase_actual, size_v, NU, NU, NU, NU);
    return data;
}

/**
 * Function: create_local_var
 * ---------------------
 * Creates the DATA structure stored in the symbol table for a local variable
 * 
 * lexema: String with the identifier
 * 
 * returns: the DATA structure created
 */
DATA *create_local_var(char *lexema){
    DATA *data = NULL;
    data = data_create(lexema, VARIABLE, tipo_actual, ESCALAR, NU, NU, NU, NU, pos_variable_local_actual);
    return data;
}

/**
 * Function: create_param
 * ---------------------
 * Creates the DATA structure stored in the symbol table for a function parameter
 * 
 * lexema: String with the identifier
 * 
 * returns: the DATA structure created
 */
DATA *create_param(char *lexema){
    DATA *data = NULL;
    data = data_create(lexema, VARIABLE, tipo_actual, ESCALAR, NU, NU, pos_parametro_actual, NU, NU);
    return data;
}

/**
 * Function: create_function
 * ---------------------
 * Creates the DATA structure stored in the symbol table for a function
 * 
 * lexema: String with the identifier
 * 
 * returns: the DATA structure created
 */
DATA *create_function(char *lexema){
    DATA *data = NULL;
    data = data_create(lexema, FUNCION, tipo_actual, NU, NU, 0, NU, 0, NU);
    return data;
}

