#include "../includes/thread_pool.h"
#include "../includes/socket.h"
#include "../includes/http.h"
#include <syslog.h>


struct thread_pool * thread_pool_ini(int n_threads, int *socket_fd){
    int i, j;
    struct thread_pool *pool = NULL;

    // Comprobación de errores
    if(!socket_fd || n_threads < 0){
        syslog(LOG_ERR, "Error iniciando threadpool. Argumentos inválidos");
        return NULL;
    }

    // Reservar memoria para la estructura de la pool
    pool = (struct thread_pool *)malloc(sizeof(struct thread_pool));
    if (!pool){
        syslog(LOG_ERR, "Error iniciando threadpool. Error alocando memoria");
        return NULL;
    }

    // Reservar memoria para el array de threads
    pool->num_threads = n_threads;
    pool->threads = (pthread_t *)malloc(n_threads * sizeof(pthread_t));
    if (!(pool->threads)){
        free(pool);
        syslog(LOG_ERR, "Error iniciando threadpool. Error alocando memoria");
        return NULL;
    }
    
    // Inicialización de los hilos
    for(i = 0; i < n_threads; i++){
        if(pthread_create(&(pool->threads[i]), NULL, worker_function, socket_fd) != 0){
            // Cancelar los hilos creados si hay error
            for (j = 0; j < i; j++){
                pthread_cancel(pool->threads[i]); // Se envía petición de cancel
                pthread_join(pool->threads[i], NULL); // Se espera a que acabe
            }
            free(pool->threads);
            free(pool);
            syslog(LOG_ERR, "Error iniciando threadpool. Error creando hilos");
            return NULL;
        }
    }

    return pool;
}

void * worker_function(void *socket_fd){
    int socket = *((int *)socket_fd), new_socket;
    // Deshabilitar cancel
    pthread_setcancelstate(PTHREAD_CANCEL_DISABLE, NULL);

    // Worker loop
    while(1){
        pthread_setcancelstate(PTHREAD_CANCEL_ENABLE, NULL);
        new_socket = socket_accept(socket);
        pthread_setcancelstate(PTHREAD_CANCEL_DISABLE, NULL);
        if (new_socket > 0){
            http_tratar_conexion(new_socket);
            close(new_socket);
        }
    }
    return NULL;
}

void thread_pool_cancel(struct thread_pool *pool){
    int i;
    if (!pool) return;
    if (pool->threads){
        for (i = 0; i < pool->num_threads; i++){
            // Cancelamos los hilos y esperamos a que acaben
            pthread_cancel(pool->threads[i]);
            pthread_join(pool->threads[i], NULL);
        }

        free(pool->threads);
    }
    free(pool);
}