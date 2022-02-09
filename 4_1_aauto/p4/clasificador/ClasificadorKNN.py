from clasificador import Clasificador
from Datos import Datos
import numpy as np
import random


class ClasificadorKNN(Clasificador):
    """Clasificador K Nearest Neighbors utilizando distancia Euclídea.
    
    Attributes:
        k (int): Número de vecinos.
        norm (boolean): Flag para normalizar los datos.
    """

    def __init__(self, k=1, norm=True):
        """Genera el objeto
        
        Args:
            k (int): Cantidad de vecinos usada.
            norm (boolean): Flag para normalizar los datos.
        """
        self.k = k
        self.norm = norm
    
    def entrenamiento(self, datostrain, nominalAtributos):
        """Entrena el clasificador.

        Args:
            datosTrain (2D np.ndarray): Datos de entrenamiento.
            nominalAtributos (list(boolean)): Lista con los tipos de atributo (nominal o no).
        """
        self.datos = np.copy(datostrain)
        if self.norm:
            self.medias, self.stds = Datos.calcularMediasDesv(self.datos)
            Datos.normalizarDatos(self.datos)
    
    def clasifica(self, datostest, nominalAtributos):
        """Realiza la clasificación de los datos proporcionados.

        Args:
            datosTest (2D np.ndarray): Datos de validación.
            nominalAtributos (list(boolean)): Lista con los tipos de atributo (nominal o no).

        Returns:
            (list(Any)): Lista con las predicciones realizadas por el clasificador.
        """
        predicciones = []

        # Se normalizan los datos de test
        test = datostest.copy()
        if self.norm:
            for j in range(len(self.medias)):
                test[:, j] -= self.medias[j]
                test[:, j] /= self.stds[j]

        # Iterando por cada dato de test
        for i in range(test.shape[0]):
            distancias = []

            for j in range(self.datos.shape[0]):
                # Se guardan las distancias a cada dato de entrenamiento como (dist, clase)
                distancias.append((np.linalg.norm(test[i][:-1] - self.datos[j][:-1]), self.datos[j][-1]))

            distancias.sort(key=lambda x: x[0])

            max_distance = distancias[self.k - 1][0]
            
            # Se escogen los k vecinos más próximos, teniendo cuidado de, si hay
            # algún empate de distancias, escoger los nodos aleatoriamente.
            clases_proximas = []
            clases_limite = []

            for (dist, clase) in distancias:
                if dist < max_distance:
                    clases_proximas.append(clase)
                elif dist == max_distance:
                    clases_limite.append(clase)
                else:
                    break

            clases_proximas += random.sample(clases_limite, self.k - len(clases_proximas))

            # Una vez cogidos los k vecinos más proximos, la predicción es la clase más común
            predicciones.append(max(set(clases_proximas), key=clases_proximas.count))

        return predicciones
