#include "afnd.h"
#include "transforma.h"


void ini_afnd1(AFND * p_afnd); /*Inicializa el automata 1 ND*/
void ini_afnd2(AFND * p_afnd); /*Inicializa el automata 2 ND*/

int main(int argc, char ** argv) {
    AFND * p_afnd = NULL, * p_afd = NULL;
    int config;

    if (argc < 2){
        fprintf(stdout, "Uso del programa: ./s1_main <d> , <d>= configuración del automata ND (1 o 2) \n");
        return -1;
    }

    config = atoi(argv[1]);

    switch (config)
    {
        case 1:
            p_afnd= AFNDNuevo("afnd_test", 6, 3);
            ini_afnd1(p_afnd);
            break;
        
        case 2:
            p_afnd= AFNDNuevo("afnd_test", 3, 2);
            ini_afnd2(p_afnd);
            break;

        default:
            fprintf(stdout, "Usa una configuración válida del autómata. (1 o 2)\n");
            return -1;
            break;
    }   
    
    p_afd = AFNDTransforma(p_afnd);

    AFNDADot(p_afnd);
    AFNDADot(p_afd);
    AFNDElimina(p_afnd);
    AFNDElimina(p_afd);
    return 0;
}


void ini_afnd1(AFND * p_afnd){
    AFNDInsertaSimbolo(p_afnd,"+");
    AFNDInsertaSimbolo(p_afnd, "0");
    AFNDInsertaSimbolo(p_afnd,".");
    AFNDInsertaEstado(p_afnd, "q0",INICIAL);
    AFNDInsertaEstado(p_afnd, "q1", NORMAL);
    AFNDInsertaEstado(p_afnd, "q2", NORMAL);
    AFNDInsertaEstado(p_afnd, "q3", NORMAL);
    AFNDInsertaEstado(p_afnd, "q4", NORMAL);
    AFNDInsertaEstado(p_afnd, "q5", FINAL);
    AFNDInsertaTransicion(p_afnd, "q0", "+", "q1");
    AFNDInsertaTransicion(p_afnd, "q1", "0", "q1");
    AFNDInsertaTransicion(p_afnd, "q1", "0", "q4");
    AFNDInsertaTransicion(p_afnd, "q1", ".", "q2");
    AFNDInsertaTransicion(p_afnd, "q2", "0", "q3");
    AFNDInsertaTransicion(p_afnd, "q3", "0", "q3");
    AFNDInsertaTransicion(p_afnd, "q4", ".", "q3");
    AFNDInsertaLTransicion(p_afnd, "q0", "q1");
    AFNDInsertaLTransicion(p_afnd, "q3", "q5");
    AFNDCierraLTransicion(p_afnd);
}

void ini_afnd2(AFND * p_afnd){
    AFNDInsertaSimbolo(p_afnd,"0");
    AFNDInsertaSimbolo(p_afnd,"1");
    AFNDInsertaEstado(p_afnd,"q0",INICIAL);
    AFNDInsertaEstado(p_afnd,"q1",NORMAL);
    AFNDInsertaEstado(p_afnd,"qf",FINAL);
    AFNDInsertaTransicion(p_afnd, "q0", "0", "q0");
    AFNDInsertaTransicion(p_afnd, "q0", "1", "q0");
    AFNDInsertaTransicion(p_afnd, "q0", "0", "q1");
    AFNDInsertaTransicion(p_afnd, "q1", "1", "qf");
}