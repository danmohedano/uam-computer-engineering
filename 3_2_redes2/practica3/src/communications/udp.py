"""
    udp.py

    Módulo encargado de manejar las comunicaciones relacionadas con UDP
    (intercambio de datos)

    Autor: Daniel Mohedano <daniel.mohedano@estudiante.uam.es>
    Autor: Silvia Sopeña <silvia.sopenna@estudiante.uam.es>
    Fecha de creación: 14/05/2021
"""
import socket
import time


class Connector_Data:
    """
    Clase que se encarga de contener lo relacionado con la comunicación de datos
    P2P (los sockets UDP que transmiten los frames de video)
    """
    def __init__(self):
        self.sender = None      # Envía los datos
        self.listener = None    # Recibe los datos
        self.dst_address = None # Dirección destino del usuario
        self.frame_count = 0    # Cantidad de frames enviados
        self.init_time = None   # Tiempo de inicio de la llamada
        self.received_frames = 0# Frames recibidos
    
    def connect(self, listen_port, dst_host, dst_port):
        """
        Se encarga de crear los sockets necesarios para la conexión con otro 
        usuario

        ARGS_IN:
            listen_port (int): puerto en el que escuchar con el socket listener
            dst_host (str): ip/host destino de los frames
            dst_port (int): puerto destino de los frames
        """
        self.sender = new_socket()
        self.listener = new_listener(listen_port)
        self.dst_address = (dst_host, dst_port)
        self.frame_count = 0
        self.init_time = time.time()
        self.received_frames = 0

    def disconnect(self):
        """
        Función para cerrar los sockets UDP y resetear los valores
        """
        if self.sender:
            self.sender.close()
            self.sender = None
        if self.listener:
            self.listener.close()
            self.listener = None
        self.dst_address = None
        self.frame_count = 0
        self.init_time = None
        self.received_frames = 0

def new_socket():
    """
    Función de creación de un socket UDP

    ARGS_OUT:
        el socket creado o None si hay error
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return s
    except Exception:
        return None


def new_listener(port):
    """
    Función de creación de un socket UDP de escucha

    ARGS_IN:
        port(int): puerto en el que escucha el socket
    ARGS_OUT:
        el socket listener
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('127.0.0.1', port))
        return s 
    except Exception:
        return None