import numpy as np
from redneuronal import *
from capa import *
from neurona import *


def leer1(fichero_de_datos, por):
    entradas, salidas = _leerFichero(fichero_de_datos)
    
    idxs_train = np.random.choice(entradas.shape[0], int(entradas.shape[0]*por))
    idxs_test = [x for x in range(entradas.shape[0]) if x not in idxs_train]

    return entradas[idxs_train], salidas[idxs_train], entradas[idxs_test], salidas[idxs_test]

   
def leer2(fichero_de_datos):
    return _leerFichero(fichero_de_datos)

    
def leer3(fichero_de_entrenamiento, fichero_de_test):
    entrada_train, salida_train = _leerFichero(fichero_de_entrenamiento)
    entrada_test, salida_test = _leerFichero(fichero_de_test)
    return entrada_train, salida_train, entrada_test, salida_test


def _leerFichero(file):
    with open(file, 'r') as f:
        lineas = f.read().split('\n')
        m = int(lineas[0].split()[0])

    datos = np.loadtxt(file, skiprows=1)

    return datos[:, :m], datos[:, m:]


def get_train_test(mode, file, file_test=None, portion=0.2):
    if mode == 1:
        return leer1(file, portion)
    elif mode == 2:
        entrada_train, salida_train = leer2(file)
        entrada_test, salida_test = entrada_train.copy(), salida_train.copy()
        return entrada_train, salida_train, entrada_test, salida_test
    else:
        return leer3(file, file_test)


def construir_red_n_m(n_entradas, m_salidas, peso_min, peso_max, umbral=0, tipo='Adaline'):
    red = RedNeuronal()
    capaEntrada = Capa()
    capaSalida = Capa()
    
    # Crear neuronas de entrada
    for _ in range(n_entradas):
        capaEntrada.Añadir(NeuronaDirecta())

    # Crear sesgo
    capaEntrada.Añadir(NeuronaSesgo())
        
    for _ in range(m_salidas):
        if tipo == 'Adaline':            
            capaSalida.Añadir(NeuronaAdaline())
        elif tipo == 'Perceptron':
            capaSalida.Añadir(NeuronaPerceptron(umbral=umbral))
            
    capaEntrada.ConectarCapa(capaSalida, peso_min, peso_max)
    
    red.AñadirCapa(capaEntrada)
    red.AñadirCapa(capaSalida)

    return red