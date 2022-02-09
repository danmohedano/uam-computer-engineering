/**
 * 20/02/2021
 * Módulo: socket
 * --------------------
 * Autores:
 * - Daniel Mohedano    <daniel.mohedano@estudiante.uam.es>
 * - Silvia Sopeña      <silvia.sopenna@estudiante.uam.es>
 * -----------------------------------------------------------
 * El módulo implementa el comportamiento genérico de los sockets
 * para automatizar su creación y uso. 
 */
#ifndef SOCKET_H
#define SOCKET_H

#include <unistd.h> 
#include <stdio.h> 
#include <sys/socket.h> 
#include <stdlib.h> 
#include <netinet/in.h> 
#include <string.h> 
#include <netdb.h>

/****************************************************************************
* FUNCIÓN: int socket_ini(int type, int port, struct addrinfo **address)
* ARGS_IN:  int type - El tipo de socket que se quiere utilizar (generalmente SOCK_STREAM) 
*           int port - El puerto al que se quiere bindear el socket de servidor
* DESCRIPCIÓN:  Crea un socket genérico configurado con la información aportada.
                Además devuelve una estructura addrinfo que se puede utilizar para,
                por ejemplo, obtener la información para realizar el connect (en el
                caso del cliente).
* ARGS_OUT: int - Descriptor de fichero del socket configurado
            struct addrinfo **address - Estructura con la información sobre 
                                        la dirección y puerto ya configuradas
*****************************************************************************/
int socket_ini(int type, int port, struct addrinfo **address);

/****************************************************************************
* FUNCIÓN: int socket_server_ini(int type, int port, int queue_size)
* ARGS_IN:  int type - El tipo de socket que se quiere utilizar (generalmente SOCK_STREAM) 
*           int port - El puerto al que se quiere bindear el socket de servidor
*           int queue_size - Tamaño de la cola de espera
* DESCRIPCIÓN:  Inicializa un socket utilizado como servidor. Se encarga de realizar
*               todas las tareas de inicialización, bindeo y listen.
* ARGS_OUT: int - Descriptor de fichero del socket configurado
*****************************************************************************/
int socket_server_ini(int type, int port, int queue_size);

/****************************************************************************
* FUNCIÓN: char *processRequest(char *request)
* ARGS_IN: int socket_fd - El descriptor de fichero del socket.
           addrinfo address - La información relacionada con la dirección  
           con la que te quieres conectar.
* DESCRIPCIÓN:  Función para establecer conexión con el socket indicado a través
                de la dirección proporcionada.
* ARGS_OUT: int - Código de retorno (-1 si error, 0 si ok)
*****************************************************************************/
int socket_connect(int socket_fd, struct addrinfo *address);

/****************************************************************************
* FUNCIÓN: int socket_accept(int socket_fd);
* ARGS_IN: int socket_fd - El descriptor de fichero del socket.
* DESCRIPCIÓN: Acepta un intento de conexión en el socket indicado.
* ARGS_OUT: int -   Descriptor de fichero para el nuevo socket generado 
                    en la conexión
*****************************************************************************/
int socket_accept(int socket_fd);

/****************************************************************************
* FUNCIÓN: int socket_send(int socket_fd, char *msg, int len)
* ARGS_IN: int socket_fd - El descriptor de fichero del socket.
           char *msg - El mensaje enviado por el socket.
           int len - La longitud del mensaje.
* DESCRIPCIÓN: Función genérica para enviar la información a través de un socket.
* ARGS_OUT: int - Código de retorno (-1 si error, 0 si ok)
*****************************************************************************/
int socket_send(int socket_fd, char *msg, size_t len);

/****************************************************************************
* FUNCIÓN: int socket_recv(int socket_fd, char *buff, int len)
* ARGS_IN: int socket_fd - El descriptor de fichero del socket.
           char *buff - El buffer donde se guarda la información recibida.
           int len - La longitud del buffer.
* DESCRIPCIÓN:  Función genérica para recibir información en un buffer a través
                de un socket determinado.
* ARGS_OUT: int - Código de retorno (-1 si error, 0 si ok)
*****************************************************************************/
int socket_recv(int socket_fd, char *buff, size_t len);

/****************************************************************************
* FUNCIÓN: int socket_tratar_peticion(int socket_fd)
* ARGS_IN: int socket_fd - El descriptor de fichero del socket.
* DESCRIPCIÓN:  Función genérica para tratar una conexion
* ARGS_OUT: int - Código de retorno (-1 si error, 0 si ok)
*****************************************************************************/
int socket_tratar_conexion(int socket_fd);

#endif