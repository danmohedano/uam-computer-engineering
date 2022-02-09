from Datos import Datos
from clasificador import ClasificadorKNN, ClasificadorRegresionLogistica, ClasificadorNaiveBayes
from EstrategiaParticionado import ValidacionSimple, ValidacionCruzada
import numpy as np
import pandas as pd


def main():
    datos_pima = Datos('data/pima-indians-diabetes.data')
    datos_wdbc = Datos('data/wdbc.data')

    particion = ValidacionCruzada(5)
    seed = 29
    
    ClasificadorRegresionLogistica(n_epochs=1, const=1).validacion(particion, datos_pima, seed)


if __name__ == '__main__':
    main()