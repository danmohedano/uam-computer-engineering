/**
 * 20/12/2020
 * Module: alfa
 * -----------------
 * Authors:
 * - Alejandro Benimeli <alejandro.benimeli@estudiante.uam.es>
 * - Daniel Mohedano    <daniel.mohedano@estudiante.uam.es>
 * - Silvia Sopeña      <silvia.sopenna@estudiante.uam.es>
 * -----------------------------------------------------------
 * This module manages acts as the main program of the compiler
 */
#include "alfa.h"
#include "alfa.tab.h"
#include "symbol_table.h"
#include <stdio.h>
#include <stdlib.h>

extern FILE *yyin;
extern FILE *yyout;
extern symbol_table *table;


int main(int argc, char **argv)
{
    int ret_code;

    if (argc < 3){
        fprintf(stdout, "Usage: ./alfa <input_file> <output_file>\n");
        return ERROR;
    }

    yyin = fopen(argv[1], "r");
    if (yyin == NULL) {
        fprintf(stderr,"ERROR: Couldn't open input file.\n");
        return ERROR;
    }
    yyout = fopen(argv[2], "w");
    if (yyout == NULL) {
        fprintf(stderr,"ERROR: Couldn't open output file.\n");
        fclose(yyin);
        return ERROR;
    }

    ret_code = yyparse();

    symbol_destroy(table);
    fclose(yyin);
    fclose(yyout);
    
    return ret_code;
}
