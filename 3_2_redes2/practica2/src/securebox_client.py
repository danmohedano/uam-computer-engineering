"""
    securebox_client.py

    Autor: Daniel Mohedano <daniel.mohedano@estudiante.uam.es>
    Autor: Silvia Sopeña <silvia.sopenna@estudiante.uam.es>
    Fecha de creación: 31/03/2021
"""
import argparse
import utilidad
import os
from project_configuration import FILEDIR_PATH


def main():
    """
    Función main para el cliente de línea de comandos para el servicio SecureBox
    """
    parser = argparse.ArgumentParser(description='Cliente de línea de comandos'
                                                 ' para el servicio SecureBox')
    parser.add_argument('--create_id', nargs='+',
                        help='Crea una nueva identidad (par de claves púlica y privada) para un usuario con nombre nombre y correo email, y la registra en SecureBox, para que pueda ser encontrada por otros usuarios. alias es una cadena identificativa opcional.')

    parser.add_argument('--search_id', dest='cadena_search_id', default=False,
                        help='Busca un usuario cuyo nombre o correo electrónico contenga cadena en el repositorio de identidades de SecureBox, y devuelve su ID.')

    parser.add_argument('--delete_id', dest='id_delete', default=False,
                        help='Borra la identidad con ID id registrada en el sistema. Obviamente, sólo se pueden borrar aquellas identidades creadas por el usuario que realiza la llamada.')

    parser.add_argument('--upload', dest='fichero_upload', default=False,
                        help='Envia un fichero a otro usuario, cuyo ID es especificado con la opción --dest_id. Por defecto, el archivo se subirá a SecureBox firmado y cifrado con las claves adecuadas para que pueda ser recuperado y verificado por el destinatario.')

    parser.add_argument('--source_id', dest='id_source',
                        default=False, help='ID del emisor del fichero.')

    parser.add_argument('--dest_id', dest='id_dest',
                        default=False, help='ID del receptor del fichero.')

    parser.add_argument('--list_files', dest='list_files', default=False,
                        action='store_true', help='Lista todos los ficheros pertenecientes al usuario')

    parser.add_argument('--download', dest='id_fichero_download', default=False,
                        help='Recupera un fichero con ID id_fichero del sistema (este ID se genera en la llamada a upload, y debe ser comunicado al receptor). Tras ser descargado, debe ser verificada la firma y, después, descifrado el contenido.')

    parser.add_argument('--delete_file', dest='id_fichero_delete',
                        default=False, help='Borra un fichero del sistema.')

    parser.add_argument('--encrypt', dest='fichero_encrypt', default=False,
                        help='Cifra un fichero, de forma que puede ser descifrado por otro usuario, cuyo ID es especificado con la opción --dest_id.')

    parser.add_argument('--sign', dest='fichero_sign',
                        default=False, help='Firma un fichero.')

    parser.add_argument('--enc_sign', dest='fichero_enc_sign', default=False,
                        help='Cifra y firma un fichero, combinando funcionalmente las dos opciones anteriores.')

    args = parser.parse_args()

    # 2.1 Gestión de identidades y usuarios
    if args.create_id:
        # Crear una nueva identidad
        if len(args.create_id) != 2 and len(args.create_id) != 3:
            print('Uso incorrecto. Proporcionar: nombre email [alias]')
        else: 
            if len(args.create_id) == 3:
                print('Bienvenido {}! A continuación se creará tu identidad'.format(args.create_id[2]))
            utilidad.crear_identidad(args.create_id[0], args.create_id[1])

    elif args.cadena_search_id:
        # Buscar una identidad
        utilidad.buscar_identidad(args.cadena_search_id)

    elif args.id_delete:
        # Borrar una identidad
        utilidad.borrar_identidad(args.id_delete)

    # 2.2 Cifrado y firma de ficheros
    elif args.fichero_enc_sign and args.id_dest:
        # Cifrado y firma
        file_bytes = utilidad.firmar_cifrar_fichero(args.fichero_enc_sign, args.id_dest)
        file_path = os.path.join(FILEDIR_PATH, args.fichero_enc_sign.split('.')[0] + '_sign_cypher')
        with open(file_path, 'wb') as f:
            f.write(file_bytes)
        print('Bytes guardados en el fichero:', args.fichero_enc_sign.split('.')[0] + '_sign_cypher')

    elif args.fichero_encrypt and args.id_dest:
        # Cifrado de fichero
        file_bytes = utilidad.cifrar_fichero(args.fichero_encrypt, args.id_dest)
        file_path = os.path.join(FILEDIR_PATH, args.fichero_encrypt.split('.')[0] + '_cypher')
        with open(file_path, 'wb') as f:
            f.write(file_bytes)
        print('Bytes guardados en el fichero:', args.fichero_encrypt.split('.')[0] + '_cypher')

    elif args.fichero_sign:
        # Firma de fichero
        file_bytes = utilidad.firmar_fichero(args.fichero_sign)
        file_path = os.path.join(FILEDIR_PATH, args.fichero_sign.split('.')[0] + '_sign')
        with open(file_path, 'wb') as f:
            f.write(file_bytes)
        print('Bytes guardados en el fichero:', args.fichero_sign.split('.')[0] + '_sign')

    # 2.3 Envío y descarga de ficheros
    elif args.fichero_upload and args.id_dest:
        # Envío de un fichero
        utilidad.enviar_fichero(args.fichero_upload, args.id_dest)

    elif args.id_fichero_download and args.id_source:
        # Recuperar fichero
        utilidad.recuperar_fichero(args.id_fichero_download, args.id_source)

    elif args.list_files:
        # Listar ficheros
        utilidad.listar_ficheros()

    elif args.id_fichero_delete:
        # Borrar fichero del sistema
        utilidad.borrar_fichero(args.id_fichero_delete)

    else:
        # No se ha elegido ninguna opción
        print('Ejecute el cliente con alguno de los argumentos descritos en la ayuda (--help)')


if __name__ == '__main__':
    main()
