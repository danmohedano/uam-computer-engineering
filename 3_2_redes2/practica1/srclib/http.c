#include <unistd.h>
#include <stdlib.h>
#include <syslog.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/stat.h>
#include "../includes/picohttpparser.h"
#include "../includes/http.h"
#include "../includes/socket.h"

// Macros para debuggear
#define DEBUG 0

// Códigos de error de la función http_leer_peticion()
#define OKAY 0
#define CONEXION_CERRADA -1
#define ERROR_LECTURA -2
#define CONNECTION_CLOSE -3
#define BUFFER_OVERFLOW -4

// Definición de códigos y razones HTTP
#define OK 200
#define OK_STR "OK"
#define NO_CONTENT 204
#define NO_CONTENT_STR "No Content"
#define BAD_REQUEST 400
#define BAD_REQUEST_STR "Bad Request"
#define NOT_FOUND 404
#define NOT_FOUND_STR "Not Found"
#define METHOD_NALLOWED 405
#define METHOD_NALLOWED_STR "Method Not Allowed"
#define UNSUPPORTED_MEDIA 415
#define UNSUPPORTED_MEDIA_STR "Unsupported Media Type"
#define INTERNAL_ERROR 500
#define INTERNAL_ERROR_STR "Internal Server Error"
#define INCORRECT_VERSION 505
#define INCORRECT_VERSION_STR "HTTP Version not supported"

// Métodos implementados
#define OPTIONS 0
#define OPTIONS_STR "OPTIONS"
#define GET 1
#define GET_STR "GET"
#define POST 2
#define POST_STR "POST"
#define METHODS {"OPTIONS", "GET", "POST"}
#define N_METHODS 3

// Tipos de contenido aceptado
#define N_MEDIA_TYPE_CLASSES 8
#define MEDIA_TYPE_CLASSES {"text/plain", "text/html", "image/gif", "image/jpeg", "video/mpeg", "application/msword", "application/pdf", "script"}
#define N_MEDIA_TYPES 13
#define MEDIA_TYPES {".txt", ".html", ".htm", ".gif", ".jpeg", ".jpg", ".mpeg", ".mpg", ".doc", ".docx", ".pdf", ".py", ".php"}
#define TYPES_PER_CLASS {1, 2, 1, 2, 2, 2, 1, 2}
#define CGI 7
#define PYTHON 11
#define PHP 12

// String para la versión http del servidor
#define VERSION_STR "HTTP/1.1"

// Definiciones de tamaños
#define BUFFER_LEN 4096
#define HEADER_LEN 250
#define REASON_LEN 45 
#define PATH_LEN 200
#define PARAM_LEN 200
#define RESPONSE_LEN (BUFFER_LEN - HEADER_LEN)

extern char *server_signature;

// Estructura para guardar la información relacionada con la petición HTTP
struct http_info{
    int code;                   // Código de respuesta
    char reason_msg[REASON_LEN];// Razón
    int method_id;              // Id del método utilizado para la petición
    char path[PATH_LEN];        // Path al recurso solicitado
    int media_class;            // Clase de contenido al que pertenece el recurso
    int media_type;             // Tipo de contenido solicitado
    char parameters[PARAM_LEN]; // Parámetros proporcionados
};

void http_tratar_conexion(int socket_fd){
    int ret_leer;
    struct http_info info;

    if (socket_fd == -1) return;

    info.method_id = -1;

    // Bucle de lectura de peticiones y respuestas hasta que 
    // el cliente indique que quiere cerrar la conexión o directamente
    // la cierre.
    while(1){
        // Se lee la petición
        ret_leer = http_leer_peticion(socket_fd, &info);
        if (ret_leer == CONEXION_CERRADA){
            if (DEBUG) syslog(LOG_INFO, "Conexion cerrada por el cliente.");
            return;
        }else if (ret_leer == ERROR_LECTURA || ret_leer == BUFFER_OVERFLOW){
            syslog(LOG_ERR, "Error en la lectura de la petición.");
            return;
        }
        // Se envía la respuesta
        http_enviar_respuesta(socket_fd, info);
        // Si se ha solicitado el cierre de conexion, se cierra
        if (ret_leer == CONNECTION_CLOSE)   return;
    }
}


