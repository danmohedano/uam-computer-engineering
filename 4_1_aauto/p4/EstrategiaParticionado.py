from abc import ABCMeta,abstractmethod
import random
import math


class Particion():
    """Contiene los índices de Train y Test para poder realizar entrenamiento y validación.

    Attributes:
        indicesTrain (list(int)): Índices utilizados para el entrenamiento.
        indicesTest (list(int)): Índices utilizados para la validación.
    """

    def __init__(self):
        """Creación del objeto
        """
        self.indicesTrain=[]
        self.indicesTest=[]

#####################################################################################################

class EstrategiaParticionado:
    """Estrategia de particionado encargada de generar las particiones para la validación.
    """
  
    # Clase abstracta
    __metaclass__ = ABCMeta
    
    # Atributos: deben rellenarse adecuadamente para cada estrategia concreta. Se pasan en el constructor 
    @abstractmethod
    def __init__(self):
        pass
    
    @abstractmethod 
    def creaParticiones(self,datos,seed=None):
        """Genera las particiones siguiendo la estrategia que se utilice.

        Args:
            datos (pd.DataFrame): Datos de los que generar las particiones.
            seed (any): Seed para la generación pseudo-aleatoria de las particiones.

        Returns:
            (list(Particion)): Lista con las particiones generadas. 
        """
        pass
  

#####################################################################################################

class ValidacionSimple(EstrategiaParticionado):
    """Estrategia de particionado simple.
    
    Attributes:
        proporcionTest (float): Proporción de los datos utilizados para la validación.
        nEjecuciones (int): Número de ejecuciones realizadas en la validación.
    """

    def __init__(self, proporcionTest, nEjecuciones):
        """Genera el objeto

        Args:
            proporcionTest (float): Proporción de los datos utilizados para la validación.
            nEjecuciones (int): Número de ejecuciones realizadas en la validación.
        """
        self.proporcionTest = proporcionTest
        self.nEjecuciones = nEjecuciones
    
    def creaParticiones(self, datos, seed=None):
        """Genera las particiones siguiendo una estrategia simple.

        Args:
            datos (pd.DataFrame): Datos de los que generar las particiones.
            seed (any): Seed para la generación pseudo-aleatoria de las particiones.

        Returns:
            (list(Particion)): Lista con las particiones generadas. 
        """
        random.seed(seed)
        particiones = []
        indices = list(range(datos.shape[0]))
        division = math.floor(len(indices) * self.proporcionTest)

        # Se crea una partición nueva para cada ejecución
        for i in range(self.nEjecuciones):
            # Se permutan los índices
            random.shuffle(indices)
            
            # Se toma la proporción deseada
            p = Particion()
            p.indicesTest = indices[:division]
            p.indicesTrain = indices[division:]
            particiones.append(p)

        return particiones
    
      
#####################################################################################################      
class ValidacionCruzada(EstrategiaParticionado):
    """Estrategia de particionado basada en validación cruzada.
    
    Attributes:
        nParticiones (int): Número de divisiones realizadas.
    """

    def __init__(self, nParticiones):
        """Genera el objeto

        Args:
            nParticiones (int): Número de divisiones realizadas.
        """
        self.nParticiones = nParticiones
    
    def creaParticiones(self, datos, seed=None):
        """Genera las particiones siguiendo una estrategia simple.

        Args:
            datos (pd.DataFrame): Datos de los que generar las particiones.
            seed (any): Seed para la generación pseudo-aleatoria de las particiones.

        Returns:
            (list(Particion)): Lista con las particiones generadas. 
        """   
        random.seed(seed)
        particiones = []
        indices = list(range(datos.shape[0]))
        random.shuffle(indices)
        divisiones = [0]

        # Se calculan las divisiones para cada grupo
        for i in range(self.nParticiones):
            divisiones.append(divisiones[i] + math.ceil((len(indices) - divisiones[i]) / (self.nParticiones - i)))

        # Se generan las particiones
        for i in range(self.nParticiones):
            p = Particion()
            # Se asigna el grupo i a Test
            p.indicesTest = indices[divisiones[i]:divisiones[i+1]]
            # El resto de grupos se asignan a Train
            p.indicesTrain = indices[0:divisiones[i]] + indices[divisiones[i+1]:len(indices)]
            particiones.append(p)

        return particiones