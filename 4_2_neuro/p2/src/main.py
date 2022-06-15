from redneuronal import *
from capa import *
from neurona import *
from utils import *
import math
import argparse
from scipy.special import expit


def fn_sigmoidal(x):
    return 2*expit(x)-1


def fn_sigmoidal_2(x, neurona):
    return (1+neurona.valor_salida)*(1-neurona.valor_salida)/2


def main_retropropagacion():
    parser = argparse.ArgumentParser(description='4. Retropropagación')
    parser.add_argument('mode', help='Modo de lectura [1,2,3]')
    parser.add_argument('file_in', help='Nombre de fichero de entrada con los datos')
    parser.add_argument('alpha', help='Tasa de aprendizaje')
    parser.add_argument('epochs', help='Número de épocas límite')
    parser.add_argument('portion', help='Porción de datos para entrenamiento')
    parser.add_argument('-wait', help='Número de épocas de paciencia')
    parser.add_argument('-val', action='store_true', help='Si se quiere utilizar conjunto de validación como condición de parada.')
    parser.add_argument('-hidden_layers', nargs="+", help='Lista de números de neuronas por cada capa oculta', default=[2])
    parser.add_argument('-file_test', help='Nombre de fichero con los datos de test. Solo utilizado en el modo de lectura 3')
    parser.add_argument('-predicciones', action='store_true', help='Selecciona si se guardan las predicciones a archivo o no')
    parser.add_argument('-norm', action='store_true', help='Decide si normalizar los datos o no.')
    parser.add_argument('-confusion', action='store_true', help='Si el programa debe guardar las matrices de confusión de cada época en un archivo.')

    args = parser.parse_args()
    
    if args.val:
        entrada_train, salida_train, entrada_val, salida_val, entrada_test, salida_test = get_train_val_test(int(args.mode), args.file_in, args.file_test, float(args.portion))
        salida_val = np.where(salida_val == 0, -1, salida_val)
    else:
        entrada_train, salida_train, entrada_test, salida_test = get_train_test(int(args.mode), args.file_in, args.file_test, float(args.portion))
    
    salida_train = np.where(salida_train == 0, -1, salida_train)
    salida_test = np.where(salida_test == 0, -1, salida_test)
    
    n_entradas = len(entrada_train[0])
    m_salidas = len(salida_train[0])
    
    red = construir_red(n_entradas, m_salidas, [int(x) for x in args.hidden_layers], -0.5, 0.5, fn_activacion=fn_sigmoidal, fn_activacion_2=fn_sigmoidal_2)

    # Normalización
    if args.norm:
        # Iterar por los atributos
        for i in range(entrada_train.shape[1]):
            media = np.mean(entrada_train[:, i])
            std = np.std(entrada_train[:, i])

            if args.val:
                entrada_val[:, i] -= media
                entrada_val[:, i] /= std
            entrada_train[:, i] -= media
            entrada_train[:, i] /= std
            entrada_test[:, i] -= media
            entrada_test[:, i] /= std

    if args.val:
        red.retropropagacion(float(args.alpha), int(args.epochs), int(args.wait), entrada_train, salida_train, entrada_val, salida_val, args.confusion)
    else:
        red.retropropagacion(float(args.alpha), int(args.epochs), -1, entrada_train, salida_train, None, None, args.confusion)

    salidas = red.evaluar(entrada_test)
    predicciones = []

    # Tratar predicciones
    for s in salidas:
        prediccion = [-1]*m_salidas
        prediccion[np.argmax(s)] = 1
        predicciones.append(prediccion)

    if args.predicciones:
        with open('../prediccion.txt', 'w') as f:
            for p in predicciones:
                f.write(' '.join([f'{x}' for x in p]) + '\n')

    aciertos = 0
    for p, y in zip(predicciones, salida_test):
        if np.array_equal(p, y):
            aciertos += 1

    print(f'\nAccuracy Test: {aciertos / len(salida_test) :.4f}')


if __name__ == '__main__':
    main_retropropagacion()
