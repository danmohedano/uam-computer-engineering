"""
    utilidad.py

    Módulo con todas las funciones de utilidad del cliente que se encargan
    de realizar las llamadas al API.

    Autor: Daniel Mohedano <daniel.mohedano@estudiante.uam.es>
    Autor: Silvia Sopeña <silvia.sopenna@estudiante.uam.es>
    Fecha de creación: 04/04/2021
"""
import cifrado
import api_requests
import os
from project_configuration import FILEDIR_PATH


def crear_identidad(nombre, email):
    """
    Función que registra una nueva identidad para el usuario

    ARGS_IN:
        nombre (str): nombre del usuario
        email (str): email del usuario
    """
    # Generar nuevas claves RSA
    print('Generando par de claves RSA de 2048 bits...', end=' ')
    public_key = cifrado.generar_claves()
    print('OK')

    # Registrar en SecureBox la nueva identidad
    response = api_requests.make_request('/users/register',
                                         {'nombre': nombre,
                                          'email': email,
                                          'publicKey': public_key})
    if response:
        print('Identidad con ID#' +
              response['userID'] + ' creada correctamente')


def buscar_identidad(cadena):
    """
    Función que busca una identidad en el servidor

    ARGS_IN:
        cadena (str): cadena a buscar (nombre o email)
    """
    print("Buscando usuario '" + cadena + " en el servidor...", end=' ')

    response = api_requests.make_request('/users/search',
                                         {'data_search': cadena})

    if response:
        print('OK')
        print('{} usuarios encontrados:'.format(len(response)))
        for i in range(len(response)):
            print('[{}] {}, {}, ID: {}'.format(i+1,
                                               response[i]['nombre'],
                                               response[i]['email'],
                                               response[i]['userID']))


def borrar_identidad(identificador):
    """
    Función que intenta eliminar un usuario a partir de su identificador

    ARGS_IN:
        identificador (str): identificador del usuario 
    """
    print('Solicitando borrado de la identidad #{}...'.format(identificador),
          end=' ')

    # Se solicita el borrado de la identidad
    response = api_requests.make_request('/users/delete',
                                         {'userID': identificador})

    if response:
        print('OK')
        print('Identidad con ID#{} borrada correctamente'.format(
            response['userID']))


def enviar_fichero(fichero, destino_id):
    """
    Función que firma un fichero dado, lo cifra con la clave pública del 
    destinatario y lo envía al servidor

    ARGS_IN:
        fichero (str): Nombre del fichero a enviar
        destino_id (str): ID del destino del fichero
    """
    print('Solicitando envio de fichero a SecureBox')
    # Se comprueba que el archivo existe
    data_cifrado = firmar_cifrar_fichero(fichero, destino_id)
    if not data_cifrado:
        return None
    # Envío del fichero
    print('-> Subiendo fichero a servidor...', end=' ')
    response = api_requests.make_request('/files/upload', 
                                         data_cifrado, 
                                         file_name=fichero)
    if response:
        print('OK')
        print('Subida de {} bytes realizada correctamente, ID del fichero: {}'.format(
            response['file_size'], response['file_id']))


def recuperar_fichero(fichero_id, origen_id):
    """
    Función que recupera un fichero del servidor de SecureBox

    ARGS_IN:
        fichero_id (str): ID del fichero a recuperar
        origen_id (str): ID del origen del fichero
    """
    # Descargar el fichero
    print('Descargando fichero de SecureBox...', end=' ')

    response, file_name = api_requests.make_request('/files/download',
                                                    {'file_id': fichero_id},
                                                    esperado_json=False)
    if not response:
        return
    print('OK')
    print('-> {} bytes descargados correctamente'.format(len(response)))

    # Descifrar el fichero
    print('-> Descifrando fichero...', end=' ')
    key_file = open(cifrado.KEY_FILE, 'rb')
    firma, msg = cifrado.descifrar_data(response, key_file.read())
    if not firma or not msg:
        return
    print('OK')

    # Recuperar clave pública del origen
    print('-> Recuperando clave pública de ID {}...'.format(origen_id), end=' ')
    response = api_requests.make_request('/users/getPublicKey',
                                         {'userID': origen_id})

    if not response:
        return
    print('OK')
    origen_public_key = response['publicKey']

    # Verificar firma
    print('-> Verificando firma...', end=' ')
    if not cifrado.verficar_firma(msg, origen_public_key, firma):
        print('Error')
        return

    print('OK')

    # Se guarda el fichero
    file_path = os.path.join(FILEDIR_PATH, file_name)
    with open(file_path, 'wb') as f:
        f.write(msg)

    print('Fichero descargado y verificado correctamente. Nombre: {}'.format(file_name))


