from redneuronal import *
from capa import *
from neurona import *
from utils import *
import argparse
import sys


def main_mp():
    parser = argparse.ArgumentParser(description='2. Neuronas de McCulloch-Pitts. Programa para simular la red \
                                                     detectora de frío y calor.')
    parser.add_argument('mp', help='Argumento que indica el ejercicio a ejecutar. No tiene uso.')
    parser.add_argument('file_in', help='Nombre de fichero de entrada con los impulsos')
    parser.add_argument('file_out', help='Nombre de fichero de salida donde guardar el estado de la red.')

    args = parser.parse_args()

    # Creación de la red
    umbral = 2.0
    
    red = RedNeuronal()
    capa_entrada = Capa()
    capa_oculta = Capa()
    capa_salida = Capa()
    
    x1 = NeuronaDirecta()
    x2 = NeuronaDirecta()
    z1 = NeuronaMC(umbral)
    z2 = NeuronaMC(umbral)
    y1 = NeuronaMC(umbral)
    y2 = NeuronaMC(umbral)
    
    x1.Conectar(y1, 2.0)
    x2.Conectar(z1, -1.0)
    x2.Conectar(z2, 2.0)
    x2.Conectar(y2, 1.0)
    z1.Conectar(y1, 2.0)
    z2.Conectar(z1, 2.0)
    z2.Conectar(y2, 1.0)

    capa_entrada.Añadir(x1)
    capa_entrada.Añadir(x2)
    capa_oculta.Añadir(z1)
    capa_oculta.Añadir(z2)
    capa_salida.Añadir(y1)
    capa_salida.Añadir(y2)
    red.AñadirCapa(capa_entrada)
    red.AñadirCapa(capa_oculta)
    red.AñadirCapa(capa_salida)
    
    # Lectura de los impulsos de entrada
    impulsos = []
    with open(args.file_in, 'r') as f:
        for line in f:
            impulsos.append(line.split())

    # Ejecución de la red
    with open(args.file_out, 'w') as f:
        f.write('\t'.join(['x1', 'x2', 'z1', 'z2', 'y1', 'y2']) + '\n')
        for i, j in impulsos:
            x1.valor_entrada = float(i)
            x2.valor_entrada = float(j)
            
            red.Disparar()
            red.Propagar()

            valores = red.valores_neuronas()
            f.write('\t'.join(['{:.0f}'.format(x) for x in valores]) + '\n')

        while valores.count(0.0) != len(valores):
            # Continuar hasta que se termine de propagar todo
            x1.valor_entrada = 0.0
            x2.valor_entrada = 0.0
            
            red.Disparar()
            red.Propagar()

            valores = red.valores_neuronas()
            f.write('\t'.join(['{:.0f}'.format(x) for x in valores]) + '\n')


def main_perceptron():
    parser = argparse.ArgumentParser(description='4. Perceptron')
    parser.add_argument('perceptron', help='Argumento que indica el ejercicio a ejecutar. No tiene uso.')
    parser.add_argument('mode', help='Modo de lectura [1,2,3]')
    parser.add_argument('file_in', help='Nombre de fichero de entrada con los datos')
    parser.add_argument('alpha', help='Tasa de aprendizaje')
    parser.add_argument('epochs', help='Número de épocas límite')
    parser.add_argument('umbral', help='Umbral')
    parser.add_argument('--file_test', help='Nombre de fichero con los datos de test. Solo utilizado en el modo de lectura 3')
    parser.add_argument('-portion', help='Porción para modo de lectura 1')
    parser.add_argument('-frontera', action='store_true', help='Selecciona si se muestran las fronteras de decisión')
    parser.add_argument('-predicciones', action='store_true', help='Selecciona si se guardan las predicciones a archivo o no')

    args = parser.parse_args()
    
    entrada_train, salida_train, entrada_test, salida_test = get_train_test(int(args.mode), args.file_in, args.file_test, float(args.portion) if args.portion else None)
    n_entradas = len(entrada_train[0])
    m_salidas = len(salida_train[0])
    red = construir_red_n_m(n_entradas, m_salidas, 0.0, 0.0, umbral=float(args.umbral), tipo='Perceptron')
    
    red.entrenamiento_perceptron(float(args.alpha), int(args.epochs), entrada_train, salida_train)

    if args.frontera:
        print('\n' + '\n'.join(red.frontera_decision))

    predicciones = red.test(entrada_test, salida_test)

    if args.predicciones:
        with open('../predicciones/prediccion_perceptron.txt', 'w') as f:
            for p in predicciones:
                f.write(' '.join([f'{x:1.0f}' for x in p]) + '\n')

    aciertos = 0
    for p, y in zip(predicciones, salida_test):
        if np.array_equal(p, y):
            aciertos += 1

    print(f'\nAccuracy Test: {aciertos / len(salida_test) :.4f}')
    

def main_adaline():
    parser = argparse.ArgumentParser(description='4. Adaline')
    parser.add_argument('adaline', help='Argumento que indica el ejercicio a ejecutar. No tiene uso.')
    parser.add_argument('mode', help='Modo de lectura [1,2,3]')
    parser.add_argument('file_in', help='Nombre de fichero de entrada con los datos')
    parser.add_argument('alpha', help='Tasa de aprendizaje')
    parser.add_argument('epochs', help='Número de épocas límite')
    parser.add_argument('tol', help='Tolerancia para el cambio de pesos')
    parser.add_argument('--file_test', help='Nombre de fichero con los datos de test. Solo utilizado en el modo de lectura 3')
    parser.add_argument('-portion', help='Porción para modo de lectura 1')
    parser.add_argument('-frontera', action='store_true', help='Selecciona si se muestran las fronteras de decisión')
    parser.add_argument('-predicciones', action='store_true', help='Selecciona si se guardan las predicciones a archivo o no')

    args = parser.parse_args()

    entrada_train, salida_train, entrada_test, salida_test = get_train_test(int(args.mode), args.file_in, args.file_test, float(args.portion) if args.portion else None)
    n_entradas = len(entrada_train[0])
    m_salidas = len(salida_train[0])
    red = construir_red_n_m(n_entradas, m_salidas, -0.5, 0.5)
    
    red.entrenamiento_adaline(float(args.alpha), int(args.epochs), float(args.tol), entrada_train, salida_train)
    
    if args.frontera:
        print('\n' + '\n'.join(red.frontera_decision))

    predicciones = red.test(entrada_test, salida_test)

    if args.predicciones:
        with open('../predicciones/prediccion_adaline.txt', 'w') as f:
            for p in predicciones:
                f.write(' '.join([f'{x:1.0f}' for x in p]) + '\n')

    aciertos = 0
    for p, y in zip(predicciones, salida_test):
        if np.array_equal(p, y):
            aciertos += 1

    print(f'\nAccuracy Test: {aciertos / len(salida_test) :.4f}')
            

main_dict = {'mp': main_mp, 'perceptron': main_perceptron, 'adaline': main_adaline}
help_string = f"Utilización incorrecta. El primer argumento debe ser el ejercicio deseado de entre {list(main_dict.keys())}"


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(help_string)
    else:
        if sys.argv[1] not in main_dict:
            print(help_string)
        else:
            main_dict[sys.argv[1]]()
