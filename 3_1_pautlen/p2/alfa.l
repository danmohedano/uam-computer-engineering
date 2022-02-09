%{
    #include <stdio.h>
    #include "tokens.h"

    int line = 1;
    int start_line = 0;
    int total_length = 0;
    void update_start_line(){
        start_line = total_length;
    }

    void update_length(){
        total_length += yyleng;
    }

%}
%option noyywrap
%option nounput
%option noinput
%%

"//".* {update_length(); }
[\n]  {line++; update_length(); update_start_line();}
[ \t]+ {update_length(); }
"main" {update_length(); fprintf(yyout, "TOK_MAIN"); return TOK_MAIN;}
"int" {update_length(); fprintf(yyout, "TOK_INT"); return TOK_INT;}
"boolean" {update_length(); fprintf(yyout, "TOK_BOOLEAN"); return TOK_BOOLEAN;}
"array" {update_length(); fprintf(yyout, "TOK_ARRAY"); return TOK_ARRAY;}
"function" {update_length(); fprintf(yyout, "TOK_FUNCTION"); return TOK_FUNCTION;}
"if" {update_length(); fprintf(yyout, "TOK_IF"); return TOK_IF;}
"else" {update_length(); fprintf(yyout, "TOK_ELSE"); return TOK_ELSE;}
"while" {update_length(); fprintf(yyout, "TOK_WHILE"); return TOK_WHILE;}
"scanf" {update_length(); fprintf(yyout, "TOK_SCANF"); return TOK_SCANF;}
"printf" {update_length(); fprintf(yyout, "TOK_PRINTF"); return TOK_PRINTF;}
"return" {update_length(); fprintf(yyout, "TOK_RETURN"); return TOK_RETURN;}

";" {update_length(); fprintf(yyout, "TOK_PUNTOYCOMA"); return TOK_PUNTOYCOMA;}
"," {update_length(); fprintf(yyout, "TOK_COMA"); return TOK_COMA;}
"(" {update_length(); fprintf(yyout, "TOK_PARENTESISIZQUIERDO"); return TOK_PARENTESISIZQUIERDO;}
")" {update_length(); fprintf(yyout, "TOK_PARENTESISDERECHO"); return TOK_PARENTESISDERECHO;}
"[" {update_length(); fprintf(yyout, "TOK_CORCHETEIZQUIERDO"); return TOK_CORCHETEIZQUIERDO;}
"]" {update_length(); fprintf(yyout, "TOK_CORCHETEDERECHO"); return TOK_CORCHETEDERECHO;}
"{" {update_length(); fprintf(yyout, "TOK_LLAVEIZQUIERDA"); return TOK_LLAVEIZQUIERDA;}
"}" {update_length(); fprintf(yyout, "TOK_LLAVEDERECHA"); return TOK_LLAVEDERECHA;}
"=" {update_length(); fprintf(yyout, "TOK_ASIGNACION"); return TOK_ASIGNACION;}
"+" {update_length(); fprintf(yyout, "TOK_MAS"); return TOK_MAS;}
"-" {update_length(); fprintf(yyout, "TOK_MENOS"); return TOK_MENOS;}
"/" {update_length(); fprintf(yyout, "TOK_DIVISION"); return TOK_DIVISION;}
"*" {update_length(); fprintf(yyout, "TOK_ASTERISCO"); return TOK_ASTERISCO;}
"&&" {update_length(); fprintf(yyout, "TOK_AND"); return TOK_AND;}
"||" {update_length(); fprintf(yyout, "TOK_OR"); return TOK_OR;}
"!" {update_length(); fprintf(yyout, "TOK_NOT"); return TOK_NOT;}
"==" {update_length(); fprintf(yyout, "TOK_IGUAL"); return TOK_IGUAL;}
"!=" {update_length(); fprintf(yyout, "TOK_DISTINTO"); return TOK_DISTINTO;}
"<=" {update_length(); fprintf(yyout, "TOK_MENORIGUAL"); return TOK_MENORIGUAL;}
">=" {update_length(); fprintf(yyout, "TOK_MAYORIGUAL"); return TOK_MAYORIGUAL;}
"<" {update_length(); fprintf(yyout, "TOK_MENOR"); return TOK_MENOR;}
">" {update_length(); fprintf(yyout, "TOK_MAYOR"); return TOK_MAYOR;}

"true" {update_length(); fprintf(yyout, "TOK_TRUE"); return TOK_TRUE;}
"false" {update_length(); fprintf(yyout, "TOK_FALSE"); return TOK_FALSE;}

[a-zA-z0-9]{101,} {fprintf(stderr, "****Error in [lin %d, col %d]: identifier too long ( %s )\n", line, total_length - start_line + 1, yytext); return 0;}
[^a-zA-Z\d\s] {fprintf(stderr, "****Error in [lin %d, col %d]: symbol not allowed ( %s )\n", line, total_length - start_line + 1, yytext); return 0;}

[a-zA-Z][a-zA-Z0-9]* {update_length(); fprintf(yyout, "TOK_IDENTIFICADOR"); return TOK_IDENTIFICADOR;}
[0-9]+ {update_length(); fprintf(yyout, "TOK_CONSTANTE_ENTERA"); return TOK_CONSTANTE_ENTERA;}


%%
#include <stdlib.h>

int main(int argc, char**argv)
{

    if (argc < 3){
        fprintf(stdout, "Usage: ./pruebaMorfo <input_file> <output_file>\n");
    }

    yyin = fopen(argv[1], "r");
    if (yyin == NULL) {
        fprintf(stderr,"ERROR: Coulnt open input file.\n");
        return -1;
    }
    yyout = fopen(argv[2], "w");
    if (yyout == NULL) {
        fprintf(stderr,"ERROR: Coulnt open output file.\n");
        return -1;
    }

    int r = 1;
    while (r != 0){
        r = yylex();
        if (r != 0){
            fprintf(yyout, " %d %s\n", r, yytext);
        }
    }

    fclose(yyout);
    fclose(yyin);
    
    return 0;
}