int http_leer_peticion(int socket_fd, struct http_info *info){
    char buffer[BUFFER_LEN];
    const char *metodo, *path;
    int ret_parseo, version;
    struct phr_header cabeceras[100];
    size_t buflen = 0, prevbuflen = 0, metodo_len, path_len, num_cabeceras, content_length = 0;
    ssize_t rret;
    int status = OKAY;

    // Bucle para leer la petición completa
    while (1) {
        rret = read(socket_fd, buffer + buflen, sizeof(buffer) - buflen);

        // Si se ha cerrado la conexión desde el otro extremo, return
        if (rret == 0) return CONEXION_CERRADA;
        if (rret < 0) return ERROR_LECTURA;

        prevbuflen = buflen;
        buflen += rret;

        // Parseo del request
        num_cabeceras = sizeof(cabeceras) / sizeof(cabeceras[0]);

        ret_parseo = phr_parse_request(buffer, buflen, &metodo, &metodo_len, &path, &path_len,
                                &version, cabeceras, &num_cabeceras, prevbuflen);
        
        if (ret_parseo > 0) break; 
        else if (ret_parseo == -1){
            // Si hay error de parseo, suponer que la petición está mal construida
            sprintf(info->reason_msg, BAD_REQUEST_STR);
            info->code = BAD_REQUEST;
            return status;
        } 

        if (buflen == sizeof(buffer)) return BUFFER_OVERFLOW;
    }

    /*----------------------------------------------------*/
    /*------- COMPROBACIÓN DE DATOS EN LA PETICIÓN -------*/
    /*----------------------------------------------------*/
    /* 1. Comprobar version HTTP                          */
    /*----------------------------------------------------*/
    if (version == 0){
        sprintf(info->reason_msg, INCORRECT_VERSION_STR);
        info->code = INCORRECT_VERSION;
        return status;
    }

    /*----------------------------------------------------*/
    /* 2. Comprobar que el método solicitado está         */
    /*    implementado                                    */
    /*----------------------------------------------------*/
    char *metodos[N_METHODS] = METHODS;
    info->method_id = -1;
    // Se busca el método en el array de métodos implementados
    for (int i = 0; i < N_METHODS; i++){
        if (!strncmp(metodo, metodos[i], metodo_len)) info->method_id = i;
    }

    if (info->method_id == -1){
        sprintf(info->reason_msg, METHOD_NALLOWED_STR);
        info->code = METHOD_NALLOWED;
        return status;
    }else if (info->method_id == OPTIONS){
        // Si el método es OPTIONS, se devuelve un código especial
        sprintf(info->reason_msg, NO_CONTENT_STR);
        info->code = NO_CONTENT;
        return status;
    }

    /*----------------------------------------------------*/
    /* 3. Comprobar cabeceras enviadas:                   */
    /*    3a. Comprobar que se ha enviado Host            */
    /*    3b. Comprobar si se ha enviado Connection: close*/
    /*    3c. Comprobar si se ha enviado Content-Length   */
    /*        (en el caso de POST para leer los args)     */
    /*----------------------------------------------------*/
    int host = 0;
    for (int i = 0; i < num_cabeceras; i++){
        if (strncmp(cabeceras[i].name, "Host", cabeceras[i].name_len) == 0){
            host = 1;
        }else if (strncmp(cabeceras[i].name, "Content-Length", cabeceras[i].name_len) == 0){
            content_length = strtol(cabeceras[i].value, (char**)NULL, 10);
        }else if (strncmp(cabeceras[i].name, "Connection", cabeceras[i].name_len) == 0 && strncmp(cabeceras[i].value, "close", cabeceras[i].value_len) == 0){
            status = CONNECTION_CLOSE;
        }
    }

    // Si la cabecera host no se envió, devolver bad request
    if (!host){
        sprintf(info->reason_msg, BAD_REQUEST_STR);
        info->code = BAD_REQUEST;
        return status;
    }

    /*----------------------------------------------------*/
    /* 4. Obtener la extensión del recurso solicitado     */
    /*----------------------------------------------------*/
    size_t extension_len = 0;
    char *extension = NULL;
    char *param_ini = NULL; // Inicio de los parametros en caso de que sea un GET

    for (char *i = (char *)path; i < path + path_len + 1; i++){
        // Se mueve por la uri hasta que se encuentra un punto
        if (extension == NULL && *i == '.'){
            extension = i;
        }else if (*i == ' ' || *i == '?'){
            // Cuando se encuentra el final de la extension o justo antes
            // de empezar a leer parámetros que se hayan concatenado a la uri
            extension_len = i - extension;
            if (*i == '?') param_ini = i + 1;
            break;
        }
    }

    // Si el recurso no tiene extension, bad request
    if (extension == NULL){
        sprintf(info->reason_msg, BAD_REQUEST_STR);
        info->code = BAD_REQUEST;
        return status;
    }

    /*----------------------------------------------------*/
    /* 5. Obtener el path real del recurso                */
    /*    (sin parametros ni el '/' inicial)              */
    /*----------------------------------------------------*/
    size_t real_path_len = extension + extension_len - path;
    strncpy(info->path, path+1, real_path_len-1);
    (info->path)[real_path_len-1] = '\0';

    /*----------------------------------------------------*/
    /* 6. Comprobar que el tipo de recurso solicitado es  */
    /*    soportado por el servidor                       */
    /*----------------------------------------------------*/
    info->media_class = -1;
    char *media_types[N_MEDIA_TYPES] = MEDIA_TYPES;
    int types_per_class[N_MEDIA_TYPE_CLASSES] = TYPES_PER_CLASS;
    int counter = 0, class = 0; 

    // Se itera por todos los tipos de recurso soportados por el servidor
    for (int i = 0; i < N_MEDIA_TYPES; i++){
        if (strncmp(extension, media_types[i], extension_len) == 0){
            // Si hay una coincidencia con una extensión, se guarda la clase y el tipo
            info->media_class = class;
            info->media_type = i;
            break;
        }
        counter++;
        if (counter == types_per_class[class]){
            // Ya hemos comprobado todas las extensiones de esta clase, pasamos a la siguiente
            counter = 0;
            class++;
        }
    }

    if (info->media_class == -1){
        // Tipo de contenido no soportado
        sprintf(info->reason_msg, UNSUPPORTED_MEDIA_STR);
        info->code = UNSUPPORTED_MEDIA;
        return status;
    }

    /*----------------------------------------------------*/
    /* 7. Comprobar que existe el recurso solicitado      */
    /*----------------------------------------------------*/
    if (access(info->path, F_OK) != 0){
        // No existe el recurso
        sprintf(info->reason_msg, NOT_FOUND_STR);
        info->code = NOT_FOUND;
        return status;
    }


    // Si el recurso solicitado existe y está todo en orden
    sprintf(info->reason_msg, OK_STR);
    info->code = OK;

    // Lectura de parámetros
    /*----------------------------------------------------*/
    /* 8. Leer la cadena de parámetros en caso de ser     */
    /*    necesario                                       */
    /*----------------------------------------------------*/
    if (info->method_id == GET){
        // Si el método es un GET y se han encontrado parámetros
        if (param_ini && (param_ini < path + path_len)) {
            size_t param_len = path_len - (param_ini - path);
            if (param_len > (PARAM_LEN - 1)){
                // Si la longitud de los parametros proporcionados es demasiado grande
                // se devuelve un bad request
                sprintf(info->reason_msg, BAD_REQUEST_STR);
                info->code = BAD_REQUEST;
                return status;
            }
            // Si todo está en orden, se copian los parámetros a la estructura
            strncpy(info->parameters, param_ini, param_len);
            info->parameters[param_len] = '\0';
        }else{
            info->parameters[0] = '\0';
        }
    }else if (info->method_id == POST){
        strncpy(info->parameters, buffer + ret_parseo, content_length);
        info->parameters[content_length] = '\0';
    }

    return status;
}

