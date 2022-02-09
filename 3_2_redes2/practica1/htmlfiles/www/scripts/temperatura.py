"""
Script simple que recibe una temperatura en grados Centigrados y
devuelve la temperatura en Farenheit
"""
import sys
import signal 
TIMEOUT = 1
signal.signal(signal.SIGALRM, input)
signal.alarm(TIMEOUT)

try:
    for line in sys.stdin:
        temp_c = line.split('&')[0].split('=')[-1]
        temp_f = (float(temp_c) * (9.0 / 5.0)) + 32 
        print("{} Celsius -> {} Farenheit".format(temp_c, temp_f))
except ValueError:
    print("{} no es un valor valido para temperatura".format(temp_c))
except:
    ignorar = True

print('\r\n')
