# Práctica 2 - Seguridad y Criptografía

- Daniel Mohedano <<daniel.mohedano@estudiante.uam.es>>
- Silvia Sopeña <<silvia.sopenna@estudiante.uam.es>>

Este repositorio contiene nuestra implementación de la Práctica 2 de la asignatura REDES 2.

## Cambios tras Entrega Temprana
No se modificó nada de la práctica.

## Instalación
Pre-requisitos:
- Librería [argparse](https://docs.python.org/3/library/argparse.html) de Python 3.
- Librería [PyCryptodome](https://pycryptodome.readthedocs.io/en/latest/src/installation.html) de Python 3.
- Librería [requests](https://docs.python-requests.org/en/master/) de Python 3.

Para instalarlos, se puede utilizar el comando `pip3 install -r requirements.txt`.

## Uso
La utilización del cliente de línea de comandos se puede realizar ejecutando `python3 src/securebox_client.py`.
Para el correcto funcionamiento, introducir el token de autenticación en el fichero `aux/authorization.json`.

Datos para testear:
- NIA: `358283` Token: `EC21fcAF5674bDBe` (Daniel Mohedano, daniel.mohedano@estudiante.uam.es)
- NIA: `400390` Token: `e73B5b0c4d8D1a26` (Silvia Sopeña, silvia.sopenna@estudiante.uam.es)
