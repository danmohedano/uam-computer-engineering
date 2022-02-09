/**
 * 05/03/2021
 * Módulo: http
 * --------------------
 * Autores:
 * - Daniel Mohedano    <daniel.mohedano@estudiante.uam.es>
 * - Silvia Sopeña      <silvia.sopenna@estudiante.uam.es>
 * -----------------------------------------------------------
 * El módulo implementa una función que se encarga de procesar
 * peticiones HTTP
 */


#ifndef HTTP_H
#define HTTP_H

struct http_info;

/****************************************************************************
* FUNCIÓN: void http_tratar_conexion(int socket_fd)
* ARGS_IN: int socket_fd - El descriptor de fichero del socket.
* DESCRIPCIÓN:  Función genérica para tratar una conexion HTTP
* ARGS_OUT: void
*****************************************************************************/
void http_tratar_conexion(int socket_fd);

/****************************************************************************
* FUNCIÓN:  int http_leer_peticion(int socket_fd, struct http_info *info)
* ARGS_IN:  int socket_fd - El descriptor de fichero del socket.
            struct http_info *info - Puntero a la estructura que guarda la 
                                     información relacionada con la petición
* DESCRIPCIÓN:  Función que se encarga de recibir y procesar una petición 
                HTTP comprobando errores.
* ARGS_OUT:     0 si funcionamiento correcto
*****************************************************************************/
int http_leer_peticion(int socket_fd, struct http_info *info);

/****************************************************************************
* FUNCIÓN:  void http_enviar_respuesta(int socket_fd, struct http_info info)
* ARGS_IN:  int socket_fd - El descriptor de fichero del socket.
            struct http_info info - Estructura que guarda la 
                                    información relacionada con la petición
* DESCRIPCIÓN:  Función que se encarga de construir la respuesta a la petición 
                recibida y procesada por http_leer_peticion()
* ARGS_OUT: void
*****************************************************************************/
void http_enviar_respuesta(int socket_fd, struct http_info info);

#endif