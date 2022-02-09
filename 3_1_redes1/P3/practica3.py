#!/usr/bin/python
'''
    practica3.py
    Programa principal que realiza el análisis de tráfico sobre una traza PCAP.
    Autor: Javier Ramos <javier.ramos@uam.es>
    2020 EPS-UAM
'''

import sys
import argparse
from argparse import RawTextHelpFormatter
import time
import logging
import shlex
import subprocess
import pandas as pd
from io import StringIO
import os
import warnings
from decimal import *

warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

'''
    Función: calcularECDF
    Entrada: 
        -datos: lista con los datos sobre los que calcular la ECDF
    Salida: :
        -datos: lista con los valores x (datos de entrada)
        -y: lista con los valores de probabilidad acumulada para cada dato de entrada
    Descripción:  Esta función recibe una lista de datos y calcula la función empírica de distribución 
    acumulada sobre los mismos. Los datos se devuelven listos para ser pintados.
'''


def calcularECDF(datos):
    datos.sort()
    n = len(datos)
    y = [(i - 1) / n for i in range(1, n + 1)]

    return datos, y


'''
    Función: ejecutarComandoObtenerSalida
    Entrada: 
        -comando: cadena de caracteres con el comando a ejecutar
    Salida: 
        -codigo_retorno: código numérico que indica el retorno del comando ejecutado.
        Si este valor es 0, entonces el comando ha ejecutado correctamente.
        -salida_retorno: cadena de caracteres con el retorno del comando. Este retorno
        es el mismo que obtendríamos por stdout al ejecutar un comando de terminal.

    Descripción: Esta función recibe una cadena con un comando a ejecutar, lo ejecuta y retorna
    tanto el código de resultado de la ejecución como la salida que el comando produzca por stdout
'''


def ejecutarComandoObtenerSalida(comando):
    proceso = subprocess.Popen(shlex.split(comando), stdout=subprocess.PIPE)
    salida_retorno = ''
    while True:

        salida_parcial = proceso.stdout.readline()
        if salida_parcial.decode() == '' and proceso.poll() is not None:
            break
        if salida_parcial:
            salida_retorno += salida_parcial.decode()
    codigo_retorno = proceso.poll()
    return codigo_retorno, salida_retorno


'''
    Función: pintarECDF
    Entrada:
        -datos: lista con los datos que se usarán para calcular y pintar la ECDF
        -nombre_fichero: cadena de caracteres con el nombre del fichero donde se guardará la imagen
        (por ejemplo figura.png)
        -titulo: cadena de caracteres con el título a pintar en la gráfica
        -titulo_x: cadena de caracteres con la etiqueta a usar para el eje X de la gráfica
        -titulo_y: cadena de caracteres con la etiqueta a usar para el eje Y de la gráfica
    Salida: 
        -Nada

    Descripción: Esta función pinta una gráfica ECDF para unos datos de entrada y la guarda en una imagen
'''


def pintarECDF(datos, nombre_fichero, titulo, titulo_x, titulo_y):
    x, y = calcularECDF(datos)
    x.append(x[-1])
    y.append(1)
    fig1, ax1 = plt.subplots()
    plt.step(x, y, '-')
    _ = plt.xticks(rotation=45)
    plt.title(titulo)
    fig1.set_size_inches(12, 10)
    plt.tight_layout()
    plt.locator_params(nbins=20)
    ax1.set_xlabel(titulo_x)
    ax1.set_ylabel(titulo_y)
    plt.savefig(nombre_fichero, bbox_inches='tight')


'''
    Función: pintarSerieTemporal
    Entrada:
        -x: lista de tiempos en formato epoch y granularidad segundos
        -y: lista con los valores a graficar
        -nombre_fichero: cadena de caracteres con el nombre del fichero donde se guardará la imagen
        (por ejemplo figura.png)
        -titulo: cadena de caracteres con el título a pintar en la gráfica
        -titulo_x: cadena de caracteres con la etiqueta a usar para el eje X de la gráfica
        -titulo_y: cadena de caracteres con la etiqueta a usar para el eje Y de la gráfica
    Salida: 
        -Nada

    Descripción: Esta función pinta una serie temporal dados unos datos x e y de entrada y la guarda en una imagen
'''


