/**
 * 22/02/2021
 * Módulo: thread_pool
 * --------------------
 * Autores:
 * - Daniel Mohedano    <daniel.mohedano@estudiante.uam.es>
 * - Silvia Sopeña      <silvia.sopenna@estudiante.uam.es>
 * -----------------------------------------------------------
 * El módulo implementa la estructura de pool de hilos
 */

#ifndef THREAD_POOL_H
#define THREAD_POOL_H

#include <pthread.h>


struct thread_pool{
    pthread_t *threads;
    int num_threads;
};

/****************************************************************************
* FUNCIÓN: struct thread_pool * thread_pool_ini(int n_threads, int *socket_fd)
* ARGS_IN:  int n_threads - Número de threads de la pool.
            int *socket_fd - Puntero al descriptor de fichero del socket del
                                servidor.
* DESCRIPCIÓN:  Función que inicializa la pool de threads.
* ARGS_OUT: struct thread_pool * - la estructura creada (NULL si error).
*****************************************************************************/
struct thread_pool * thread_pool_ini(int n_threads, int *socket_fd);

/****************************************************************************
* FUNCIÓN: void * worker_function(void *socket_fd)
* ARGS_IN: void *socket_fd - Descriptor de fichero del socket.
* DESCRIPCIÓN:  Función de trabajador de los hilos (que se encargan de tratar
                peticiones).
* ARGS_OUT: NULL (aunque la función nunca acaba)
*****************************************************************************/
void * worker_function(void *socket_fd);

/****************************************************************************
* FUNCIÓN: void thread_pool_cancel(struct thread_pool *pool)
* ARGS_IN: struct thread_pool *pool - Esctructura del tipo thread_pool que se
           quiere liberar.
* DESCRIPCIÓN:  Función que cancela las estructuras thread_pool. Cancela los
                hilos y libera la memoria
* ARGS_OUT: void
*****************************************************************************/
void thread_pool_cancel(struct thread_pool *pool);

#endif 