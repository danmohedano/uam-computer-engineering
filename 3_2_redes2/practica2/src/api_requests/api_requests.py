"""
    api_requests.py

    Módulo para realizar las peticiones HTTP a un API enviando datos en
    formato JSON.

    Autor: Daniel Mohedano <daniel.mohedano@estudiante.uam.es>
    Autor: Silvia Sopeña <silvia.sopenna@estudiante.uam.es>
    Fecha de creación: 04/04/2021
"""
import requests
import json
import os
from api_requests.definitions import ROOT_URL, FILE_FORM_NAME, DEFAULT_FILENAME
from project_configuration import AUTHORIZATION_PATH


def make_request(url, args, file_name=False, esperado_json=True):
    """
    Función que realiza una petición POST a la URL proporcionada junto
    con los argumentos pasados.

    ARGS_IN:
        url (str): url a la que realizar la petición (cuelga de la
            dirección definida en definitions.ROOT_URL)
        args (dict/bytes): argumentos que se pasarán en el cuerpo de la petición
        file_name (str): nombre del fichero, en caso de hacer upload
        esperado_json (str): boolean indicando si la respuesta se espera como
            json o no (esta última solo utilizada en el caso de download)
    ARGS_OUT:
        El contenido de la respuesta. En caso de descargar un fichero, también
        el nombre de dicho fichero
    """
    response_json = None

    # Se lee el archivo authorization.json para cargar el token de autenticación
    # del usuario


    if not os.path.exists(AUTHORIZATION_PATH) or not os.path.isfile(AUTHORIZATION_PATH):
        print('No encontrado archivo de autorización con el token')
        return None

    with open(AUTHORIZATION_PATH) as f:
        data = json.load(f)
        token = data.get('token', None)

    if not token:
        print('Token no incluido en el archivo authorization.json')
        return None

    # Se construye la cabecera de autorización con el token indicado
    headers = {'Authorization': 'Bearer ' + token}

    # Se realiza la petición
    if file_name:
        r = requests.post(ROOT_URL + url, headers=headers,
                          files={FILE_FORM_NAME: (file_name, args)})
    else:
        r = requests.post(ROOT_URL + url, headers=headers, json=args)

    # Se intenta parsear el contenido de la respuesta como un JSON
    try:
        response_json = r.json()
    except:
        if esperado_json:
            print("Error en la respuesta. No devuelto contenido.")

    # Si se ha devuelto un error, se muestra
    if response_json and 'http_error_code' in response_json:
        print('\nError ' + response_json['error_code'] + ': '
            + response_json['description'])
        return None

    if esperado_json:
        return response_json
    else:
        # En el caso de estar descargando un archivo, se devuelven
        # tanto los datos del archivo como el nombre del mismo
        if 'content-disposition' in r.headers:
            return r.content, r.headers.get('content-disposition').split('"')[1]
        else:
            return r.content, DEFAULT_FILENAME
