"""
    config.py

    Archivo de configuración del proyecto

    Autor: Daniel Mohedano <daniel.mohedano@estudiante.uam.es>
    Autor: Silvia Sopeña <silvia.sopenna@estudiante.uam.es>
    Fecha de creación: 02/05/2021
"""
import os

DS_HOST = 'vega.ii.uam.es' # Host del servidor DS
DS_PORT = 8000 # Puerto de escucha del servidor DS
SUPPORTED_PROTOCOLS = 'V0' # Protocolos soportados por la aplicacion

# Configuración del usuario
NICK = 'debaleba1' # Nick del usuario
PASSWORD = 'password' # Password del usuario
USER_PORT = '8080' # Puerto de escucha elegido por el usuario
USER_UDP_PORT = '5100' # Puerto de recepción de datos
FPS = 30.0
USER_IP = '127.0.0.1'

MAX_FPS = 100.0

DEBUG = True
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
