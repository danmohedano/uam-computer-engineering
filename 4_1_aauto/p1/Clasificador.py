from abc import ABCMeta,abstractmethod
import numpy as np
from scipy.stats import norm


class Clasificador:
    """Clase abstracta para la implementación de clasificadores.
    """
  
    # Clase abstracta
    __metaclass__ = ABCMeta
  
    @abstractmethod
    def entrenamiento(self, datosTrain, nominalAtributos):
        """Realiza el entrenamiento del clasificador.

        Args:
            datosTrain (2D np.ndarray): Datos de entrenamiento.
            nominalAtributos (list(boolean)): Lista con los tipos de atributo (nominal o no).
        """
        pass
  
    @abstractmethod
    def clasifica(self, datosTest, nominalAtributos):
        """Realiza la clasificación de los datos proporcionados.

        Args:
            datosTest (2D np.ndarray): Datos de validación.
            nominalAtributos (list(boolean)): Lista con los tipos de atributo (nominal o no).

        Returns:
            (list(Any)): Lista con las predicciones realizadas por el clasificador.
        """
        pass
  
    def error(self, datos, pred):
        """Calcula el porcentaje de error entre los datos y la predicción.

        Args:
            datos (2D np.ndarray): Datos utilizados en la validación.
            pred (list(Any)): Predicciones realizadas por el clasificador.

        Returns:
            (float): Porcentaje de error cometido.
        """
        # Aqui se compara la prediccion (pred) con las clases reales y se calcula el error
        n_errors = 0    
        for i in range(len(pred)):
            if datos[i][-1] != pred[i]:
                n_errors += 1
        
        return n_errors / len(pred)
            
    def validacion(self, particionado, dataset, seed=None):
        """Realiza la validación siguiendo una estrategia de particionado determinada.

        Args:
            particionado (EstrategiaParticionado): Estrategia de particionado elegida para la validación.
            dataset (Datos): Datos que validar.
            seed (Any): Semilla para la generación de particiones.

        Returns:
            (float): Error medio obtenido en la validación.
            (float): Desviación típica del error medio obtenido.
        """
        errores = []
        particiones = particionado.creaParticiones(dataset, seed)

        for particion in particiones:
            datos_train = dataset.extraeDatos(particion.indicesTrain).to_numpy()
            datos_test = dataset.extraeDatos(particion.indicesTest).to_numpy()

            self.entrenamiento(datos_train, dataset.nominalAtributos)
            predicciones = self.clasifica(datos_test, dataset.nominalAtributos)

            errores.append(self.error(datos_test, predicciones))
        
        return np.mean(errores), np.std(errores)

##############################################################################

class ClasificadorNaiveBayes(Clasificador):
    """Clasificador Naive Bayes
    
    Attributes:
        laplace (boolean): Flag para determinar el uso o no de la corrección de Laplace.
    """


    def __init__(self, laplace=False):
        """Genera el objeto
        
        Args:
            laplace (boolean): Flag para determinar el uso o no de la corrección de Laplace.
        """
        self.laplace = laplace
  

    
    def entrenamiento(self, datostrain, nominalAtributos):
        """Entrena el clasificador de Naive Bayes construyendo las tablas.

        Args:
            datosTrain (2D np.ndarray): Datos de entrenamiento.
            nominalAtributos (list(boolean)): Lista con los tipos de atributo (nominal o no).
        """
        self.tablas = []
        self.vals_atributo_dicts = [None] * (len(nominalAtributos) - 1)
        
        # Calcular cantidad de valores para la clase
        vc = np.unique(datostrain[:,-1])
        self.vals_clase_dict = {vc[x]: x for x in range(len(vc))}
        self.prioris = np.zeros(len(self.vals_clase_dict))

        # Inicializar las tablas a 0 (o a 1 si se aplica Laplace)
        for i in range(len(nominalAtributos) - 1):
            if nominalAtributos[i]:
                va = np.unique(datostrain[:,i])
                # Se guardan los posibles valores del atributo
                self.vals_atributo_dicts[i] = {va[x]: x for x in range(len(va))}
                if self.laplace:
                    self.tablas.append(np.ones((len(va), len(self.vals_clase_dict))))
                else:
                    self.tablas.append(np.zeros((len(va), len(self.vals_clase_dict))))
            else:
                # Si el atributo no es nominal, la tabla solo tiene 2 filas (media y desviación típica)
                self.tablas.append(np.zeros((2, len(self.vals_clase_dict))))

        # Rellenar las tablas con los valores
        for j in range(len(nominalAtributos) - 1):
            if nominalAtributos[j]:
                # Se rellena por conteo
                for i in range(datostrain.shape[0]):
                    fila = self.vals_atributo_dicts[j][datostrain[i][j]] 
                    columna = self.vals_clase_dict[datostrain[i][-1]]
                    self.tablas[j][fila][columna] += 1
            else:
                # Se rellena la tabla con la media y desviación típica
                for c in self.vals_clase_dict:
                    # Se calcula para cada valor de la clase
                    idxs = np.where(datostrain[:,-1] == c)[0]

                    self.tablas[j][0][self.vals_clase_dict[c]] = np.mean(datostrain[idxs, j])
                    self.tablas[j][1][self.vals_clase_dict[c]] = np.std(datostrain[idxs, j])

        # Calcular prioris
        for c, idx in self.vals_clase_dict.items():
            self.prioris[idx] = (np.count_nonzero(datostrain[:,-1] == c)) / (datostrain.shape[0])
    
    
    def clasifica(self,datostest,nominalAtributos):
        """Realiza la clasificación de los datos proporcionados.

        Args:
            datosTest (2D np.ndarray): Datos de validación.
            nominalAtributos (list(boolean)): Lista con los tipos de atributo (nominal o no).

        Returns:
            (list(Any)): Lista con las predicciones realizadas por el clasificador.
        """
        predicciones = []

        # Para cada dato se realiza la predicción
        for dato_idx in range(datostest.shape[0]):
            pred_max = 0
            pred = None

            # Calcular MAP para cada una de las hipótesis
            for h, h_idx in self.vals_clase_dict.items():
                pred_h = 1

                # Calcular P(D|H) para cada atributo
                for atr in range(len(nominalAtributos) - 1):
                    if nominalAtributos[atr]:
                        # Se calcula la frecuencia
                        atr_idx = self.vals_atributo_dicts[atr][datostest[dato_idx][atr]]
                        n_atr = self.tablas[atr][atr_idx][h_idx]
                        n_total = np.sum(self.tablas[atr][:,h_idx])
                        pred_h *= n_atr / n_total
                    else:
                        # Se estima la probabilidad con una normal
                        dist = norm(self.tablas[atr][0][h_idx], self.tablas[atr][1][h_idx])
                        pred_h *= dist.pdf(datostest[dato_idx][atr])

                # Multiplicar por P(H)
                pred_h *= self.prioris[h_idx]

                if pred_h > pred_max:
                    pred_max = pred_h
                    pred = h

            # Se guarda la hipótesis con mayor probabilidad como la predicción
            predicciones.append(pred)

        return predicciones