def pintarSerieTemporal(x, y, nombre_fichero, titulo, titulo_x, titulo_y):
    fig1, ax1 = plt.subplots()
    plt.plot(x, y, '-')
    _ = plt.xticks(rotation=45)
    plt.title(titulo)
    fig1.set_size_inches(12, 10)
    plt.gcf().autofmt_xdate()
    plt.gca().xaxis.set_major_locator(mtick.FixedLocator(x))
    plt.gca().xaxis.set_major_formatter(
        mtick.FuncFormatter(lambda pos, _: time.strftime("%d-%m-%Y %H:%M:%S", time.localtime(pos))))
    plt.tight_layout()
    plt.locator_params(nbins=20)
    ax1.set_xlabel(titulo_x)
    ax1.set_ylabel(titulo_y)
    plt.savefig(nombre_fichero, bbox_inches='tight')


'''
    Función: pintarTarta
    Entrada:
        -etiquetas: lista con cadenas de caracteres que contienen las etiquetas a usar en el gráfico de tarta
        -valores: lista con los valores a graficar
        -nombre_fichero: cadena de caracteres con el nombre del fichero donde se guardará la imagen
        (por ejemplo figura.png)
        -titulo: cadena de caracteres con el título a pintar en la gráfica
        
    Salida: 
        -Nada

    Descripción: Esta función pinta un gráfico de tarta dadas unas etiquetas y valores de entrada y lo guarda en una imagen
'''


