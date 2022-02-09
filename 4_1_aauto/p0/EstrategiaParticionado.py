from abc import ABCMeta,abstractmethod
import random
import math


class Particion():

    # Esta clase mantiene la lista de �ndices de Train y Test para cada partici�n del conjunto de particiones  
    def __init__(self):
        self.indicesTrain=[]
        self.indicesTest=[]

#####################################################################################################

class EstrategiaParticionado:
  
    # Clase abstracta
    __metaclass__ = ABCMeta
    
    # Atributos: deben rellenarse adecuadamente para cada estrategia concreta. Se pasan en el constructor 
    @abstractmethod
    def __init__(self):
        pass
    
    @abstractmethod 
    def creaParticiones(self,datos,seed=None):
        pass
  

#####################################################################################################

class ValidacionSimple(EstrategiaParticionado):

    def __init__(self, proporcionTest, nEjecuciones):
        self.proporcionTest = proporcionTest
        self.nEjecuciones = nEjecuciones
    
    # Crea particiones segun el metodo tradicional de division de los datos segun el porcentaje deseado y el n�mero de ejecuciones deseado
    # Devuelve una lista de particiones (clase Particion)
    def creaParticiones(self,datos,seed=None):
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

    def __init__(self, nParticiones):
        self.nParticiones = nParticiones
    
    # Crea particiones segun el metodo de validacion cruzada.
    # El conjunto de entrenamiento se crea con las nfolds-1 particiones y el de test con la particion restante
    # Esta funcion devuelve una lista de particiones (clase Particion)
    # TODO: implementar
    def creaParticiones(self,datos,seed=None):   
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