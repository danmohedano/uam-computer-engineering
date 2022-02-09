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
#include "../includes/http.h"
#include "confuse.h"

#define PORT 8080 
#define QUEUE_SIZE 4

extern int errno;
char *server_signature;
static volatile sig_atomic_t got_signal = 0;

// Manejador vacío para el sigsuspend del servidor
void manejador_SIGINT(int sig){
    got_signal = 1;
}

int main(int argc, char const *argv[]) 
{ 
	int server_fd, accept_fd; 
    struct sigaction act; 

    static char *root = NULL;
    static long int max_clients = 0, port = 0;

    cfg_opt_t opts[] = {
        CFG_SIMPLE_STR("server_root", &root),
        CFG_SIMPLE_INT("max_clients", &max_clients),
        CFG_SIMPLE_INT("listen_port", &port),
        CFG_SIMPLE_STR("server_signature", &server_signature),
        CFG_END()
    };

    cfg_t *cfg;

    // Configuración del servidor
    cfg = cfg_init(opts, 0);
    cfg_parse(cfg, "server.conf");

    printf("server_root: %s\n", root);
    printf("max_clients: %ld\n", max_clients);
    printf("listen_port: %ld\n", port);
    printf("server_signature: %s\n", server_signature);

    cfg_free(cfg);

    // Crear daemon
    /*do_daemon(root);*/

    umask(0);
    setlogmask(LOG_UPTO(LOG_INFO));
    openlog("SERVER-LOG: ", LOG_CONS | LOG_PID | LOG_NDELAY, LOG_DAEMON);
    fprintf(stdout, "Iniciando servidor.\n");

    if ((chdir(root)) < 0){
        fprintf(stdout, "Error cambiando el directorio de trabajo.\n");
        exit(EXIT_FAILURE);
    }

    //Configuración de máscara
    act.sa_handler = manejador_SIGINT;
    sigemptyset(&(act.sa_mask));
    act.sa_flags = 0;

    if (sigaction(SIGINT, &act, NULL) < 0){
        free(root);
        free(server_signature);
        fprintf(stdout, "Error [%d] - %s\n", errno, strerror(errno));
        return EXIT_FAILURE;
    }

    // Inicialización del socket
    server_fd = socket_server_ini(SOCK_STREAM, (int)port, QUEUE_SIZE);
    if (server_fd == -1){
        free(root);
        free(server_signature);
        fprintf(stdout, "Error configurando socket de servidor.\n");
        return EXIT_FAILURE;
    }

    fprintf(stdout, "Servidor de pruebas iterativo iniciado\n");

    while (!got_signal){
        accept_fd = socket_accept(server_fd);
        if (accept_fd == -1){
            if (!got_signal){
                break;
            }
        }else{
            fprintf(stdout, "Conexión aceptada. Tratando conexión.\n");
            http_tratar_conexion(accept_fd);
            close(accept_fd);
        }
    }


    fprintf(stdout, "Recibida señal. Cerrando servidor\n");
	
    close(server_fd);
    free(root);
    free(server_signature);

	return EXIT_SUCCESS; 
} 
