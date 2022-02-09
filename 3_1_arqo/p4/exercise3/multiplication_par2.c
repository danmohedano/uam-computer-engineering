/**
 * Parallel version (Loop 2) of module to calculate the regular multiplication of matrices
 * 
 * Author:
 *  Daniel Mohedano <daniel.mohedano@estudiante.uam.es>
 *  Silvia Sopeña   <silvia.sopenna@estudiante.uam.es>
 * 
 * Date: 26/11/2020
 */ 
#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

#include "../code/arqo4.h"

void compute(float **A, float **B, float **C, int n);

int main( int argc, char *argv[])
{
	int n;
	float **a=NULL, **b=NULL, **c=NULL;
	struct timeval fin,ini;

	printf("Word size: %ld bits\n",8*sizeof(float));

	if( argc < 3 )
	{
		printf("Error: ./%s <matrix_size> <num_threads>\n", argv[0]);
		return -1;
	}
	n=atoi(argv[1]);
	omp_set_num_threads(atoi(argv[2]));
	a=generateMatrix(n);
    b=generateMatrix(n);
    c=generateEmptyMatrix(n);
	if( !a | !b | !c )
	{
		return -1;
	}


	
	gettimeofday(&ini,NULL);

	/* Main computation */
	compute(a, b, c, n);
	/* End of computation */

	gettimeofday(&fin,NULL);
	printf("Execution time: %f\n", ((fin.tv_sec*1000000+fin.tv_usec)-(ini.tv_sec*1000000+ini.tv_usec))*1.0/1000000.0);
	
	freeMatrix(a);
    freeMatrix(b);
    freeMatrix(c);
	return 0;
}


void compute(float **A, float **B, float **C, int n)
{
	int i,j,k;
    float sum;
	

    /* Multiplication */
	for(i=0;i<n;i++)
	{
		#pragma omp parallel for private(sum, k)
		for(j=0;j<n;j++)
		{   
            sum = 0;
            for (k=0;k<n;k++)
            {
                sum += A[i][k] * B[k][j];
            }
			C[i][j] = sum;
		}
	}
}
