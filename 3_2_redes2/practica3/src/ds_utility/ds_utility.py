"""
    ds_utility.py

    Módulo encargado de establecer comunicaciones con el servidor de 
    descubrimiento

    Autor: Daniel Mohedano <daniel.mohedano@estudiante.uam.es>
    Autor: Silvia Sopeña <silvia.sopenna@estudiante.uam.es>
    Fecha de creación: 02/05/2021
"""
from config import DS_HOST, DS_PORT, SUPPORTED_PROTOCOLS, USER_PORT, USER_IP, DEBUG
from communications import tcp, general_comms
from .definitions import BUFFER_SIZE
import atexit
import logging


class Connector_DS:
    """
    Clase encargada de la conexión con el DS. Contiene el socket a través el 
    cual comunicarse y la funcionalidad para enviar los comandos.
    """
    def __init__(self):
        """
        Método de inicialización del conector. Crea el socket de conexion con DS
        """
        self.socket = tcp.new_socket(DS_HOST, DS_PORT)
        self.socket.settimeout(0.25)
        atexit.register(self.cleanup)
        logging.basicConfig(level=logging.DEBUG,
                            format='P3Client-%(levelname)s: %(message)s')

        if DEBUG:
            logging.debug('Conector DS creado')

    def cleanup(self):
        """
        Función de limpieza para cerrar la conexión con DS
        """
        if DEBUG:
            logging.debug('Cerrando socket DS')
        self.enviar_mensaje('QUIT')
        self.socket.close()

    def enviar_mensaje(self, msg):
        """
        Envía un mensaje por la conexión establecida en el conector

        ARGS_IN:
            msg (str): mensaje a enviar
        ARGS_OUT:
            la respuesta del servidor
        """
        general_comms.enviar(self.socket, msg)
        data = general_comms.recibir(self.socket, BUFFER_SIZE)

        return data.decode('utf-8')

    def registrar(self, nick, password):
        """
        Registra al usuario en el sistema

        ARGS_IN:
            nick (str): nick del usuario
            password (str): contraseña del usuario

        ARGS_OUT:
            True si todo va bien, False si hay algún error
        """
        message = 'REGISTER ' + nick + ' ' + USER_IP + ' ' + USER_PORT + ' ' + \
                  password + ' ' + SUPPORTED_PROTOCOLS

        response = self.enviar_mensaje(message)

        return False if 'NOK' in response else True

    def query(self, nick):
        """
        Obtiene la información de un usuario a partir de su nick

        ARGS_IN:
            nick (str): nick del usuario
        ARGS_OUT:
            diccionario con la info del usuario
        """
        message = 'QUERY ' + nick
        response = self.enviar_mensaje(message)

        if 'NOK' in response:
            return None
        else:
            return {'nick': response.split(' ')[2],
                    'ip': response.split(' ')[3],
                    'port': response.split(' ')[4],
                    'protocols': response.split(' ')[5].split('#')}

    def list_users(self):
        """
        Función para obtener lista de usuarios

        ARGS_OUT:
            lista de usuarios con su info
        """
        message = 'LIST_USERS'
        general_comms.enviar(self.socket, message)
        
        response = self.socket.recv(1024)

        try:
            while True:
                response += self.socket.recv(1024)
        except Exception:
            pass

        response = response.decode('utf-8')
        if 'NOK' in response:
            return None
        else:
            user_list = response.split('#')[:-1]
            # Tratar el primer usuario ya que contiene también el OK
            user_list[0] = user_list[0].split(' ')[3:]
            for i in range(1, len(user_list)):
                user_list[i] = user_list[i].split(' ')
            return user_list