/**
 * Module to calculate the transposed multiplication of matrices
 * 
 * Author:
 *  Daniel Mohedano <daniel.mohedano@estudiante.uam.es>
 *  Silvia Sopeña   <silvia.sopenna@estudiante.uam.es>
 * 
 * Date: 26/11/2020
 */ 
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

#include "arqo3.h"

void compute(tipo **A, tipo **B, tipo **T, tipo **C, int n);

int main( int argc, char *argv[])
{
	int n;
	tipo **a=NULL, **b=NULL, **t =NULL, **c=NULL;
	struct timeval fin,ini;

	printf("Word size: %ld bits\n",8*sizeof(tipo));

	if( argc!=2 )
	{
		printf("Error: ./%s <matrix size>\n", argv[0]);
		return -1;
	}
	n=atoi(argv[1]);
	a=generateMatrix(n);
    b=generateMatrix(n);
    t=generateEmptyMatrix(n);
    c=generateEmptyMatrix(n);
	if( !a | !b | !t | !c )
	{
		return -1;
	}


	
	gettimeofday(&ini,NULL);

	/* Main computation */
	compute(a, b, t, c, n);
	/* End of computation */

	gettimeofday(&fin,NULL);
	printf("Execution time: %f\n", ((fin.tv_sec*1000000+fin.tv_usec)-(ini.tv_sec*1000000+ini.tv_usec))*1.0/1000000.0);

	freeMatrix(a);
    freeMatrix(b);
    freeMatrix(c);
    freeMatrix(t);
	return 0;
}


void compute(tipo **A, tipo **B, tipo **T, tipo **C, int n)
{
	int i,j,k;
    tipo sum;

    /* Calculate transposed */
	for(i=0;i<n;i++)
    {
        for(j=0;j<n;j++)
        {
            T[j][i] = B[i][j];
        }
    }

    /* Multiplication */
	for(i=0;i<n;i++)
	{
		for(j=0;j<n;j++)
		{   
            sum = 0;
            for (k=0;k<n;k++)
            {
                sum += A[i][k] * T[j][k];
            }
			C[i][j] = sum;
		}
	}
}