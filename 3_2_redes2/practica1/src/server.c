#include <unistd.h> 
#include <stdio.h> 
#include <stdlib.h> 
#include <sys/socket.h> 
#include <sys/types.h>
#include <sys/stat.h>
#include <netinet/in.h> 
#include <string.h> 
#include <signal.h>
#include <syslog.h>
#include <errno.h>
#include "../includes/socket.h"
#include "../includes/thread_pool.h"
#include "confuse.h"

#define DEFAULT_PORT 8080
#define DEFAULT_POOL_SIZE 10
#define DEFAULT_QUEUE_SIZE 10

extern int errno;
char *server_signature;

void do_daemon(char *root_path){
    pid_t pid_hijo, pid_nieto;

    // Hacer fork al padre
    pid_hijo = fork();
    if (pid_hijo < 0) exit(EXIT_FAILURE);
    if (pid_hijo > 0) exit(EXIT_SUCCESS); // Abandonar proceso padre

    if (setsid() < 0) exit(EXIT_FAILURE);

    signal(SIGCHLD, SIG_IGN);
    signal(SIGHUP, SIG_IGN);

    // Hacer fork al hijo
    pid_nieto = fork();
    if (pid_nieto < 0) exit(EXIT_FAILURE);
    if (pid_nieto > 0) exit(EXIT_SUCCESS); // Abandonar proceso hijo

    // El proceso nieto se convierte en el daemon
    umask(0);
    setlogmask(LOG_UPTO(LOG_INFO));
    openlog("SERVER-LOG: ", LOG_CONS | LOG_PID | LOG_NDELAY, LOG_DAEMON);
    syslog(LOG_ERR, "Iniciando servidor.");

    if ((chdir(root_path)) < 0){
        syslog(LOG_ERR, "Error cambiando el directorio de trabajo.");
        exit(EXIT_FAILURE);
    }

    syslog(LOG_INFO, "Cerrando descriptores de fichero estandar.");
    close(STDIN_FILENO);
    close(STDOUT_FILENO);
    close(STDERR_FILENO);
    return;
}


// Manejador vacío para el sigsuspend del servidor
void manejador_SIGINT(int sig){

}

int main(int argc, char const *argv[]) 
{ 
	int server_fd; 
    struct sigaction act; 
    sigset_t mascara, old_mascara;
    struct thread_pool *pool = NULL;

    static char *root = NULL;
    static long int max_clients = DEFAULT_POOL_SIZE, port = DEFAULT_PORT, queue_size = DEFAULT_QUEUE_SIZE;

    cfg_opt_t opts[] = {
        CFG_SIMPLE_STR("server_root", &root),
        CFG_SIMPLE_INT("max_clients", &max_clients),
        CFG_SIMPLE_INT("max_queue", &queue_size),
        CFG_SIMPLE_INT("listen_port", &port),
        CFG_SIMPLE_STR("server_signature", &server_signature),
        CFG_END()
    };

    cfg_t *cfg;

    // Configuración del servidor
    cfg = cfg_init(opts, 0);
    if (cfg_parse(cfg, "server.conf") == CFG_PARSE_ERROR){
        if (cfg) cfg_free(cfg);
        printf("Error leyendo archivo de configuración.\n");
        return EXIT_FAILURE;
    }

    printf("server_root: %s\n", root);
    printf("max_clients: %ld\n", max_clients);
    printf("max_queue: %ld\n", queue_size);
    printf("listen_port: %ld\n", port);
    printf("server_signature: %s\n", server_signature);


    cfg_free(cfg);

    // Crear daemon
    do_daemon(root);

    //Configuración de máscara
    act.sa_handler = manejador_SIGINT;
    sigemptyset(&(act.sa_mask));
    act.sa_flags = 0;

    //Configuración de máscara para hilos
    sigemptyset(&mascara);
    sigaddset(&mascara, SIGINT);
    pthread_sigmask(SIG_BLOCK, &mascara, &old_mascara);

    if (sigaction(SIGINT, &act, NULL) < 0){
        free(root);
        free(server_signature);
        syslog(LOG_ERR, "Error [%d] - %s", errno, strerror(errno));
        return EXIT_FAILURE;
    }

    // Inicialización del socket
    server_fd = socket_server_ini(SOCK_STREAM, (int)port, (int)queue_size);
    if (server_fd == -1){
        free(root);
        free(server_signature);
        syslog(LOG_ERR, "Error configurando socket de servidor.");
        return EXIT_FAILURE;
    }

    pool = thread_pool_ini((int)max_clients, &server_fd);
    if (pool == NULL){
        free(root);
        free(server_signature);
        close(server_fd);
        return EXIT_FAILURE;
    }
    syslog(LOG_INFO, "Servidor iniciado en puerto %d con %d threads. A la espera de conexiones.", (int)port, (int)max_clients);

    // Espera a recibir la señal SIGINT que corta el proceso
    sigsuspend(&old_mascara);

    syslog(LOG_INFO, "Recibida señal. Esperando a finalizar servidor.");

    thread_pool_cancel(pool);

    syslog(LOG_INFO, "Pool de threads cancelada. Cerrando proceso.");
	
    close(server_fd);
    free(root);
    free(server_signature);
	return EXIT_SUCCESS; 
} 
