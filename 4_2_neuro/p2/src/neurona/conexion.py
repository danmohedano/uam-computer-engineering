

class Conexion:
    """Conexion
    
    Attributes:
        peso (float): Peso de la conexión.
        peso_anterior (float): Peso anterior de la conexión.
        neurona (Neurona): Nuerona objetivo de la conexión.
        valor (float): Valor en la conexión.
    """
    def __init__(self, peso, neurona):
        self.peso = peso
        self.neurona = neurona
        self.peso_anterior = self.peso

    def Propagar(self, valor):
        # Se almacena el valor y se suma a la entrada de la neurona objetivo
        self.valor = valor
        self.neurona.valor_entrada += (self.peso * self.valor)
