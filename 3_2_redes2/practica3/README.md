# Práctica 3 - Multimedia

- Daniel Mohedano <<daniel.mohedano@estudiante.uam.es>>
- Silvia Sopeña <<silvia.sopenna@estudiante.uam.es>>

Este repositorio contiene nuestra implementación de la Práctica 3 de la asignatura REDES 2.

## Instalación
Para instalar las librerías de Python necesarias se puede utilizar el comando `pip install -r requirements.txt`.

## Uso
La ejecución de la aplicación se reduce a ejecutar `python3 src/practica3_client.py`.

Previamente se deben haber configurado los datos relevantes en el fichero `src/config.py` para establecer los siguientes valores:
- Nick
- Contraseña
- Puertos de escucha (tanto TCP como UDP)
- FPS de captura deseados

Se añade también una variable extra denominada `DEBUG` utilizada para mostrar información de debuggind durante la ejecución de la aplicación.