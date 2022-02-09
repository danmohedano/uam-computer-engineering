%{
#include <stdio.h>

extern int line;
extern int total_length;
extern int start_line;
extern int flex_error;

extern FILE *yyin;
extern FILE *yyout;
extern int yylex(void);

int yyerror(char *s);
%}

%union {
    char *str;
    int num;
}

/* Palabras reservadas */ 
%token <str> TOK_MAIN
%token <str> TOK_INT
%token <str> TOK_BOOLEAN
%token <str> TOK_ARRAY
%token <str> TOK_FUNCTION
%token <str> TOK_IF
%token <str> TOK_ELSE
%token <str> TOK_WHILE
%token <str> TOK_SCANF
%token <str> TOK_PRINTF
%token <str> TOK_RETURN


/* Simbolos */
%token <str> TOK_PUNTOYCOMA
%token <str> TOK_COMA
%token <str> TOK_PARENTESISIZQUIERDO
%token <str> TOK_PARENTESISDERECHO
%token <str> TOK_CORCHETEIZQUIERDO
%token <str> TOK_CORCHETEDERECHO
%token <str> TOK_LLAVEIZQUIERDA
%token <str> TOK_LLAVEDERECHA
%token <str> TOK_ASIGNACION
%token <str> TOK_MAS
%token <str> TOK_MENOS
%token <str> TOK_DIVISION
%token <str> TOK_ASTERISCO
%token <str> TOK_AND 
%token <str> TOK_OR
%token <str> TOK_NOT
%token <str> TOK_IGUAL
%token <str> TOK_DISTINTO
%token <str> TOK_MENORIGUAL
%token <str> TOK_MAYORIGUAL
%token <str> TOK_MENOR
%token <str> TOK_MAYOR


/* Identificadores  */
%token <str> TOK_IDENTIFICADOR

/* Constantes */ 

%token <num> TOK_CONSTANTE_ENTERA
%token <str> TOK_TRUE
%token <str> TOK_FALSE

/* Errores */
%token TOK_ERROR


%left TOK_OR TOK_AND TOK_NOT
%left TOK_MENOR TOK_MAYOR TOK_IGUAL TOK_DISTINTO TOK_MENORIGUAL TOK_MAYORIGUAL
%left TOK_MAS TOK_MENOS
%left TOK_ASTERISCO TOK_DIVISION

%%

programa: TOK_MAIN TOK_LLAVEIZQUIERDA declaraciones funciones sentencias TOK_LLAVEDERECHA {fprintf(yyout, ";R1:\t<programa> ::= main { <declaraciones> <funciones> <sentencias> }\n");}

declaraciones:  declaracion               {fprintf(yyout, ";R2:\t<declaraciones> ::= <declaracion>\n");}
              | declaracion declaraciones {fprintf(yyout, ";R3:\t<declaraciones> ::= <declaracion> <declaraciones>\n");}

declaracion: clase identificadores TOK_PUNTOYCOMA {fprintf(yyout, ";R4:\t<declaracion> ::= <clase> <identificadores> ;\n");}

clase:  clase_escalar   {fprintf(yyout, ";R5:\t<clase> ::= <clase_escalar>\n");}
      | clase_vector    {fprintf(yyout, ";R7:\t<clase> ::= <clase_vector>\n");}

clase_escalar:  tipo {fprintf(yyout, ";R9:\t<clase_escalar> ::= <tipo>\n");}

tipo:   TOK_INT         {fprintf(yyout, ";R10:\t<tipo> ::= int\n");}
      | TOK_BOOLEAN     {fprintf(yyout, ";R11:\t<tipo> ::= boolean\n");}

clase_vector: TOK_ARRAY tipo TOK_CORCHETEIZQUIERDO constante_entera TOK_CORCHETEDERECHO {fprintf(yyout, ";R15:\t<clase_vector> ::= array <tipo> [ <constante_entera> ]\n");}

identificadores: identificador                          {fprintf(yyout, ";R18:\t<identificadores> ::= <identificador>\n");}
              | identificador TOK_COMA identificadores  {fprintf(yyout, ";R19:\t<identificadores> ::= <identificador> , <identificadores>\n");}

funciones: funcion funciones    {fprintf(yyout, ";R20:\t<funciones> ::= <funcion> <funciones>\n");}
           |                    {fprintf(yyout, ";R21:\t<funciones> ::= \n");}

funcion: TOK_FUNCTION tipo identificador TOK_PARENTESISIZQUIERDO parametros_funcion TOK_PARENTESISDERECHO TOK_LLAVEIZQUIERDA declaraciones_funcion sentencias TOK_LLAVEDERECHA {fprintf(yyout, ";R22:\t<funcion> ::= funcion <tipo> <identificador> ( <parametros_funcion ) { <declaraciones_funcion> <sentencias> }\n");}

