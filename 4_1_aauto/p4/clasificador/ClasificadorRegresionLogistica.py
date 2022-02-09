from clasificador import Clasificador
import numpy as np
import random
import math
import scipy.special


class ClasificadorRegresionLogistica(Clasificador):
    """Clasificador Regresión Logística por máxima verosimilitud.

    Args:
        n_epochs (int): Número de épocas para el entrenamiento.
        const (float): Constante de aprendizaje.
    """

    def __init__(self, n_epochs=1, const=1.0):
        self.n_epochs = n_epochs
        self.const = const

    @staticmethod
    def _sigmoid(val):
        """Calcula la función sigmoidal aplicada al valor val.
        
        Args:
            val (float): Valor a evaluar.

        Returns:
            float: Valor de la sigmoidal.
        """
        return scipy.special.expit(val)
    
    def entrenamiento(self, datostrain, nominalAtributos):
        """Entrena el clasificador.

        Args:
            datosTrain (2D np.ndarray): Datos de entrenamiento.
            nominalAtributos (list(boolean)): Lista con los tipos de atributo (nominal o no).
        """
        # Se inicializa el vector del hiperplano
        self.w = [random.uniform(-1.0, 1.0)] * datostrain.shape[1]

        # Loop de entrenamiento
        for ie in range(self.n_epochs):
            for j in range(datostrain.shape[0]):
                xj = np.concatenate([[1], datostrain[j][:-1]])
                product = np.dot(self.w, xj)

                self.w = self.w - (self.const * (self._sigmoid(product) - datostrain[j][-1]) * xj)
    
    def clasifica(self, datostest, nominalAtributos):
        """Realiza la clasificación de los datos proporcionados.

        Args:
            datosTest (2D np.ndarray): Datos de validación.
            nominalAtributos (list(boolean)): Lista con los tipos de atributo (nominal o no).

        Returns:
            (list(Any)): Lista con las predicciones realizadas por el clasificador.
        """
        predicciones = []

        for j in range(datostest.shape[0]):
            xj = np.concatenate([[1], datostest[j][:-1]])
            product = np.dot(self.w, xj)

            if product >= 0:
                predicciones.append(1)
            else:
                predicciones.append(0)
        
        return predicciones

    def confianza(self, datostest, nominalAtributos):
        """Realiza la clasificación de los datos proporcionados y devuelve 
        score para cada dato de test.

        Args:
            datosTest (2D np.ndarray): Datos de validación.
            nominalAtributos (list(boolean)): Lista con los tipos de atributo (nominal o no).

        Returns:
            (list(Any)): Lista con los scores de cada dato.
        """
        scores = []

        for j in range(datostest.shape[0]):
            xj = np.concatenate([[1], datostest[j][:-1]])
            product = np.dot(self.w, xj)

            scores.append(product)
        
        return scores

    def validacion_scores(self, particionado, dataset, seed=None):
        """Realiza la validación siguiendo una estrategia de particionado determinada.

        Args:
            particionado (EstrategiaParticionado): Estrategia de particionado elegida para la validación.
            dataset (Datos): Datos que validar.
            seed (Any): Semilla para la generación de particiones.

        Returns:
            (list): Lista con los scores de test.
        """
        scores = []
        particiones = particionado.creaParticiones(dataset, seed)

        for particion in particiones:
            datos_train = dataset.extraeDatos(particion.indicesTrain).to_numpy()
            datos_test = dataset.extraeDatos(particion.indicesTest).to_numpy()

            self.entrenamiento(datos_train, dataset.nominalAtributos)
            scores += [(particion.indicesTest[i], self.confianza(datos_test, dataset.nominalAtributos)[i]) for i in range(len(particion.indicesTest))]
        
        return scores

