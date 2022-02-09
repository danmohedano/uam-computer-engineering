"""
    p2p.py

    Módulo encargado de almacenar la funcionalidad relacionada con el 
    intercambio P2P de información (tanto control como datos)

    Autor: Daniel Mohedano <daniel.mohedano@estudiante.uam.es>
    Autor: Silvia Sopeña <silvia.sopenna@estudiante.uam.es>
    Fecha de creación: 16/05/2021
"""
import threading
import logging
import time
import cv2
import numpy as np
from config import DEBUG, USER_UDP_PORT
from communications import general_comms, tcp, udp
from communications.definitions import FRAME_BUFFER_SIZE, DELAY_TIME, TOLERANCE


logging.basicConfig(level=logging.DEBUG,
                            format='P3Client-%(levelname)s: %(message)s')


def accept_thread_function(con_control, connector_ds, con_data, video_client):
    """
    Función con bucle asignada a un thread para escuchar posibles conexiones
    por llamadas
    
    ARGS_IN: 
        con_control (obj tcp.Connector_Control): estructura de control
        connector_ds (obj Connector_DS): conexión con el DS
        con_data (obj udp.Connector_Data): estructura de intercambio de datos
        video_client (obj VideoClient): video client
    """
    control_thread = None
    try:
        while True:
            conn, addr = con_control.listener.accept()
            if DEBUG:
                logging.debug('Conexion establecida con ' + str(addr))

            data = general_comms.recibir(conn, 1024).decode('utf-8')
            if con_control.active_call or con_data.sender:
                # Si se está en una llamada
                if 'CALLING' == data.split(' ')[0]:
                    # Se genera un socket auxiliar y se indica BUSY
                    caller_data = connector_ds.query(data.split(' ')[1])
                    aux_socket = tcp.new_socket(caller_data['ip'], int(caller_data['port']))
                    con_control.command_busy(aux_socket)
                    aux_socket.close()
                    conn.close()
                elif 'CALL_ACCEPTED' == data.split(' ')[0]:
                    # Si la persona ha aceptado nuestra llamada
                    # Se crean los socket UDP
                    con_data.connect(int(USER_UDP_PORT), addr[0], int(data.split(' ')[2]))

                    # Se lanza el thread de escucha (CONTROL)
                    control_thread = threading.Thread(target=control_call_thread_function, 
                                                      args=(conn, con_control, con_data, video_client, ))
                    control_thread.start()

                    # Se lanza el thread de escucha (DATA)
                    data_thread = threading.Thread(target=receive_frame_thread_function,
                                                    args=(con_data, video_client))
                    data_thread.start()

                elif 'CALL_BUSY' == data.split(' ')[0] or 'CALL_DENIED' == data.split(' ')[0]:
                    if 'CALL_DENIED' == data.split(' ')[0]:
                        video_client.app.infoBox('Información', 'La llamada fue rechazada')
                    else:
                        video_client.app.infoBox('Información', 'El usuario está ocupado')
                    # Si no se acepta la llamada, se cierra el sender
                    con_control.active_call = False
                    con_control.sender.close()
                    con_control.sender = None
                    conn.close()
                else:
                    # Cualquier otro comando se ignora
                    conn.close()
            else:
                # Si no se está en una llamada
                if 'CALLING' == data.split(' ')[0]:
                    # Obtenemos la información del llamante, creamos un socket
                    # y aceptamos la llamada
                    caller_data = connector_ds.query(data.split(' ')[1])
                    if con_control.create_sender(caller_data['ip'], 
                                                 int(caller_data['port'])):
                        user_response = video_client.app.yesNoBox('Llamada entrante', 'Llamada entrante de '+caller_data['nick']+'\nDesea aceptarla?')
                        if user_response:
                            con_control.command_accept()
                            con_control.active_call = True

                            # Se crean los socket UDP
                            con_data.connect(int(USER_UDP_PORT), addr[0], int(data.split(' ')[2]))
                            
                            # Se lanza el thread de escucha (CONTROL)
                            control_thread = threading.Thread(target=control_call_thread_function, 
                                                            args=(conn, con_control, con_data, video_client, ))
                            control_thread.start()

                            # Se lanza el thread de escucha (DATA)
                            data_thread = threading.Thread(target=receive_frame_thread_function,
                                                            args=(con_data, video_client))
                            data_thread.start()
                        else:
                            con_control.command_deny()
                            con_control.sender.close()
                            con_control.sender = None
                            conn.close()
                    else:
                        logging.info('No se pudo realizar conexión con el llamante (Conexión fallida)')
                else:
                    # Cualquier otro comando se ignora
                    conn.close()

    except Exception:
        # Se espera al thread si no ha acabado
        if control_thread:
            control_thread.join()
        return


