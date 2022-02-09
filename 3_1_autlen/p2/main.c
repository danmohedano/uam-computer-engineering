/**
 * 02/12/2020
 * Módulo: main
 * --------------------
 * Autores:
 * - Daniel Mohedano    <daniel.mohedano@estudiante.uam.es>
 * - Silvia Sopeña      <silvia.sopenna@estudiante.uam.es>
 * -----------------------------------------------------------
 * Testea el módulo minimiza.h. Tiene cargadas distintas configuraciones
 * de autómatas de tal forma que a traves de argumentos en la consola de 
 * comandos se puede elegir que configuración testear. 
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "afnd.h"
#include "minimiza.h"

void ini_afnd1(AFND * p_afnd); /*Inicializa el automata 1*/
void ini_afnd2(AFND * p_afnd); /*Inicializa el automata 2*/
void ini_afnd3(AFND * p_afnd); /*Inicializa el automata 3*/
void ini_afnd4(AFND * p_afnd); /*Inicializa el automata 4*/

int main(int argc, char ** argv)
{
	AFND * p_afnd = NULL;
	AFND * p_afnd_min = NULL;
	int config;

	if (argc < 2){
		fprintf(stdout, "Uso del programa: ./main <d> , <d>= configuración del automata(1 o 2) \n");
        return -1;
	}

	config = atoi(argv[1]);

	switch(config)
	{
		case 1:
            p_afnd= AFNDNuevo("afnd_test", 8, 2);
            ini_afnd1(p_afnd);
            break;
        
        case 2:
            p_afnd= AFNDNuevo("afnd_test", 8, 2);
            ini_afnd2(p_afnd);
            break;

		case 3:
			p_afnd = AFNDNuevo("afnd_test", 12, 2);
			ini_afnd3(p_afnd);
			break;

		case 4:
			p_afnd = AFNDNuevo("afnd_test", 3, 2);
			ini_afnd4(p_afnd);
			break;

        default:
            fprintf(stdout, "Usa una configuración válida del autómata. (1 o 2)\n");
            return -1;
            break;
	}


	p_afnd_min = AFNDMinimiza(p_afnd);

    if (p_afnd_min == NULL) {
        AFNDElimina(p_afnd);
        return 0;
    }

	AFNDADot(p_afnd_min);
	AFNDADot(p_afnd);
	AFNDImprime(stdout,p_afnd_min);

	AFNDElimina(p_afnd);
	AFNDElimina(p_afnd_min);

	return 0;

}

void ini_afnd1(AFND * p_afnd){
	AFNDInsertaSimbolo(p_afnd,"0");
	AFNDInsertaSimbolo(p_afnd,"1");

	AFNDInsertaEstado(p_afnd,"A",INICIAL);
	AFNDInsertaEstado(p_afnd,"B",NORMAL);
	AFNDInsertaEstado(p_afnd,"C",NORMAL);
	AFNDInsertaEstado(p_afnd,"D",FINAL);
	AFNDInsertaEstado(p_afnd,"E",NORMAL);
	AFNDInsertaEstado(p_afnd,"F",NORMAL);
	AFNDInsertaEstado(p_afnd,"G",NORMAL);
	AFNDInsertaEstado(p_afnd,"H",NORMAL);


	AFNDInsertaTransicion(p_afnd, "A", "0", "B");
	AFNDInsertaTransicion(p_afnd, "A", "1", "A");
	AFNDInsertaTransicion(p_afnd, "B", "0", "A");
	AFNDInsertaTransicion(p_afnd, "B", "1", "C");
	AFNDInsertaTransicion(p_afnd, "C", "0", "D");
	AFNDInsertaTransicion(p_afnd, "C", "1", "B");
	AFNDInsertaTransicion(p_afnd, "D", "0", "D");
	AFNDInsertaTransicion(p_afnd, "D", "1", "A");
	AFNDInsertaTransicion(p_afnd, "E", "0", "D");
	AFNDInsertaTransicion(p_afnd, "E", "1", "F");
	AFNDInsertaTransicion(p_afnd, "F", "0", "G");
	AFNDInsertaTransicion(p_afnd, "F", "1", "E");
	AFNDInsertaTransicion(p_afnd, "G", "0", "F");
	AFNDInsertaTransicion(p_afnd, "G", "1", "G");
	AFNDInsertaTransicion(p_afnd, "H", "0", "G");
	AFNDInsertaTransicion(p_afnd, "H", "1", "D");
}