parametros_funcion: parametro_funcion resto_parametros_funcion {fprintf(yyout, ";R23:\t<parametros_funcion> ::= <parametro_funcion> <resto_parametros_funcion>\n");}

resto_parametros_funcion: TOK_PUNTOYCOMA parametro_funcion resto_parametros_funcion     {fprintf(yyout, ";R25:\t<resto_parametros_funcion> ::= ; <parametro_funcion> <resto_parametros_funcion>\n");}
                          |                                                             {fprintf(yyout, ";R26:\t<resto_parametros_funcion> ::= <>\n");}

parametro_funcion: tipo identificador {fprintf(yyout, ";R27:\t<parametro_funcion> ::= <tipo> <identificador>\n");}

declaraciones_funcion: declaraciones    {fprintf(yyout, ";R28:\t<declaraciones_funcion> ::= <declaraciones>\n");}
                       |                {fprintf(yyout, ";R29:\t<declaraciones_funcion> ::= <>\n");}

sentencias: sentencia                   {fprintf(yyout, ";R30:\t<sentencias> ::= <sentencia>\n");}
          | sentencia sentencias        {fprintf(yyout, ";R31:\t<sentencias> ::= <sentencia> <sentencias>\n");}

sentencia: sentencia_simple TOK_PUNTOYCOMA      {fprintf(yyout, ";R32:\t<sentencia> ::= <sentencia_simple> ;\n");}
         | bloque                               {fprintf(yyout, ";R33:\t<sentencia> ::= <bloque>\n");}

sentencia_simple: asignacion            {fprintf(yyout, ";R34:\t<sentencia_simple> ::= <asignacion>\n");}
                | lectura               {fprintf(yyout, ";R35:\t<sentencia_simple> ::= <lectura>\n");}
                | escritura             {fprintf(yyout, ";R36:\t<sentencia_simple> ::= <escritura>\n");}
                | retorno_funcion       {fprintf(yyout, ";R38:\t<sentencia_simple> ::= <retorno_funcion>\n");}
                  
bloque: condicional     {fprintf(yyout, ";R40:\t<bloque> ::= <condicional>\n");}
      | bucle           {fprintf(yyout, ";R41:\t<bloque> ::= <bucle>\n");}
        
asignacion: identificador TOK_ASIGNACION exp    {fprintf(yyout, ";R43:\t<asignacion> ::= <identificador> = <exp>\n");}
          | elemento_vector TOK_ASIGNACION exp  {fprintf(yyout, ";R44:\t<asignacion> ::= <elemento_vector> = <exp>\n");}
            
elemento_vector: identificador TOK_CORCHETEIZQUIERDO exp TOK_CORCHETEDERECHO    {fprintf(yyout, ";R48:\t<elemento_vector> ::= <identificador> [ <exp> ]\n");}

condicional: TOK_IF TOK_PARENTESISIZQUIERDO exp TOK_PARENTESISDERECHO TOK_LLAVEIZQUIERDA sentencias TOK_LLAVEDERECHA {fprintf(yyout, ";R50:\t<condicional> ::= if ( <exp> ) { <sentencias> }\n");}
           | TOK_IF TOK_PARENTESISIZQUIERDO exp TOK_PARENTESISDERECHO TOK_LLAVEIZQUIERDA sentencias TOK_LLAVEDERECHA TOK_ELSE TOK_LLAVEIZQUIERDA sentencias TOK_LLAVEDERECHA {fprintf(yyout, ";R51:\t<condicional> ::= if ( <exp> ) { <sentencias> } else { <sentencias> }\n");}

bucle: TOK_WHILE TOK_PARENTESISIZQUIERDO exp TOK_PARENTESISDERECHO TOK_CORCHETEIZQUIERDO sentencias TOK_CORCHETEDERECHO {fprintf(yyout, ";R52:\t<bucle> ::= while ( <exp> ) { <sentencias> }\n");}

lectura: TOK_SCANF identificador {fprintf(yyout, ";R54:\t<lectura> ::= scanf <identificador>\n");}

escritura: TOK_PRINTF exp {fprintf(yyout, ";R56:\t<escritura> ::= printf <exp>\n");}

retorno_funcion: TOK_RETURN exp {fprintf(yyout, ";R61:\t<retorno_funcion> ::= return <exp>\n");}

