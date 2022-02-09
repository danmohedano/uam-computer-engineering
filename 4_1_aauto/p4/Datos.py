# -*- coding: utf-8 -*-

# coding: utf-8
import pandas as pd
import numpy as np

class Datos:
    """Contiene conjuntos de datos.

    Clase encargada de contener los conjuntos de datos que luego son utilizados por clasificadores. 
    La clase se encarga de procesar los datos y convertirlos a valores enteros cuando es necesario.

    Attributes:
        datos (pd.Dataframe): Los datos que contiene la clase.
        atributos (list(string)): Nombres de los atributos contenidos en self.datos.
        nominalAtributos (list(boolean)): Determina si cada atributo es nominal o no.
        diccionario (dict): Diccionario de traducción entre los valores nominales y
            los valores enteros por los que se sustituyen.    
    """

    def __init__(self, nombreFichero):
        """Genera un objeto de tipo Datos.

        Args:
            nombreFichero (string): Nombre del fichero csv de donde cargar los datos.
        """   
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
        

    def extraeDatos(self, idx):
        """Devuelve los datos que se encuentran en los índices proporcionados.

        Args:
            idx (list(int)): Lista de índices.

        Returns:
            (pd.DataFrame): Datos contenidos en los índices indicados.
        """
        return self.datos.iloc[idx]

    @property
    def shape(self):
        """
        Returns:
            (tuple(int, int)): Forma de los datos (# filas, #columnas).
        """
        return self.datos.shape

    @staticmethod
    def calcularMediasDesv(datos):
        """Calcula la media y desviación típica de cada atributo.

        Realizará el cálculo en todas las columnas excepto la última (considerada la clase).

        Args:
            datos (2D np.ndarray): Conjunto de datos.

        Returns:
            medias (list(float)): Lista de medias.
            stds (list(float)): Lista de desviaciones típicas.
        """
        medias = []
        stds = []

        # Se itera por cada atributo (columna)
        for j in range(datos.shape[1] - 1):
            medias.append(np.mean(datos[:, j]))
            stds.append(np.std(datos[:, j]))

        return medias, stds

    @staticmethod
    def normalizarDatos(datos):
        """Normaliza los datos proporcionados usando Z-score.

        Args:
            datos (2D np.ndarray): Conjunto de datos a normalizar.
        """
        medias, stds = Datos.calcularMediasDesv(datos)

        # Normalizar cada columna
        for j in range(len(medias)):
            datos[:, j] -= medias[j]
            datos[:, j] /= stds[j]