void http_enviar_respuesta(int socket_fd, struct http_info info){
    char *buffer = NULL;
    char *metodos[N_METHODS] = METHODS;
    char response[RESPONSE_LEN];
    size_t buflen = 0, filesize = 0, responselen = 0;
    FILE *fp = NULL;


    /*----------------------------------------------------*/
    /* 1. En caso de ser necesario, se ejecuta el script  */
    /*----------------------------------------------------*/
    if (info.media_class == CGI && (info.method_id == GET || info.method_id == POST) && info.code == OK){
        // Comprobamos que se hayan proporcionado parametros
        if (strlen(info.parameters) == 0){
            sprintf(info.reason_msg, BAD_REQUEST_STR);
            info.code = BAD_REQUEST;
        }
        else{
            pid_t pid;
            int child_input[2]; // Pipe para el input
            int child_output[2];// Pipe para el output

            if (pipe(child_input) || pipe(child_output)) responselen += sprintf(response, "Error ejecutando script.");
            else{
                pid = fork();
                if (pid != 0){
                    // Padre
                    // Cerrar los extremos de los pipes que no se utilizan
                    close(child_input[0]);  // Lectura del input
                    close(child_output[1]); // Escritura del output

                    // Se escriben los parametros
                    write(child_input[1], info.parameters, strlen(info.parameters));
                    close(child_input[1]);

                    wait(NULL);

                    // Leemos el output del script hasta que no se lea mas o se llene el buffer.
                    int bytes_read = 0;
                    while(responselen < (RESPONSE_LEN - 1)){
                        bytes_read = read(child_output[0], response + responselen, RESPONSE_LEN - 1 - responselen);
                        if (bytes_read == 0) break;
                        responselen += bytes_read;
                    }

                    response[responselen] = '\0';
                }else{
                    // Hijo
                    // Cerrar los extremos de los pipes que no se utilizan
                    close(child_input[1]);  // Escritura del input
                    close(child_output[0]); // Lecutra del output

                    dup2(child_input[0], STDIN_FILENO);
                    dup2(child_output[1], STDOUT_FILENO);

                    // Ejecutar el script
                    if (info.media_type == PYTHON) execlp("python", "python", info.path, (char*)NULL);
                    else if (info.media_type == PHP) execlp("php", "php", info.path, (char*)NULL);

                    exit(EXIT_SUCCESS);
                }
            }
        }
    }

    /*----------------------------------------------------*/
    /* 2. Alocar memoria para el buffer que contendrá     */
    /*    la respuesta                                      */
    /*----------------------------------------------------*/
    if (info.method_id == GET && info.code == OK && info.media_class != CGI){
        // Si el método es GET, se calcula el tamaño del fichero
        fp = fopen(info.path, "r");
        if (fp){
            // Se busca el final del archivo
            if (fseek(fp, 0, SEEK_END) == 0){
                // Se calcula el tamaño
                filesize = ftell(fp);
                if (filesize != -1){
                    buffer = (char*)malloc(sizeof(char)*(filesize + HEADER_LEN));
                    // Se vuelve a colocar el puntero al principio del archivo
                    if (fseek(fp, 0, SEEK_SET) != 0){
                        free(buffer);
                        buffer = NULL;
                    } 
                }
            }
        }
        // Si ha habido algún error en el proceso, devolver un Internal Server Error
        if (!buffer){
            info.code = INTERNAL_ERROR;
            sprintf(info.reason_msg, INTERNAL_ERROR_STR);
            buffer = (char*)malloc(BUFFER_LEN);
        }
    }else{
        buffer = (char*)malloc(sizeof(char) * BUFFER_LEN);
    }

    /*----------------------------------------------------*/
    /* 3. Se escribe la línea inicial de la respuesta     */
    /*----------------------------------------------------*/
    buflen = sprintf(buffer, "%s %d %s\r\n", VERSION_STR, info.code, info.reason_msg);

    /*----------------------------------------------------*/
    /* 4. Si la petición fue OPTIONS, se envían los       */
    /*    métodos soportados por el servidor              */
    /*----------------------------------------------------*/
    if (info.method_id == OPTIONS){
        buflen += sprintf(buffer + buflen, "Allow: ");
        for (int i = 0; i < N_METHODS; i++){
            if (i == 0){
                buflen += sprintf(buffer + buflen, "%s", metodos[i]);
            }
            else{
                buflen += sprintf(buffer + buflen, ", %s", metodos[i]);
            }
            
        }
        buflen += sprintf(buffer + buflen, "\r\n");
    }

    /*----------------------------------------------------*/
    /* 5. Cabecera Date                                   */
    /*----------------------------------------------------*/
    char date_buffer[100];
    time_t now = time(0);
    struct tm tm = *gmtime(&now);
    strftime(date_buffer, sizeof date_buffer, "%a, %d %b %Y %H:%M:%S %Z", &tm);
    buflen += sprintf(buffer + buflen, "Date: %s\r\n", date_buffer);

    /*----------------------------------------------------*/
    /* 6. Cabecera server                                 */
    /*----------------------------------------------------*/
    buflen += sprintf(buffer + buflen, "Server: %s\r\n", server_signature);

    /*----------------------------------------------------*/
    /* 7. Cabecera Content-Type (si se devuelve contenido)*/
    /*----------------------------------------------------*/
    char *media_classes[N_MEDIA_TYPE_CLASSES] = MEDIA_TYPE_CLASSES;
    if (info.media_class == CGI && (info.method_id == GET || info.method_id == POST) && info.code == OK){
        // En el caso de CGI consideramos siempre la respuesta como text/plain
        buflen += sprintf(buffer + buflen, "Content-Type: text/plain\r\n");
    } else if (info.code == OK && info.method_id == GET && info.media_class != CGI){
        buflen += sprintf(buffer + buflen, "Content-Type: %s\r\n", media_classes[info.media_class]);
    }

    /*----------------------------------------------------*/
    /* 7. Cabecera Content-Length                         */
    /*----------------------------------------------------*/
    if (info.media_class == CGI && (info.method_id == GET || info.method_id == POST) && info.code == OK){
        buflen += sprintf(buffer + buflen, "Content-Length: %ld\r\n", responselen);
    } else if (info.code == OK && info.method_id == GET && info.media_class != CGI){
        buflen += sprintf(buffer + buflen, "Content-Length: %ld\r\n", filesize);
    }else{
        buflen += sprintf(buffer + buflen, "Content-Length: 0\r\n");
    }

    /*----------------------------------------------------*/
    /* 7. Cabecera Last-Modified                          */
    /*----------------------------------------------------*/
    if (info.code == OK && info.method_id == GET && info.media_class != CGI){
        struct stat estadisticas;
        stat(info.path, &estadisticas);
        strftime(date_buffer, sizeof date_buffer, "%a, %d %b %Y %H:%M:%S %Z", localtime(&estadisticas.st_mtime));
        buflen += sprintf(buffer + buflen, "Last-Modified: %s\r\n", date_buffer);
    }

    /*----------------------------------------------------*/
    /* 8. Fin de las cabeceras                            */
    /*----------------------------------------------------*/
    buflen += sprintf(buffer + buflen, "\r\n");

    /*----------------------------------------------------*/
    /* 9. Cuerpo de la respuesta                          */
    /*----------------------------------------------------*/
    if (info.media_class == CGI && (info.method_id == GET || info.method_id == POST) && info.code == OK){
        buflen += sprintf(buffer + buflen, "%s", response);
    } else if (info.code == OK && info.method_id == GET && info.media_class != CGI){
        buflen += fread(buffer + buflen, sizeof(char), filesize, fp);   
    } 

    buffer[buflen++] = '\0';

    /*----------------------------------------------------*/
    /* 10. Enviar la respuesta                            */
    /*----------------------------------------------------*/
    socket_send(socket_fd, buffer, buflen);
    

    if (buffer) free(buffer);
    if (fp) fclose(fp);
    return;
}