"""
    practica3_client.py

    Cliente principal de la aplicación

    Autor: Daniel Mohedano <daniel.mohedano@estudiante.uam.es>
    Autor: Silvia Sopeña <silvia.sopenna@estudiante.uam.es>
	Autor: 
    Fecha de creación: 02/05/2021
"""
from appJar import gui
from PIL import Image, ImageTk
import numpy as np
import cv2
import os
import time
import logging
import threading
from ds_utility import Connector_DS
from communications import tcp, p2p, udp, general_comms
from config import USER_PORT, NICK, PASSWORD, DEBUG, FPS, MAX_FPS, PROJECT_ROOT


class VideoClient(object):
    def __init__(self, window_size):
        logging.basicConfig(level=logging.DEBUG,
                            format='P3Client-%(levelname)s: %(message)s')
        # Configuración de la conexión con el DS
        self.con_ds = Connector_DS()
        self.con_ds.registrar(NICK, PASSWORD)

        # Configuración del socket TCP listener
        self.con_control = tcp.Connector_Control(int(USER_PORT))
        if DEBUG:
            logging.debug('Creado Conector de Control')

        # Configuración de la estructura Connector_Data (utilizada al realizar
        # llamadas)
        self.con_data = udp.Connector_Data()

        # Configuración del thread de escucha del listener (espera a recibir
        # una llamada)
        self.listener_thread = threading.Thread(target=p2p.accept_thread_function, 
                                                args=(self.con_control, self.con_ds, self.con_data, self, ))

        # Configuración de la interfaz gráfica
        self.gui_configuration(window_size)

    def gui_configuration(self, window_size):
        """
        Función para configurar la interfaz gráfica
        ARGS_IN:
            window_size (str): resolución de la imagen i.e. "800x640"
        """
        # Creamos una variable que contenga el GUI principal
        self.app = gui("Redes2 - P2P", window_size)
        self.app.setGuiPadding(10, 10)

        # Preparación del interfaz
        self.app.addLabel("title", "Cliente Multimedia P2P - Redes2 [{}]".format(NICK))
        self.app.addImage("video", os.path.join(PROJECT_ROOT, "imgs", "base.gif"))

        # Se muestra un frame oscuro de fondo
        self.black_frame()
        # Se registra los dos eventos de captura de video y muestra de frame
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.app.setPollTime(int(1/MAX_FPS*1000))
        self.iteration_counter = 0
        self.app.registerEvent(self.capturaVideo)
        self.app.registerEvent(self.show_frame)

        # Añadir los botones
        self.app.addButtons(
            ["Llamar", "Colgar", "Pausar/Reanudar", "Listar Usuarios", "Cambiar Fuente", "Cámara", "Salir"], self.buttonsCallback)
        
        # Barra de estado
        # Debe actualizarse con información útil sobre la llamada (duración, FPS, etc...)
        self.app.addStatusbar(fields=2)

    def start(self):
        self.listener_thread.start()
        self.app.go()

    def capturaVideo(self):
        """
        Captura el frame de vídeo que mostrar como vídeo propio. Solo lo muestra
        cada cierto número de iteraciones para ajustar el framerate al deseado.
        """
        if self.iteration_counter == 0:
            # Capturamos un frame de la cámara o del vídeo
            ret, frame = self.cap.read()
            if not ret:
                # En caso de ser un vídeo, se vuelve al frame 0 cuando se acaba
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.cap.read()
            self.frame_small = cv2.resize(frame, (160, 120))

            # Si se está en una llamada, se envía el frame
            if self.con_data.sender and self.con_control.active_call:
                frame = cv2.resize(frame, (640,480))
                encode_param = [cv2.IMWRITE_JPEG_QUALITY, 50]
                result, encimg = cv2.imencode('.jpg', frame, encode_param)
                if not result:
                    logging.debug('Error al codificar frame')
                    return
                
                encimg = encimg.tobytes()
                self.con_data.frame_count += 1
                header = '{}#{}#{}#{}#'.format(self.con_data.frame_count,
                                               time.time(),
                                               '640x480',
                                               FPS)
                data = header.encode() + encimg
                general_comms.enviar_bytes(self.con_data.sender, data, self.con_data.dst_address)
        
        self.iteration_counter = (self.iteration_counter + 1) % int(MAX_FPS/FPS)
        

    # Establece la resolución de la imagen capturada
    def setImageResolution(self, resolution):
        # Se establece la resolución de captura de la webcam
        # Puede añadirse algún valor superior si la cámara lo permite
        # pero no modificar estos
        if resolution == "LOW":
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)
        elif resolution == "MEDIUM":
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        elif resolution == "HIGH":
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def black_frame(self):
        """
        Guarda el frame grande como un frame negro (utilizado para indicar
        que no se está en llamada)
        """
        aux_cap = cv2.VideoCapture(os.path.join(PROJECT_ROOT, 'imgs', 'base.gif'))
        ret, frame = aux_cap.read()
        self.frame_big = frame
        aux_cap.release()

    def show_frame(self):
        """
        Función que se encarga de mostrar el frame compuesto. 
        En caso de estar en llamada también actualiza los datos presentados de 
        FPS y duración.
        """
        frame_compuesto = self.frame_big
        frame_compuesto[0:self.frame_small.shape[0], 0:self.frame_small.shape[1]] = self.frame_small
        frame_compuesto = cv2.resize(frame_compuesto, (640, 480))
        cv2_im = cv2.cvtColor(frame_compuesto, cv2.COLOR_BGR2RGB)
        img_tk = ImageTk.PhotoImage(Image.fromarray(cv2_im))
        self.app.setImageData("video", img_tk, fmt='PhotoImage')

        self.app.clearStatusbar()
        if self.con_data.sender:
            fps = int(self.con_data.received_frames/(time.time() - self.con_data.init_time))
            self.app.setStatusbar('FPS: {}'.format(fps), 0)
            self.app.setStatusbar('Duration: {:02d}:{:02d}:{:02d}'.format(int((time.time() - self.con_data.init_time)//3600), 
                                                              int(((time.time() - self.con_data.init_time)%3600)//60), 
                                                              int((time.time() - self.con_data.init_time)%60)), 1)

    # Función que gestiona los callbacks de los botones
    def buttonsCallback(self, button):
        if button == "Salir":
            # Salimos de la aplicación
            if self.con_control.active_call or self.con_data.sender:
                # Si se está en llamada, se finaliza
                self.con_control.command_end()
                time.sleep(0.25)
            if DEBUG:
                logging.debug('Se cierra el listening socket')
            self.con_control.listener.close()
            self.listener_thread.join()
            self.cap.release()
            cv2.destroyAllWindows()
            self.app.stop()

        elif button == "Llamar":
            if self.con_control.active_call or self.con_data.sender:
                self.app.infoBox('Información', 'Ya estás en una llamada')
            else:
                # Entrada del nick del usuario a conectar
                nick = self.app.textBox("Llamar a...",
                                        "Introduce el nick del usuario a llamar")
                user_data = self.con_ds.query(nick)
                if not user_data:
                    self.app.infoBox('Información', 'No se pudo realizar la llamada. Nick incorrecto.')
                elif self.con_control.create_sender(user_data['ip'], int(user_data['port'])):
                    self.con_control.command_call()
                    self.con_control.active_call = True
                else:
                    self.app.infoBox('Información', 'No se pudo realizar la llamada (Conexión fallida)')

        elif button == "Colgar":
            if self.con_control.active_call or self.con_data.sender:
                self.con_control.command_end()
            else:
                self.app.infoBox('Información', 'No estás en una llamada')

        elif button == "Listar Usuarios":
            user_list = self.con_ds.list_users()
            user_str = 'Total de usuarios ' + str(len(user_list)) + ':\n'
            for x in user_list:
                user_str += x[0] + ', '

            self.app.infoBox('Lista de usuarios', user_str)

        elif button == "Cambiar Fuente":
            if self.con_control.active_call or self.con_data.sender:
                self.app.infoBox('Información', 'No disponible durante una llamada')
            else:
                path = self.app.openBox(title='Cambiar Fuente', dirName=PROJECT_ROOT)
                if path:
                    self.cap.release()
                    self.cap = cv2.VideoCapture(path)

        elif button == "Cámara":
            if self.con_control.active_call or self.con_data.sender:
                self.app.infoBox('Información', 'No disponible durante una llamada')
            else:
                self.cap.release()
                self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                
        elif button == "Pausar/Reanudar":
            if self.con_data.sender:
                if self.con_control.active_call:
                    self.con_control.command_hold()
                else:
                    self.con_control.command_resume()
                self.con_control.active_call = not self.con_control.active_call
            else:
                self.app.infoBox('Información', 'No disponible fuera de llamada')


if __name__ == '__main__':
    vc = VideoClient("800x600")

    # Crear aquí los threads de lectura, de recepción y,
    # en general, todo el código de inicialización que sea necesario
    # ...

    # Lanza el bucle principal del GUI
    # El control ya NO vuelve de esta función, por lo que todas las
    # acciones deberán ser gestionadas desde callbacks y threads
    vc.start()
