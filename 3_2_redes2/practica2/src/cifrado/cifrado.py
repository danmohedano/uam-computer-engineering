"""
    cifrado.py

    Módulo con todas la funcionalidad relacionada con el cifrado y firma
    de archivos.

    Autor: Daniel Mohedano <daniel.mohedano@estudiante.uam.es>
    Autor: Silvia Sopeña <silvia.sopenna@estudiante.uam.es>
    Fecha de creación: 04/04/2021
"""
from Cryptodome.PublicKey import RSA
from Cryptodome.Hash import SHA256
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Random import get_random_bytes
from cifrado.definitions import KEY_LENGTH, KEY_FILE, AES_KEY_LENGTH, IV_LENGTH


def generar_claves():
    """
    Función que genera nuevas claves (pública y privada) RSA de 2048b y las 
    guarda en el archivo keys.pem

    ARGS_OUT:
        public_key (str): Clave pública generada
    """
    # Se generan las claves
    key = RSA.generate(KEY_LENGTH)

    # Se guardan al archivo
    with open(KEY_FILE, 'wb') as f:
        f.write(key.export_key('PEM'))

    return key.public_key().export_key().decode('utf-8')


def firmar_data(data, clave):
    """
    Firma un contenido utilizando la clave proporcionada

    ARGS_IN:
        data (bytes): contenido a firmar
        clave (str): clave privada del emisor con la que firmar
    """
    # Se importa la clave RSA
    key = RSA.importKey(clave)
    # Se hashea el contenido
    h = SHA256.new(data)
    # Se devuelve el contenido firmado
    return pkcs1_15.new(key).sign(h)


def verficar_firma(data, clave, firma):
    """
    Verifica una firma digital

    ARGS_IN:
        data (bytes): contenido sin firmar
        clave (str): clave pública del emisor con la que verificar
        firma (bytes): contenido firmado
    ARGS_OUT:
        True si se verifica, False cualquier otras situación
    """
    # Se importa la clave RSA
    key = RSA.importKey(clave)
    # Se hashea el contenido
    h = SHA256.new(data)
    try:
        # Se verifica la firma
        pkcs1_15.new(key).verify(h, firma)
        return True
    except (ValueError, TypeError):
        return False


def cifrar_data(data, clave_publica):
    """
    Ciframos el data utilizando un esquema híbrido. Se usa AES256b con
    encadenamiento CBC y IV 16B y posteriormente la clave de AES con RSA

    ARGS_IN:
        data (bytes): datos a cifrar (firma + datos)
        clave_publica (str): clave pública del receptor
    ARGS_OUT:
        el mensaje cifrado
    """
    # Generamos la clave simétrica random y el IV
    clave_simetrica = get_random_bytes(AES_KEY_LENGTH)
    iv = get_random_bytes(IV_LENGTH)

    # Se cifra el data simétricamente
    cifrado_simetrico = AES.new(clave_simetrica, AES.MODE_CBC, iv=iv)
    data_cifrado = cifrado_simetrico.encrypt(pad(data, AES.block_size))

    # Se cifra la clave simétrica generada con RSA
    clave_rsa = RSA.importKey(clave_publica)
    cifrado_asimetrico = PKCS1_OAEP.new(clave_rsa)
    clave_cifrada = cifrado_asimetrico.encrypt(clave_simetrica)

    return iv + clave_cifrada + data_cifrado


def descifrar_data(data, clave_privada):
    """
    Descifra un mensaje cifrado con la anterior función

    ARGS_IN:
        data (bytes): mensaje cifrado
        clave_privada (str): clave privada del receptor para descifrar
                el mensaje
    ARGS_OUT:
        la firma y el mensaje descifrado
    """
    # Se cogen las distintas partes del mensaje cifrado
    iv = data[0:IV_LENGTH]
    clave_simetrica_cifrada = data[IV_LENGTH:IV_LENGTH+256]
    content = data[IV_LENGTH+256:]

    # Se descifra la clave simétrica con la clave privada del receptor
    clave_rsa = RSA.importKey(clave_privada)
    cifrado_asimetrico = PKCS1_OAEP.new(clave_rsa)
    try:
        clave_simetrica = cifrado_asimetrico.decrypt(clave_simetrica_cifrada)
    except (ValueError, TypeError):
        print('Error descifrando clave simétrica')
        return None, None

    # Se descifra el contenido del mensaje utilzando la clave
    # simétrica descifrada
    #try:
    cifrado_simetrico = AES.new(clave_simetrica, AES.MODE_CBC, iv)
    content_descifrado = unpad(cifrado_simetrico.decrypt(content),
                                   AES.block_size)
    """except (ValueError, KeyError):
        print('Error descifrando el contenido')
        return None, None"""

    return content_descifrado[0:256], content_descifrado[256:]