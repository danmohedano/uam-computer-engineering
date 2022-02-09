#include "../includes/socket.h"
#include <syslog.h>
#include <errno.h>

#define MAX_PORT 65535
#define BUFFER_SIZE 1024
#define DEFAULT_MSG "HTTP/1.1 200 OK\r\n\n"

extern int errno;

int socket_ini(int type, int port, struct addrinfo **address){
    struct addrinfo config;
    int addr_ret, socket_fd;
    char port_str[6];

    // Comprobación del numero de puerto
    if(port > MAX_PORT || port < 0){
        syslog(LOG_ERR, "Error iniciando socket. Número de puerto inválido");
        return -1;
    }

    // Configuración del struct
    memset(&config, 0, sizeof config);
    config.ai_family = AF_UNSPEC;   // Elegir tanto IPv4 como IPv6
    config.ai_socktype = type;      // Tipo de socket
    config.ai_flags = AI_PASSIVE;   // Para escoger la propia IP

    // Pasar el puerto a string para poder utilizar con getaddrinfo()
    sprintf(port_str, "%d", port);

    // Realizar la configuración de la dirección (para crear el socket
    // y para su uso posterior en otras funciones)
    if ((addr_ret = getaddrinfo(NULL, port_str, &config, address)) != 0){
        syslog(LOG_ERR, "Error configurando addrinfo. %s", gai_strerror(addr_ret));
        return -1;
    }
    socket_fd = socket((*address)->ai_family, (*address)->ai_socktype, (*address)->ai_protocol);
    if (socket_fd == -1){
        syslog(LOG_ERR, "Error iniciando socket [%d] - %s", errno, strerror(errno));
    }
    return socket_fd;
}

int socket_server_ini(int type, int port, int queue_size){
    int socket_fd, y = 1;
    struct addrinfo *address;

    if (queue_size < 1){
        syslog(LOG_ERR, "Error iniciando socket. Tamaño de cola inválido");
        return -1;
    }

    // Configuramos inicialmente el socket con la información relevante
    // (mismo proceso que para el socket de cliente)
    socket_fd = socket_ini(type, port, &address);

    if (socket_fd == -1){
        return -1;
    }

    // Configuramos el socket para que pueda reutilizar el puerto (evitando errores)
    if (setsockopt(socket_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &y, sizeof(y))){ 
		syslog(LOG_ERR, "Error iniciando socket [%d] - %s", errno, strerror(errno));
		return -1; 
	}

    // Bindeamos el socket al puerto solicitado
    if (bind(socket_fd, address->ai_addr, address->ai_addrlen) != 0){
        syslog(LOG_ERR, "Error iniciando socket [%d] - %s", errno, strerror(errno));
        return -1;
    }

    // "Iniciamos" la escucha
    if(listen(socket_fd, queue_size) != 0){
        syslog(LOG_ERR, "Error iniciando socket [%d] - %s", errno, strerror(errno));
        return -1;
    }

    // Liberamos la memoria relacionada con el addrinfo
    freeaddrinfo(address);

    return socket_fd;
}


int socket_connect(int socket_fd, struct addrinfo *address){
    if (socket_fd < 0){
        fprintf(stderr, "Descriptor de fichero inválido.\n");
        return -1;
    }
    if (!address){
        fprintf(stderr, "Estructura addrinfo inválida.\n");
        return -1;
    }

    return connect(socket_fd, address->ai_addr, address->ai_addrlen);
}

int socket_accept(int socket_fd){
    struct sockaddr_storage connection_addr;
    socklen_t addr_size;
    int ret_value;

    if (socket_fd < 0){
        syslog(LOG_ERR, "Error aceptando conexión. Descriptor de socket inválido");
        return -1;
    }

    // Realizamos el accept y devolvemos el nuevo fd
    addr_size = sizeof connection_addr;
    ret_value = accept(socket_fd, (struct sockaddr *)&connection_addr, &addr_size);
    if (ret_value == -1){
        syslog(LOG_ERR, "Error aceptando conexión [%d] - %s", errno, strerror(errno));
    }
    return ret_value;
}

int socket_send(int socket_fd, char *msg, size_t len){
    if (socket_fd < 0 || msg == NULL || len < 1){
        syslog(LOG_ERR, "Error de envío.\n");
        return -1;
    }

    size_t sent = 0;
    while (sent != len){
        sent += write(socket_fd, msg + sent, len - sent);
    }

    return 0;
}

int socket_recv(int socket_fd, char *buff, size_t len){
    if (socket_fd < 0 || buff == NULL || len < 1){
        syslog(LOG_ERR, "Error de recepción.\n");
        return -1;
    }

    size_t received = 0;
    while (received != len){
        received += read(socket_fd, buff + received, len - received);
    }
    
    return 0;
}

int socket_tratar_conexion(int socket_fd){
    char buffer[BUFFER_SIZE] = {0};

    if (socket_fd < 0) return -1;

    if (socket_recv(socket_fd, buffer, BUFFER_SIZE) != 0) return -1; 
    syslog(LOG_INFO, "Mensaje recibido: %s", buffer);
    if(socket_send(socket_fd, DEFAULT_MSG, strlen(DEFAULT_MSG)) != 0) return -1; 

    return 0;
}

