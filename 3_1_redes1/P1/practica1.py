"""
    practica1.py

    Autor: Daniel Mohedano <daniel.mohedano@estudiante.uam.es>
    Autor: Silvia Sopeña <silvia.sopenna@estudiante.uam.es>
    2020 EPS-UAM
"""

from rc1_pcap import *
import sys
import binascii
import signal
import argparse
from argparse import RawTextHelpFormatter
import time
import logging

ETH_FRAME_MAX = 1514
PROMISC = 1
NO_PROMISC = 0
TO_MS = 10
num_paquete = 0
TIME_OFFSET = 30 * 60


def signal_handler(nsignal, frame):
    logging.info('Control C pulsado')
    if handle:
        pcap_breakloop(handle)


def procesa_paquete(us, header, data):
    global num_paquete, pdumper, n_bytes
    logging.info('Nuevo paquete de {} bytes capturado en el timestamp UNIX {}.{}'.format(header.len, header.ts.tv_sec,
                                                                                         header.ts.tv_usec))
    num_paquete += 1

    aux_string = data[:min(n_bytes, header.len)].hex()
    aux_string = " ".join(aux_string[i:i+2] for i in range(0, len(aux_string), 2))
    logging.info(aux_string)

    if pdumper is not None:
        header.ts.tv_sec += TIME_OFFSET
        pcap_dump(pdumper, header, data)

    return

if __name__ == "__main__":
    global pdumper, args, handle, n_bytes
    parser = argparse.ArgumentParser(
        description='Captura tráfico de una interfaz ( o lee de fichero) y muestra la longitud y timestamp de los paquetes',
        formatter_class=RawTextHelpFormatter)
    parser.add_argument('--file', dest='tracefile', default=False, help='Fichero pcap a abrir')
    parser.add_argument('--itf', dest='interface', default=False, help='Interfaz a abrir')
    parser.add_argument('--nbytes', dest='nbytes', type=int, default=14, help='Número de bytes a mostrar por paquete')
    parser.add_argument('--debug', dest='debug', default=False, action='store_true', help='Activar Debug messages')
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s %(levelname)s]\t%(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='[%(asctime)s %(levelname)s]\t%(message)s')

    if args.tracefile is False and args.interface is False:
        logging.error('No se ha especificado interfaz ni fichero')
        parser.print_help()
        sys.exit(-1)

    signal.signal(signal.SIGINT, signal_handler)

    errbuf = bytearray()
    handle = None
    pdumper = None
    dumper_handle = None
    n_bytes = args.nbytes

    if args.tracefile is not False:
        handle = pcap_open_offline(args.tracefile, errbuf)
    else:
        handle = pcap_open_live(args.interface, ETH_FRAME_MAX, NO_PROMISC, TO_MS, errbuf)
        dumper_handle = pcap_open_dead(DLT_EN10MB, ETH_FRAME_MAX)
        pdumper = pcap_dump_open(dumper_handle, "captura.{}.{}.pcap".format(args.interface, int(time.time())))

    ret = pcap_loop(handle, -1, procesa_paquete, None)
    if ret == -1:
        logging.error('Error al capturar un paquete')
    elif ret == -2:
        logging.debug('pcap_breakloop() llamado')
    elif ret == 0:
        logging.debug('No mas paquetes o limite superado')
    logging.info('{} paquetes procesados'.format(num_paquete))
    pcap_close(handle)
    if args.interface is not False:
        pcap_close(dumper_handle)
        pcap_dump_close(pdumper)