def listar_ficheros():
    """
    Función que lista los ficheros del usuario
    """
    print("Listando los ficheros del usuario...", end=' ')

    response = api_requests.make_request('/files/list', None)

    if response:
        print('OK')
        print('{} ficheros encontrados:'.format(response['num_files']))
        for i in range(response['num_files']):
            print('[{}] {}, ID: {}'.format(i+1, response['files_list']
                  [i]['fileName'], response['files_list'][i]['fileID']))


def borrar_fichero(fichero_id):
    """
    Función que borra el fichero

    ARGS_IN:
        fichero_id (str): ID del fichero a borrar
    """
    print("Solicitando borrado del fichero #{}...".format(fichero_id), end=' ')
    response = api_requests.make_request(
        '/files/delete', {'file_id': fichero_id})

    if response:
        print('OK')
        print('Fichero con ID#{} borrado correctamente'.format(
            response['file_id']))


def firmar_fichero(fichero):
    """
    Función para firmar un fichero.

    ARGS_IN:
        fichero (str): Nombre del fichero

    ARGS_OUT:   
        bytes del fichero firmado
    """
    print('Realizando cifrado y firma de {}'.format(fichero))
    # Se comprueba que el archivo existe
    try:
        file_path = os.path.join(FILEDIR_PATH, fichero)
        f = open(file_path, 'rb')
        file_bytes = f.read()
        f.close()
    except:
        print('Error leyendo el fichero')
        return None

    # Firmado del fichero
    print('-> Firmando fichero...', end=' ')
    # Se lee la clave privada del emisor y se firman los bytes del fichero
    try:
        key_file = open(cifrado.KEY_FILE, 'rb')
        firma = cifrado.firmar_data(file_bytes, key_file.read())
        key_file.close()
        print('OK')

        return firma + file_bytes
    except:
        print('Error')
        return None


def cifrar_fichero(fichero, destino_id):
    """
    Función para cifrar un fichero

    ARGS_IN:
        fichero (str): Nombre del fichero
        destino_id (str): ID del destino del fichero

    ARGS_OUT:
        bytes del fichero cifrados
    """
    print('Realizando cifrado y firma de {}'.format(fichero))
    # Se comprueba que el archivo existe
    try:
        file_path = os.path.join(FILEDIR_PATH, fichero)
        f = open(file_path, 'rb')
        file_bytes = f.read()
        f.close()
    except:
        print('Error leyendo el fichero')
        return None

    # Recuperación de la clave pública del destinatario
    print('-> Recuperando clave pública de ID {}...'.format(destino_id), end=' ')
    response = api_requests.make_request('/users/getPublicKey',
                                         {'userID': destino_id})

    if not response:
        return None
    print('OK')
    destino_public_key = response['publicKey']

    # Cifrado del fichero
    print('-> Cifrando fichero...', end=' ')
    data_cifrado = cifrado.cifrar_data(file_bytes, destino_public_key)
    print('OK')

    return data_cifrado


def firmar_cifrar_fichero(fichero, destino_id):
    """
    Función para firmar y cifrar un fichero.

    ARGS_IN:
        fichero (str): Nombre del fichero
        destino_id (str): ID del destino del fichero

    ARGS_OUT:
        bytes del cifrado del fichero junto con su firma
    """
    # Recuperación de la clave pública del destinatario
    print('-> Recuperando clave pública de ID {}...'.format(destino_id), end=' ')
    response = api_requests.make_request('/users/getPublicKey',
                                         {'userID': destino_id})

    if not response:
        return None
    print('OK')
    destino_public_key = response['publicKey']

    # Firmado del fichero
    fichero_firmado = firmar_fichero(fichero)
    if not fichero_firmado:
        return None
    # Cifrado del fichero
    print('-> Cifrando fichero...', end=' ')
    data_cifrado = cifrado.cifrar_data(fichero_firmado, destino_public_key)
    print('OK')

    return data_cifrado