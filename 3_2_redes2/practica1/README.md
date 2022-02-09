# Práctica 1 - Servidor Web

- Daniel Mohedano <<daniel.mohedano@estudiante.uam.es>>
- Silvia Sopeña <<silvia.sopenna@estudiante.uam.es>>

Este repositorio contiene nuestra implementación de la Práctica 1 de la asignatura REDES 2.

## Cambios tras Entrega Temprana
No se modificó nada de la práctica.

## Instalación
Basta con descargar los contenidos del repositorio para poder usarlos. Una vez descargados se obtiene la siguiente estructura:
```
practica1
└───htmlfiles/www/
└───includes/
└───src/
└───srclib/
│   makefile
│   server.conf
│   README.md
```
El único pre-requisito es disponer de la librería [libconfuse](https://github.com/libconfuse/libconfuse) instalada en el sistema.

## Uso
El makefile realiza todo el proceso de compilación de forma automática. Además se han incluido algunos targets auxiliares para facilitar el uso del servidor:
- `test`: Ejecuta el servidor
- `test_valgrind`: Ejecuta el servidor usando Valgrind para comprobar pérdidas de memoria
- `logs`: Imprime en pantalla los mensajes del fichero `/var/log/syslog` relacionados con el servidor
- `clean`: Limpia los archivos objeto y librerías además de los ejecutables generados por la compilación

Dentro de `htmlfiles/www/` se encuentran todos los recursos disponibles en el servidor. La carpeta `htmlfiles/www/media/` proporcionada con la práctica no está en el repositorio por lo que habría que moverla al lugar indicado.

El servidor está programado para esperar una señal `SIGINT`, tras la cual comienza el proceso de limpieza y cierre. Por lo tanto, para terminar la ejecución del servidor basta con enviar dicha señal, por ejemplo, con `kill -SIGINT PID`.

Los argumentos aceptados en el archivo de configuración del servidor son los siguientes:
- `server_root`: Raiz del servidor desde donde acceder a sus documentos
- `max_clients`: Número máximo de clientes simultáneos aceptados (tamaño de la pool de hilos). Default = 10
- `max_queue`: Tamaño de la cola de espera. Default = 10
- `listen_port`: Puerto de escucha del servidor. Default = 8080
- `server_signature`: Firma del servidor enviada en las cabeceras HTTP

