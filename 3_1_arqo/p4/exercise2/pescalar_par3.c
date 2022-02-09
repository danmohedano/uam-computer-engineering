// ----------- Arqo P4-----------------------
// pescalar_par1
// ¿Funciona correctamente?
//
#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include "../code/arqo4.h"

int main(int argc, char **argv)
{
	float *A=NULL, *B=NULL;
	long long k=0;
	unsigned long long size = 0;
	struct timeval fin,ini;
	double sum=0;

	if (argc < 3){
		printf("Usage: ./pescalar_serie size n_threads\n");
		return -1;
	}
     	
	size = strtoull(argv[1], NULL, 10);
       
	A = generateVectorOne(size);
	B = generateVectorOne(size);
	if ( !A || !B )
	{
		printf("Error when allocationg matrix\n");
		freeVector(A);
		freeVector(B);
		return -1;
	}
	
	omp_set_num_threads(atoi(argv[2]));   
	
	printf("Se han lanzado %d hilos.\n",atoi(argv[2]));

	gettimeofday(&ini,NULL);
	/* Bloque de computo */
	sum = 0;
	
    #pragma omp parallel for reduction(+:sum)
	for(k=0;k<size;k++)
	{
		sum = sum + A[k]*B[k];
	}
	/* Fin del computo */
	gettimeofday(&fin,NULL);

	printf("Resultado: %f\n",sum);
	printf("Tiempo: %f\n", ((fin.tv_sec*1000000+fin.tv_usec)-(ini.tv_sec*1000000+ini.tv_usec))*1.0/1000000.0);
	freeVector(A);
	freeVector(B);

	return 0;
}
