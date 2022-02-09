from abc import ABCMeta,abstractmethod
import numpy as np


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