exp:  exp TOK_MAS exp           {fprintf(yyout, ";R72:\t<exp> ::= <exp> + <exp>\n");}
    | exp TOK_MENOS exp         {fprintf(yyout, ";R73:\t<exp> ::= <exp> - <exp>\n");}
    | exp TOK_DIVISION exp      {fprintf(yyout, ";R74:\t<exp> ::= <exp> / <exp>\n");}
    | exp TOK_ASTERISCO exp     {fprintf(yyout, ";R75:\t<exp> ::= <exp> * <exp>\n");}
    | TOK_MENOS exp             {fprintf(yyout, ";R76:\t<exp> ::= - <exp>\n");}
    | exp TOK_AND exp           {fprintf(yyout, ";R77:\t<exp> ::= <exp> && <exp>\n");}
    | exp TOK_OR exp            {fprintf(yyout, ";R78:\t<exp> ::= <exp> || <exp>\n");}
    | TOK_NOT exp               {fprintf(yyout, ";R79:\t<exp> ::= ! <exp>\n");}
    | identificador             {fprintf(yyout, ";R80:\t<exp> ::= <identificador>\n");}
    | constante                 {fprintf(yyout, ";R81:\t<exp> ::= <constante>\n");}
    | TOK_PARENTESISIZQUIERDO exp TOK_PARENTESISDERECHO         {fprintf(yyout, ";R82:\t( <exp> )\n");}
    | TOK_PARENTESISIZQUIERDO comparacion TOK_PARENTESISDERECHO {fprintf(yyout, ";R83:\t<exp> ::= ( <comparacion> )\n");}
    | elemento_vector           {fprintf(yyout, ";R85:\t<exp> ::= <elemento_vector>\n");}
    | identificador TOK_PARENTESISIZQUIERDO lista_expresiones TOK_PARENTESISDERECHO     {fprintf(yyout, ";R88:\t<exp> ::= <identificador> ( <lista_expresiones> )\n");}

lista_expresiones:   exp resto_lista_expresiones {fprintf(yyout, ";R89:\t<lista_expresiones> ::= <exp> <resto_lista_expresiones>\n");}
                    | {fprintf(yyout, ";R90:\t<lista_expresiones> ::= \n");}
                    
resto_lista_expresiones: TOK_COMA exp resto_lista_expresiones {fprintf(yyout, ";R91:\t<resto_lista_expresiones> ::= , <exp> <resto_lista_expresiones>\n");}
                        | {fprintf(yyout, ";R92:\t<resto_lista_expresiones> ::= \n");}
                        
comparacion:  exp TOK_IGUAL exp         {fprintf(yyout, ";R93:\t<comparacion> ::= <exp> == <exp>\n");}
            | exp TOK_DISTINTO exp      {fprintf(yyout, ";R94:\t<comparacion> ::= <exp> != <exp>\n");}
            | exp TOK_MENORIGUAL exp    {fprintf(yyout, ";R95:\t<comparacion> ::= <exp> <= <exp>\n");}
            | exp TOK_MAYORIGUAL exp    {fprintf(yyout, ";R96:\t<comparacion> ::= <exp> >= <exp>\n");}
            | exp TOK_MENOR exp         {fprintf(yyout, ";R97:\t<comparacion> ::= <exp> < <exp>\n");}
            | exp TOK_MAYOR exp         {fprintf(yyout, ";R98:\t<comparacion> ::= <exp> > <exp>\n");}

constante:    constante_logica  {fprintf(yyout, ";R99:\t<constante> ::= <constante_logica>\n");}
            | constante_entera  {fprintf(yyout, ";R100:\t<constante> ::= <constante_entera>\n");}

constante_logica:     TOK_TRUE  {fprintf(yyout, ";R102:\t<constante_logica> ::= true\n");}
                    | TOK_FALSE {fprintf(yyout, ";R103:\t<constante_logica> ::= false\n");}

constante_entera: TOK_CONSTANTE_ENTERA {fprintf(yyout, ";R104:\t<constante_entera> ::= TOK_CONSTANTE_ENTERA\n");}

identificador: TOK_IDENTIFICADOR {fprintf(yyout, ";R108:\t<identificador> ::= TOK_IDENTIFICADOR\n");}

%%
int main(int argc, char **argv)
{
    if (argc < 3){
        fprintf(stdout, "Usage: ./pruebaSintactico <input_file> <output_file>\n");
        return -1;
    }

    yyin = fopen(argv[1], "r");
    if (yyin == NULL) {
        fprintf(stderr,"ERROR: Couldn't open input file.\n");
        return -1;
    }
    yyout = fopen(argv[2], "w");
    if (yyout == NULL) {
        fprintf(stderr,"ERROR: Couldn't open output file.\n");
        return -1;
    }

    yyparse();

    fclose(yyin);
    fclose(yyout);
    return 0;
}

int yyerror(char *s)
{
    if (flex_error == 0){
        fprintf(stderr, "****Syntactical error in [lin %d, col %d]\n", line, total_length - start_line);
    }
    
    return 0;
}
