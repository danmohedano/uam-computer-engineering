# -*- coding: utf-8 -*-

# coding: utf-8
import pandas as pd
import numpy as np

class Datos:

    # Constructor: procesar el fichero para asignar correctamente las variables nominalAtributos, datos y diccionarios
    def __init__(self, nombreFichero):    
        # Cargado de datos a un DataFrame   
        self.datos = pd.read_csv(nombreFichero)

        # Creación de nominalAtributos, comprobando si son nominales o no (considerados object por Pandas)
        self.atributos = list(self.datos.columns)
        self._atributos_index = {self.atributos[i]: i for i in range(len(self.atributos))}
        self.nominalAtributos = []

        for atr in self.atributos:
            if self.datos[atr].dtype.name not in ['object', 'int64', 'float64']:
                raise ValueError
            else:
                self.nominalAtributos.append(self.datos[atr].dtype.name == 'object')

        # Creación del diccionario de conversión
        self.diccionario = {}
        for atr in self.atributos:
            if self.nominalAtributos[self._atributos_index[atr]]:
                # Se obtienen los valores únicos del atributo y se ordenan lexicográficamente
                uniq_values = self.datos[atr].unique()
                uniq_values.sort()
                self.diccionario[atr] = {uniq_values[j]: j for j in range(len(uniq_values))}
            else:
                self.diccionario[atr] = {}

        # Sustitución de valores nominales por valores enteros en los datos
        for atr in self.atributos:
            if self.nominalAtributos[self._atributos_index[atr]]:
                self.datos[atr].replace(self.diccionario[atr], inplace=True)
        

    # Devuelve el subconjunto de los datos cuyos �ndices se pasan como argumento
    def extraeDatos(self, idx):
        return self.datos.iloc[idx]

    @property
    def shape(self):
        return self.datos.shape
