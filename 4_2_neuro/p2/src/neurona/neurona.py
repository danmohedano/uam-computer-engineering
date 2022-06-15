from abc import ABC, abstractmethod
from .conexion import Conexion

class Neurona(ABC):
    """Neurona
    
    Attributes:
        umbral (float): Umbral de activación.
        valor_entrada (float): Valor de entrada.
        valor_salida (float): Valor de salida.
        conexiones (list): Conexiones desde esta neurona.
    """
    def __init__(self, umbral=0):
        self.umbral = umbral
        self.conexiones = []
        self.valor_entrada = 0.0
        self.valor_salida = 0.0

    def Inicializar(self):
        """
        Inicializa la neurona restaurando sus valores internos.
        Args:
            x (int): Umbral
        """
        self.valor_entrada = 0
    
    def Conectar(self, neurona, peso):
        """
        Crea una conexion entre las dos neuronas.
        Args:
            neurona: Neurona objetivo.
            peso: Peso de la conexión.
        """
        self.conexiones.append(Conexion(peso, neurona))

    @abstractmethod
    def Disparar(self):
        """
        Decide cuál va a ser el valor a propagar en función de cuál es el valor almacenado en su entrada
        """
        pass

    def Propagar(self):
        """
        Envía su salida a todas las conexiones, sumándolo a sus entradas
        """
        for conexion in self.conexiones:
            conexion.Propagar(self.valor_salida)


class NeuronaDirecta(Neurona):
    def Disparar(self):
        """
        Decide cuál va a ser el valor a propagar en función de cuál es el valor almacenado en su entrada
        """
        self.valor_salida = self.valor_entrada
        self.valor_entrada = 0.0


class NeuronaSesgo(Neurona):
    def __init__(self, umbral=1.0):
        super().__init__(umbral)
        self.valor_salida = 1.0

    def Disparar(self):
        pass


class NeuronaMC(Neurona):
    def Disparar(self):
        """
        Decide cuál va a ser el valor a propagar en función de cuál es el valor almacenado en su entrada
        """
        self.valor_salida = 1.0 if self.valor_entrada >= self.umbral else 0.0
        self.valor_entrada = 0.0


class NeuronaAdaline(Neurona):
    def Disparar(self):
        """
        Decide cuál va a ser el valor a propagar en función de cuál es el valor almacenado en su entrada
        """
        self.valor_salida = 1.0 if self.valor_entrada >= 0 else -1.0
        self.valor_entrada = 0.0
    
    
class NeuronaPerceptron(Neurona):
    def Disparar(self):
        """
        Decide cuál va a ser el valor a propagar en función de cuál es el valor almacenado en su entrada
        """
        if (-1)*self.umbral <= self.valor_entrada <= self.umbral:
            self.valor_salida = 0.0
        else:
            self.valor_salida = 1.0 if self.valor_entrada > self.umbral else -1.0
               
        self.valor_entrada = 0.0


class NeuronaGenerica(Neurona):
    def __init__(self, fn_activacion, fn_activacion_2):
        super().__init__()
        self.fn = fn_activacion
        self.fn_activacion_2 = fn_activacion_2

    def Disparar(self):
        self.valor_salida = self.fn(self.valor_entrada)

    def fn_2(self, x):
        return self.fn_activacion_2(x, self)