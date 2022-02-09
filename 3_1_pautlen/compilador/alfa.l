%{
    #include <stdio.h>
    #include <string.h>
    #include "alfa.h"
    #include "alfa.tab.h"

    int line = 1;
    int start_line = 0;
    int total_length = 0;
    int flex_error = 0;

    // User defined functions prototypes
    void update_start_line();
    void update_length();

%}
%option noyywrap
%option nounput
%option noinput
%%

"//".* {update_length(); }
[\n]  {line++; update_length(); update_start_line();}
[ \t]+ {update_length(); }
"main" {update_length(); return TOK_MAIN;}
"int" {update_length(); return TOK_INT;}
"boolean" {update_length(); return TOK_BOOLEAN;}
"array" {update_length(); return TOK_ARRAY;}
"function" {update_length(); return TOK_FUNCTION;}
"if" {update_length(); return TOK_IF;}
"else" {update_length(); return TOK_ELSE;}
"while" {update_length(); return TOK_WHILE;}
"scanf" {update_length(); return TOK_SCANF;}
"printf" {update_length(); return TOK_PRINTF;}
"return" {update_length(); return TOK_RETURN;}

";" {update_length(); return TOK_PUNTOYCOMA;}
"," {update_length(); return TOK_COMA;}
"(" {update_length(); return TOK_PARENTESISIZQUIERDO;}
")" {update_length(); return TOK_PARENTESISDERECHO;}
"[" {update_length(); return TOK_CORCHETEIZQUIERDO;}
"]" {update_length(); return TOK_CORCHETEDERECHO;}
"{" {update_length(); return TOK_LLAVEIZQUIERDA;}
"}" {update_length(); return TOK_LLAVEDERECHA;}
"=" {update_length(); return TOK_ASIGNACION;}
"+" {update_length(); return TOK_MAS;}
"-" {update_length(); return TOK_MENOS;}
"/" {update_length(); return TOK_DIVISION;}
"*" {update_length(); return TOK_ASTERISCO;}
"&&" {update_length(); return TOK_AND;}
"||" {update_length(); return TOK_OR;}
"!" {update_length(); return TOK_NOT;}
"==" {update_length(); return TOK_IGUAL;}
"!=" {update_length(); return TOK_DISTINTO;}
"<=" {update_length(); return TOK_MENORIGUAL;}
">=" {update_length(); return TOK_MAYORIGUAL;}
"<" {update_length(); return TOK_MENOR;}
">" {update_length(); return TOK_MAYOR;}

"true" {update_length(); return TOK_TRUE;}
"false" {update_length(); return TOK_FALSE;}

[a-zA-Z][a-zA-z0-9]{100,} {fprintf(stderr, "****Error in [lin %d, col %d]: identifier too long ( %s )\n", line, total_length - start_line + 1, yytext); flex_error = 1; return TOK_ERROR;}

[a-zA-Z][a-zA-Z0-9]* {update_length(); strcpy(yylval.attributes.lexema, yytext); return TOK_IDENTIFICADOR;}
[0-9]+ {update_length(); yylval.attributes.valor_entero = atoi(yytext); return TOK_CONSTANTE_ENTERA;}

. {fprintf(stderr, "****Error in [lin %d, col %d]: symbol not allowed ( %s )\n", line, total_length - start_line + 1, yytext); flex_error = 1; return TOK_ERROR;}

%%

// User defined functions implementation

void update_start_line(){
    start_line = total_length;
}

void update_length(){
    total_length += yyleng;
}