void ini_afnd2(AFND * p_afnd){
	AFNDInsertaSimbolo(p_afnd,"0");
	AFNDInsertaSimbolo(p_afnd,"1");

	AFNDInsertaEstado(p_afnd,"A",INICIAL);
	AFNDInsertaEstado(p_afnd,"B",NORMAL);
	AFNDInsertaEstado(p_afnd,"C",FINAL);
	AFNDInsertaEstado(p_afnd,"D",NORMAL);
	AFNDInsertaEstado(p_afnd,"E",NORMAL);
	AFNDInsertaEstado(p_afnd,"F",NORMAL);
	AFNDInsertaEstado(p_afnd,"G",NORMAL);
	AFNDInsertaEstado(p_afnd,"H",NORMAL);


	AFNDInsertaTransicion(p_afnd, "A", "0", "B");
	AFNDInsertaTransicion(p_afnd, "A", "1", "F");
	AFNDInsertaTransicion(p_afnd, "B", "0", "G");
	AFNDInsertaTransicion(p_afnd, "B", "1", "C");
	AFNDInsertaTransicion(p_afnd, "C", "0", "A");
	AFNDInsertaTransicion(p_afnd, "C", "1", "C");
	AFNDInsertaTransicion(p_afnd, "D", "0", "C");
	AFNDInsertaTransicion(p_afnd, "D", "1", "G");
	AFNDInsertaTransicion(p_afnd, "E", "0", "H");
	AFNDInsertaTransicion(p_afnd, "E", "1", "F");
	AFNDInsertaTransicion(p_afnd, "F", "0", "C");
	AFNDInsertaTransicion(p_afnd, "F", "1", "G");
	AFNDInsertaTransicion(p_afnd, "G", "0", "G");
	AFNDInsertaTransicion(p_afnd, "G", "1", "E");
	AFNDInsertaTransicion(p_afnd, "H", "0", "G");
	AFNDInsertaTransicion(p_afnd, "H", "1", "C");
}

void ini_afnd3(AFND *p_afnd){
	AFNDInsertaSimbolo(p_afnd, "0");
	AFNDInsertaSimbolo(p_afnd, "1");

	AFNDInsertaEstado(p_afnd, "q0", INICIAL_Y_FINAL);
	AFNDInsertaEstado(p_afnd, "q1", NORMAL);
	AFNDInsertaEstado(p_afnd, "q2", NORMAL);
	AFNDInsertaEstado(p_afnd, "q3", NORMAL);
	AFNDInsertaEstado(p_afnd, "q4", FINAL);
	AFNDInsertaEstado(p_afnd, "q5", NORMAL);
	AFNDInsertaEstado(p_afnd, "q6", NORMAL);
	AFNDInsertaEstado(p_afnd, "q7", NORMAL);
	AFNDInsertaEstado(p_afnd, "q8", FINAL);
	AFNDInsertaEstado(p_afnd, "q9", NORMAL);
	AFNDInsertaEstado(p_afnd, "q10", NORMAL);
	AFNDInsertaEstado(p_afnd, "q11", NORMAL);

	AFNDInsertaTransicion(p_afnd, "q0", "0", "q1");
	AFNDInsertaTransicion(p_afnd, "q0", "1", "q1");
	AFNDInsertaTransicion(p_afnd, "q1", "0", "q2");
	AFNDInsertaTransicion(p_afnd, "q1", "1", "q2");
	AFNDInsertaTransicion(p_afnd, "q2", "0", "q3");
	AFNDInsertaTransicion(p_afnd, "q2", "1", "q3");
	AFNDInsertaTransicion(p_afnd, "q3", "0", "q4");
	AFNDInsertaTransicion(p_afnd, "q3", "1", "q4");
	AFNDInsertaTransicion(p_afnd, "q4", "0", "q5");
	AFNDInsertaTransicion(p_afnd, "q4", "1", "q5");
	AFNDInsertaTransicion(p_afnd, "q5", "0", "q6");
	AFNDInsertaTransicion(p_afnd, "q5", "1", "q6");
	AFNDInsertaTransicion(p_afnd, "q6", "0", "q7");
	AFNDInsertaTransicion(p_afnd, "q6", "1", "q7");
	AFNDInsertaTransicion(p_afnd, "q7", "0", "q8");
	AFNDInsertaTransicion(p_afnd, "q7", "1", "q8");
	AFNDInsertaTransicion(p_afnd, "q8", "0", "q9");
	AFNDInsertaTransicion(p_afnd, "q8", "1", "q9");
	AFNDInsertaTransicion(p_afnd, "q9", "0", "q10");
	AFNDInsertaTransicion(p_afnd, "q9", "1", "q10");
	AFNDInsertaTransicion(p_afnd, "q10", "0", "q11");
	AFNDInsertaTransicion(p_afnd, "q10", "1", "q11");
	AFNDInsertaTransicion(p_afnd, "q11", "0", "q0");
	AFNDInsertaTransicion(p_afnd, "q11", "1", "q0");
}

void ini_afnd4(AFND *p_afnd){
	AFNDInsertaSimbolo(p_afnd, "0");
	AFNDInsertaSimbolo(p_afnd, "1");

	AFNDInsertaEstado(p_afnd, "q0", INICIAL_Y_FINAL);
	AFNDInsertaEstado(p_afnd, "q1", FINAL);
	AFNDInsertaEstado(p_afnd, "q2", NORMAL);

	AFNDInsertaTransicion(p_afnd, "q0", "0", "q1");
	AFNDInsertaTransicion(p_afnd, "q0", "1", "q2");
	AFNDInsertaTransicion(p_afnd, "q1", "0", "q1");
	AFNDInsertaTransicion(p_afnd, "q1", "1", "q2");
	AFNDInsertaTransicion(p_afnd, "q2", "0", "q0");
	AFNDInsertaTransicion(p_afnd, "q2", "1", "q2");
}