def pintarTarta(etiquetas, valores, nombre_fichero, titulo):
    explode = tuple([0.05] * (len(etiquetas)))

    fig1, ax1 = plt.subplots()
    plt.pie(valores, autopct='%1.1f%%', startangle=90, pctdistance=0.85)
    plt.legend(etiquetas, loc="best")
    plt.title(titulo)
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig1 = plt.gcf()
    fig1.gca().add_artist(centre_circle)
    fig1.set_size_inches(12, 10)
    ax1.axis('equal')
    plt.tight_layout()
    plt.savefig(nombre_fichero, bbox_inches='tight')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Programa principal que realiza el análisis de tráfico sobre una traza PCAP',
        formatter_class=RawTextHelpFormatter)
    parser.add_argument('--trace', dest='tracefile', default=False, help='Fichero de traza a usar', required=True)
    parser.add_argument('--mac', dest='mac', default=False, help='MAC usada para filtrar', required=True)
    parser.add_argument('--ip_flujo_tcp', dest='ip_flujo_tcp', default=False, help='IP para filtrar por el flujo TCP',
                        required=True)
    parser.add_argument('--port_flujo_udp', dest='port_flujo_udp', default=False,
                        help='Puerto para filtrar por el flujo UDP', required=True)
    parser.add_argument('--debug', dest='debug', default=False, action='store_true', help='Activar Debug messages')
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s %(levelname)s]\t%(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='[%(asctime)s %(levelname)s]\t%(message)s')

    # Creamos un directorio a donde volcaremos los resultado e imágenes

    if not os.path.isdir('resultados'):
        os.mkdir('resultados')

    if not os.path.isdir('aux'):
        os.mkdir('aux')

    file_ip = "aux/ip.txt"
    file_udp = "aux/udp.txt"
    file_tcp = "aux/tcp.txt"

    # Analisis de protocolos
    # Añadir código para obtener el porcentaje de tráfico IPv4 y NO-IPv4
    npaquetes = int(subprocess.getoutput("tshark -r traza.pcap -T fields -e frame.number | wc -l"))
    print('# paquetes: {}'.format(npaquetes))
    subprocess.getoutput("tshark -r traza.pcap -T fields -e frame.number -e ip.src -e ip.dst -e ip.len -Y 'ip' > {}".format(file_ip))
    nip = int(subprocess.getoutput("wc -l < {}".format(file_ip)))
    print('# IPv4: {}'.format(nip))
    print('% IPv4: {:0.4f}'.format(100*Decimal(nip)/Decimal(npaquetes)))
    print('% NO-IPv4: {:0.4f}'.format(100*Decimal((npaquetes - nip))/Decimal(npaquetes)))
    # Añadir código para obtener el porcentaje de tráfico TPC,UDP y OTROS sobre el tráfico IP
    ntcp = int(subprocess.getoutput("tshark -r traza.pcap -T fields -e frame.number -Y 'tcp' | wc -l"))
    nudp = int(subprocess.getoutput("tshark -r traza.pcap -T fields -e frame.number -Y 'udp and ip' | wc -l"))
    print('# TCP: {}'.format(ntcp))
    print('# UDP: {}'.format(nudp))
    print('% TCP: {:0.4f}'.format(100*Decimal(ntcp)/Decimal(nip)))
    print('% UDP: {:0.4f}'.format(100*Decimal(nudp)/Decimal(nip)))
    print('% OTROS: {:0.4f}'.format(100*Decimal(nip - nudp - ntcp)/Decimal(nip)))

    # Obtención de top direcciones IP
    # TODO: Añadir código para obtener los datos y generar la gráfica de top IP origen por bytes
    salida = subprocess.getoutput("""awk '{ip_origen[$2] += $4;} END { for (valor in ip_origen) { print valor"\t"ip_origen[valor];}}' aux/ip.txt | sort -k2 -n | tail -n 5""")
    print(salida)
    etiquetas = []
    valores = []
    for linea in salida.split("\n"):
        ip_src, nbytes = linea.split("\t")
        etiquetas.append(ip_src)
        valores.append(nbytes)

    pintarTarta(etiquetas, valores, "resultados/top5iporigenbytes.png", "Top 5 direcciones IP origen por bytes")
    # TODO: Añadir código para obtener los datos y generar la gráfica de top IP origen por paquetes
    salida = subprocess.getoutput("""awk '{ip_origen[$2] += 1;} END { for (valor in ip_origen) { print valor"\t"ip_origen[valor];}}' aux/ip.txt | sort -k2 -n | tail -n 5""")
    print(salida)
    etiquetas = []
    valores = []
    for linea in salida.split("\n"):
        ip_src, n = linea.split("\t")
        etiquetas.append(ip_src)
        valores.append(n)

    pintarTarta(etiquetas, valores, "resultados/top5iporigen.png", "Top 5 direcciones IP origen por paquetes")
    # TODO: Añadir código para obtener los datos y generar la gráfica de top IP destino por bytes
    salida = subprocess.getoutput("""awk '{ip_destino[$3] += $4;} END { for (valor in ip_destino) { print valor"\t"ip_destino[valor];}}' aux/ip.txt | sort -k2 -n | tail -n 5""")
    print(salida)
    etiquetas = []
    valores = []
    for linea in salida.split("\n"):
        ip_dst, nbytes = linea.split("\t")
        etiquetas.append(ip_dst)
        valores.append(nbytes)

    pintarTarta(etiquetas, valores, "resultados/top5ipdestinobytes.png", "Top 5 direcciones IP destino por bytes")
    # TODO: Añadir código para obtener los datos y generar la gráfica de top IP destino por paquetes
    salida = subprocess.getoutput("""awk '{ip_destino[$3] += 1;} END { for (valor in ip_destino) { print valor"\t"ip_destino[valor];}}' aux/ip.txt | sort -k2 -n | tail -n 5""")
    print(salida)
    etiquetas = []
    valores = []
    for linea in salida.split("\n"):
        ip_src, n = linea.split("\t")
        etiquetas.append(ip_src)
        valores.append(n)

    pintarTarta(etiquetas, valores, "resultados/top5ipdestino.png", "Top 5 direcciones IP destino por paquetes")
    
    # Obtención de top puertos TCP
    # TODO: Añadir código para obtener los datos y generar la gráfica de top puerto origen TCP por bytes

    # TODO: Añadir código para obtener los datos y generar la gráfica de top puerto destino TCP por bytes

    # TODO: Añadir código para obtener los datos y generar la gráfica de top puerto origen TCP por paquetes

    # TODO: Añadir código para obtener los datos y generar la gráfica de top puerto destino  TCP por paquetes

    # Obtención de top puertos UDP
    # TODO: Añadir código para obtener los datos y generar la gráfica de top puerto origen UDP por bytes

    # TODO: Añadir código para obtener los datos y generar la gráfica de top puerto destino UDP por bytes

    # TODO: Añadir código para obtener los datos y generar la gráfica de top puerto origen UDP por paquetes

    # TODO: Añadir código para obtener los datos y generar la gráfica de top puerto destino UDP por paquetes

    # Obtención de series temporales de ancho de banda
    # TODO: Añadir código para obtener los datos y generar la gráfica de la serie temporal de ancho de banda con MAC como origen

    # TODO: Añadir código para obtener los datos y generar la gráfica de la serie temporal de ancho de banda con MAC como destino

    # Obtención de las ECDF de tamaño de los paquetes
    # TODO: Añadir código para obtener los datos y generar la gráfica de la ECDF de los tamaños de los paquetes a nivel 2

    # Obtención de las ECDF de tamaño de los tiempos entre llegadas
    # TODO: Añadir código para obtener los datos y generar la gráfica de la ECDF de los tiempos entre llegadas para el flujo TCP

    # TODO: Añadir código para obtener los datos y generar la gráfica de la ECDF de los tiempos entre llegadas para el flujo UDP
