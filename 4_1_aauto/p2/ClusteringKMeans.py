import numpy as np
import random


class KMeans:
    """Implementación del algoritmo de clustering KMeans

    Attributes:
        k (int): Cantidad de clusters deseada
    """
    def __init__(self, k = 1):
        self.k = k

    def cluster(self, datos_cluster):
        """Aplica el clustering a los datos proporcionados

        Args:
            datos_cluster (Datos): Datos a agrupar.
        
        Returns:
            list: Cluster al que pertenece cada dato.
        """
        # Se extraen los datos de la clase
        datos = datos_cluster.datos.iloc[:,datos_cluster.datos.columns != 'Class']

        clusters = [-1]*datos.shape[0]

        # Elegir centroides aleatoriamente
        centroides = []
        for i in range(self.k):
            centroides.append(datos.iloc[random.randint(0, datos.shape[0] - 1)])

        stop_flag = False
        while not stop_flag:
            stop_flag = True

            # Para cada dato
            for i in range(datos.shape[0]):
                # Se calcula la distancia a cada centroide y se guarda como (dist, centroide)
                distancias = []
                for j in range(self.k):
                    distancias.append((np.linalg.norm(datos.iloc[i] - centroides[j]), j))

                # Se añade el punto al centroide más cercano
                new_cluster = min(set(distancias), key=lambda x: x[0])[1]

                if clusters[i] != new_cluster:
                    stop_flag = False
                    clusters[i] = new_cluster

            # Se recalculan los centroides
            for j in range(self.k):
                puntos_contenidos = [i for i in range(len(clusters)) if clusters[i] == j]
                centroides[j] = datos.iloc[puntos_contenidos].mean(axis=0)

        return clusters
