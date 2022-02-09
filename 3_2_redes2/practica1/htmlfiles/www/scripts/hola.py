"""
Script simple que recibe una palabra y devuelve la
cadena "Hola <<cadena>>!"
"""
import sys
import signal
TIMEOUT = 1
signal.signal(signal.SIGALRM, input)
signal.alarm(TIMEOUT)

try:
    for line in sys.stdin:
        nombre = line.split('&')[0].split('=')[-1]
        print("Hola, {}!".format(nombre))
        break
except:
    ignorar = True
        
print('\r\n')