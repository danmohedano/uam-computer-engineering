"""
    tcp.py

    Módulo encargado de manejar las comunicaciones relacionadas con TCP
    (tanto DS como comunciación de control)

    Autor: Daniel Mohedano <daniel.mohedano@estudiante.uam.es>
    Autor: Silvia Sopeña <silvia.sopenna@estudiante.uam.es>
    Fecha de creación: 14/05/2021
"""
import socket
from config import USER_UDP_PORT, NICK
from communications import general_comms


class Connector_Control:
    """
    Clase que se encarga de contener lo relacionado con la conexión de control 
    y el envío de los comandos
    """
    def __init__(self, listen_port):
        self.listener = new_listener(listen_port)
        self.sender = None
        self.active_call = False

    def create_sender(self, host, port):
        """
        Crea el socket de envío de comandos de control

        ARGS_IN:
            host (str): host al que conectar el socket
            port (int): puerto al que conectar el socket
        ARGS_OUT:
            True si se crea correctamente, False si no
        """
        self.sender = new_socket(host, port)
        return True if self.sender else False

    def command_call(self):
        """
        Envía el comando CALLING para realizar una llamada
        """
        msg = 'CALLING ' + NICK + ' ' + USER_UDP_PORT
        general_comms.enviar(self.sender, msg)

    def command_hold(self):
        """
        Envía el comando CALL_HOLD para pausar una llamada
        """
        msg = 'CALL_HOLD ' + NICK
        general_comms.enviar(self.sender, msg)

    def command_resume(self):
        """
        Envía el comando CALL_RESUME para resumir una llamada
        """
        msg = 'CALL_RESUME ' + NICK 
        general_comms.enviar(self.sender, msg)

    def command_end(self):
        """
        Envía el comando CALL_END para finalizar una llamada
        """
        msg = 'CALL_END ' + NICK 
        general_comms.enviar(self.sender, msg)
    
    def command_accept(self):
        """
        Envía el comando CALL_ACCEPTED para aceptar una llamada
        """
        msg = 'CALL_ACCEPTED ' + NICK + ' ' + USER_UDP_PORT
        general_comms.enviar(self.sender, msg)
        
    def command_deny(self):
        """
        Envía el comando CALL_DENIED para rechazar una llamada
        """
        msg = 'CALL_DENIED ' + NICK
        general_comms.enviar(self.sender, msg)

    def command_busy(self, aux_socket):
        """
        Envía el comando CALL_BUSY para indicar que ya está en una llamada

        ARGS_IN:
            aux_socket (socket): socket auxiliar para contestar con el comando
                CALL_BUSY
        """
        msg = 'CALL_BUSY ' + NICK
        general_comms.enviar(aux_socket, msg)


def new_socket(host, port):
    """
    Función de creación de un socket TCP

    ARGS_IN:
        host (str): host al que conectar el socket
        port (int): puerto al que conectar el socket
    ARGS_OUT:
        el socket creado o None si hay error
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        return s
    except Exception:
        return None


def new_listener(port):
    """
    Función de creación de un socket TCP de escucha

    ARGS_IN:
        port(int): puerto en el que escucha el socket
    ARGS_OUT:
        el socket listener
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('127.0.0.1', port))
        s.listen()
        return s
    except Exception:
        return None