def control_call_thread_function(listening_socket, con_control, con_data, video_client):
    """
    Función que se encarga de tratar la conexión de control

    ARGS_IN:
        listening_socket (socket): socket de escucha de comandos generado
            por el accept 
        con_control (obj Connector_Control): estructura de control
        con_data (obj udp.Connector_Data): estructura de intercambio de datos
        video_client (obj VideoClient): video client
    """
    while True:
        data = general_comms.recibir(listening_socket, 1024)
        if data:
            data = data.decode('utf-8')
            
        if not data:
            break
        elif 'CALL_END' == data.split(' ')[0]:
            break
        elif 'CALL_HOLD' == data.split(' ')[0]:
            con_control.active_call = False
        elif 'CALL_RESUME' == data.split(' ')[0]:
            con_control.active_call = True

    listening_socket.close()
    con_control.active_call = False
    con_control.sender.close()
    con_control.sender = None
    con_data.disconnect()

    # Se espera a que se muestren todos los frames programados que faltan y
    # se cambia el frame al oscuro
    time.sleep(DELAY_TIME*1.5)
    video_client.black_frame()

    if DEBUG:
        logging.debug('Acabada llamada')


def receive_frame_thread_function(con_data, video_client):
    """
    Función que recibe los frames durante una llamada

    ARGS_IN:
        con_data (obj udp.Connector_Data): estructura de intercambio de datos
        video_client (obj VideoClient): video client
    """
    try:
        while con_data.listener:
            # Leer el frame
            data = con_data.listener.recv(FRAME_BUFFER_SIZE)
            # Obtener el header
            header = data.split(b'#')[:4]
            frame_ini = 0
            # Calcular la posición en la que comienza el frame
            for x in header:
                frame_ini += len(x) + 1
            frame = data[frame_ini:]

            if DEBUG:
                logging.debug('<<FRAME[{}]:TIME:{}:RES:{}:FPS:{}'.format(header[0].decode('utf-8'),
                                                                         header[1].decode('utf-8'), 
                                                                         header[2].decode('utf-8'), 
                                                                         header[3].decode('utf-8')))

            # Si el frame se puede mostrar todavía (ha llegado lo 
            # sufiencientemente pronto), se muestra
            dif = (float(header[1].decode('utf-8')) + DELAY_TIME) - time.time()
            if dif > TOLERANCE:
                # Se planifica un thread para que muestre el frame
                if DEBUG:
                    logging.debug('FRAME[{}] SCHEDULED'.format(header[0].decode('utf-8')))

                t = threading.Timer(dif, show_frame_thread_function, args=(frame, video_client, ))
                t.start()
                con_data.received_frames += 1

    except Exception:
        # Se cierra el socket desde otro hilo, causando una excepción en el 
        # recv
        return


def show_frame_thread_function(frame, video_client):
    """
    Función para mostrar frame

    ARGS_IN:
        frame (bytes): frame a mostrar
        video_client (obj VideoClient): video client
    """
    video_client.frame_big = cv2.imdecode(np.frombuffer(frame, np.uint8), 1)
    #video_client.show_frame()
