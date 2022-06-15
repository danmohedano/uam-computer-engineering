from numpy import random


class Capa:
    """Capa
    
    Attributes:
        neuronas(list): Neuronas de la capa.
    """

    def __init__(self):
        self.Inicializar()

    def Inicializar(self):
        self.neuronas = []

    def Añadir(self, neurona):
        self.neuronas.append(neurona)

    # conectar esta capa a la capa parámetro
    def ConectarCapa(self, capa, peso_min, peso_max):
        peso = random.uniform(peso_min, peso_max)
        for n in self.neuronas:
            for n2 in capa.neuronas:
                n.Conectar(n2, peso)

    # Conexión de capa -> neurona
    def ConectarNeurona(self, neurona, peso_min, peso_max):
        peso = random.uniform(peso_min, peso_max)
        for n in self.neuronas:
            n.Conectar(neurona, peso)

    def Disparar(self):
        for neurona in self.neuronas:
            neurona.Disparar()

    def Propagar(self):
        for neurona in self.neuronas:
            neurona.Propagar()
