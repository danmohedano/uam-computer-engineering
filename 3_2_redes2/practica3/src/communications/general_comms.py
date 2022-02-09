"""
    general_comms.py

    Módulo encargado de manejar toda la utilidad general de ambos tipos 
    de conexiones (principalmente enviar y recibir datos)

    Autor: Daniel Mohedano <daniel.mohedano@estudiante.uam.es>
    Autor: Silvia Sopeña <silvia.sopenna@estudiante.uam.es>
    Fecha de creación: 14/05/2021
"""
import logging
import socket
from config import DEBUG


logging.basicConfig(level=logging.DEBUG,
                            format='P3Client-%(levelname)s: %(message)s')


def enviar(sck, msg, address=None):
    """
    Enviar un mensaje (string) a través del socket proporcionado

    ARGS_IN:
        sck (socket): socket a utilizar
        msg (str): mensaje a enviar
        address (tuple): dirección a la que enviar (necesario en UDP)
    """
    if DEBUG:
        logging.debug('SENT>>' + msg)
    enviar_bytes(sck, msg.encode(), address)


def enviar_bytes(sck, msg, address=None):
    """
    Envía un mensaje por la conexión establecida en el conector

    ARGS_IN:
        sck (socket): socket a utilizar
        msg (str): mensaje a enviar  
        address (tuple): dirección a la que enviar (necesario en UDP)
    """
    try:
        if sck.type == socket.SocketKind.SOCK_DGRAM:
            sck.sendto(msg, address)
        else:
            sck.sendall(msg)
        if DEBUG:
            logging.debug('SENT BYTES')
    except Exception:
        return


def recibir(sck, buffer_size):
    """
    Recibe el mensaje a través del socket.

    ARGS_IN:
        sck (socket): socket a utilizar
        buffer_size (int): tamaño del buffer
    ARGS_OUT:
        Los bytes recibidos
    """
    if buffer_size <= 0:
        return None

    data = sck.recv(buffer_size)

    if not data:
        return None

    if DEBUG:
        logging.debug('RECV<<' + data.decode('utf-8'))

    return data