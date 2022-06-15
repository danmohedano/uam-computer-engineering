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


def leer4(fichero_de_datos, por):
    entradas, salidas = _leerFichero(fichero_de_datos)

    idxs_train = np.random.choice(entradas.shape[0], int(entradas.shape[0] * por))
    idxs_test_val = [x for x in range(entradas.shape[0]) if x not in idxs_train]
    idxs_val = np.random.choice(idxs_test_val, int(len(idxs_test_val) / 2))
    idxs_test = [x for x in idxs_test_val if x not in idxs_val]

    return entradas[idxs_train], salidas[idxs_train], entradas[idxs_val], salidas[idxs_val], entradas[idxs_test], salidas[idxs_test]


def leer5(fichero_de_entrenamiento, fichero_de_test, por):
    entrada_train, salida_train = _leerFichero(fichero_de_entrenamiento)
    entrada_test, salida_test = _leerFichero(fichero_de_test)

    idxs_train = np.random.choice(entrada_train.shape[0], int(entrada_train.shape[0] * por))
    idxs_val = [x for x in range(entrada_train.shape[0]) if x not in idxs_train]

    return entrada_train[idxs_train], salida_train[idxs_train], entrada_train[idxs_val], salida_train[idxs_val], entrada_test, salida_test


def _leerFichero(file):
    with open(file, 'r') as f:
        lineas = f.read().split('\n')
        m = int(lineas[0].split()[0])

    datos = np.loadtxt(file, skiprows=1)

    return datos[:, :m], datos[:, m:]


def get_train_test(mode, file, file_test=None, portion=0.8):
    if mode == 1:
        return leer1(file, portion)
    elif mode == 2:
        entrada_train, salida_train = leer2(file)
        entrada_test, salida_test = entrada_train.copy(), salida_train.copy()
        return entrada_train, salida_train, entrada_test, salida_test
    elif mode == 3:
        return leer3(file, file_test)


def get_train_val_test(mode, file, file_test=None, portion=0.6):
    if mode == 1:
        return leer4(file, portion)
    elif mode == 2:
        entradas, salidas = leer2(file)
        entrada_test, salida_test = entradas.copy(), salidas.copy()

        idxs_train = np.random.choice(entradas.shape[0], int(entradas.shape[0] * portion))
        idxs_val = [x for x in range(entradas.shape[0]) if x not in idxs_train]

        return entradas[idxs_train], salidas[idxs_train], entradas[idxs_val], salidas[idxs_val], entrada_test, salida_test
    elif mode == 3:
        return leer5(file, file_test, portion)


def construir_red_n_m(n_entradas, m_salidas, peso_min, peso_max, umbral=0, fn_activacion=None, tipo='Adaline'):
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
        elif tipo == 'MLP':
            capaSalida.Añadir(NeuronaGenerica(fn_activacion=fn_activacion))
            
    capaEntrada.ConectarCapa(capaSalida, peso_min, peso_max)
    
    red.AñadirCapa(capaEntrada)
    red.AñadirCapa(capaSalida)

    return red

def construir_red(n_entradas, m_salidas, capas_ocultas, peso_min, peso_max, fn_activacion=lambda x: x, fn_activacion_2=lambda _: 1):
    red = RedNeuronal()
    capaEntrada = Capa()
    capaSalida = Capa()

    # Crear neuronas de entrada
    for _ in range(n_entradas):
        capaEntrada.Añadir(NeuronaGenerica(lambda x: x, lambda _:1))

    # Crear sesgo
    capaEntrada.Añadir(NeuronaSesgo())

    red.AñadirCapa(capaEntrada)

    prev_capa = capaEntrada
    for neuronas_capa_oculta in capas_ocultas:
        capa_oculta = Capa()
        for _ in range(neuronas_capa_oculta):
            capa_oculta.Añadir(NeuronaGenerica(fn_activacion=fn_activacion, fn_activacion_2=fn_activacion_2))
            
        # Crear sesgo
        capa_oculta.Añadir(NeuronaSesgo())

        prev_capa.ConectarCapa(capa_oculta, peso_min, peso_max)
        prev_capa = capa_oculta
        red.AñadirCapa(capa_oculta)

    for _ in range(m_salidas):
        capaSalida.Añadir(NeuronaGenerica(fn_activacion=fn_activacion, fn_activacion_2=fn_activacion_2))

    prev_capa.ConectarCapa(capaSalida, peso_min, peso_max)
    red.AñadirCapa(capaSalida)

    return red