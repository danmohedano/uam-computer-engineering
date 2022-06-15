import numpy as np


class RedNeuronal:
    """RedNeuronal

    Attributes:
        capas(list): Capas que componen la red neuronal.
    """
    def __init__(self):
        self.Inicializar()

    def Inicializar(self):
        self.capas = []

    def AñadirCapa(self, capa):
        """
        Añade capa a la red
        Args:
            capa (Capa): Capa a añadir.
        """
        self.capas.append(capa)

    def Disparar(self):
        """
        Dispara todas las capas.
        """
        for capa in self.capas:
            capa.Disparar()

    def Propagar(self):
        """
        Propaga todas las capas.
        """
        for capa in self.capas:
            capa.Propagar()

    def valores_neuronas(self):
        """
        Devuelve los valores de las neuronas en el estado actual.
        Returns:
            list: Lista de valores
        """
        valores = []
        for c in self.capas:
            for n in c.neuronas:
                valores.append(n.valor_salida)

        return valores

    def entrenamiento_perceptron(self, alpha, epochs, x_train, y_train):
        """
        Entrenamiento de Perceptrón.
        Args:
            alpha: Constante de aprendizaje.
            epochs: Número de épocas.
            x_train: Datos de entrenamiento.
            y_train: Clases de los datos de entrenamiento.
        """
        weights_updated = True
        print('#Epoch\tECM\tAccuracy')
        for epoch in range(epochs):
            if not weights_updated:
                break
            weights_updated = False
            for x, t in zip(x_train, y_train):
                # Establecer activaciones de neuronas de entrada
                for i in range(len(x)):
                    self.capas[0].neuronas[i].valor_entrada = x[i]

                # Calcular respuesta de cada neurona de salida
                self.Disparar()
                self.Propagar()
                self.Disparar()
                self.Propagar()

                # Ajustar pesos y sesgo según error
                for j in range(len(t)):
                    if self.capas[1].neuronas[j].valor_salida != t[j]:
                        weights_updated = True
                        for i in range(len(x)):
                            # Ajustar pesos
                            self.capas[0].neuronas[i].conexiones[j].peso += alpha*t[j]*x[i]

                        # Ajustar sesgo
                        self.capas[0].neuronas[-1].conexiones[j].peso += alpha*t[j]

            # Cálculo ECM
            ecm = 0.0
            accuracy = 0.0

            for x, t in zip(x_train, y_train):
                # Establecer activaciones de neuronas de entrada
                for i in range(len(x)):
                    self.capas[0].neuronas[i].valor_entrada = x[i]

                # Calcular respuesta de cada neurona de salida
                self.Disparar()
                self.Propagar()
                self.Disparar()
                self.Propagar()

                # Comprobar clasificación iterando por cada neurona de salida
                acierto = 1
                for j in range(len(t)):
                    ecm += (self.capas[-1].neuronas[j].valor_salida - t[j])**2
                    if self.capas[-1].neuronas[j].valor_salida != t[j]:
                        acierto = 0
                
                accuracy += acierto
                    
            accuracy /= len(y_train)
            ecm /= len(y_train)

            print(f'{epoch+1}\t{ecm:.4f}\t{accuracy:.4f}')


    def entrenamiento_adaline(self, alpha, epochs, tol, x_train, y_train):
        """
        Entrenamiento de Adaline.
        Args:
            alpha: Constante de aprendizaje.
            epochs: Número de épocas.
            tol: Tolerancia de la condición de parada.
            x_train: Datos de entrenamiento.
            y_train: Clases de los datos de entrenamiento.
        """
        weights_updated = True
        print('#Epoch\tECM\tAccuracy')
        for epoch in range(epochs):
            if not weights_updated:
                break
            weights_updated = False
            
            w_old = [[self.capas[0].neuronas[i].conexiones[j].peso for j in range(len(y_train[0]))] for i in range(len(x_train[0]))]
            
            for x, t in zip(x_train, y_train):
                # Establecer activaciones de neuronas de entrada
                for i in range(len(x)):
                    self.capas[0].neuronas[i].valor_entrada = x[i]

                # Calcular respuesta de cada neurona de salida
                self.Disparar()
                self.Propagar()

                # Ajustar pesos y sesgo
                for j in range(len(t)):
                    y = self.capas[1].neuronas[j].valor_entrada
                    for i in range(len(x)):
                        # Ajustar pesos
                        w_inc = alpha * (t[j] - y) * x[i]
                        self.capas[0].neuronas[i].conexiones[j].peso += w_inc

                    # Ajustar sesgo
                    w_inc = alpha * (t[j] - y)
                    self.capas[0].neuronas[-1].conexiones[j].peso += w_inc

            # Comprobar condición de parada
            for i in range(len(x_train[0])):
                for j in range(len(y_train[0])):
                    if abs(self.capas[0].neuronas[i].conexiones[j].peso - w_old[i][j]) > tol:
                        weights_updated = True


            # Cálculo ECM
            ecm = 0.0
            accuracy = 0.0

            for x, t in zip(x_train, y_train):
                # Establecer activaciones de neuronas de entrada
                for i in range(len(x)):
                    self.capas[0].neuronas[i].valor_entrada = x[i]

                # Calcular respuesta de cada neurona de salida
                self.Disparar()
                self.Propagar()
                
                for j in range(len(t)):
                    ecm += (self.capas[-1].neuronas[j].valor_entrada - t[j])**2

                self.Disparar()
                self.Propagar()

                # Comprobar clasificación iterando por cada neurona de salida
                acierto = 1
                for j in range(len(t)):
                    if self.capas[-1].neuronas[j].valor_salida != t[j]:
                        acierto = 0
                
                accuracy += acierto
                    
            accuracy /= len(y_train)
            ecm /= len(y_train)

            print(f'{epoch+1}\t{ecm:.4f}\t{accuracy:.4f}')

    def test(self, x_test, y_test):
        """
        Evaluación de la red.
        Args:
            x_test: Datos de test.
            y_test: Clases de los datos de test.

        Returns:
            list: Predicciones
        """
        predicciones = []

        for x, t in zip(x_test, y_test):
            # Establecer activaciones de neuronas de entrada
            for i in range(len(x)):
                self.capas[0].neuronas[i].valor_entrada = x[i]

            # Calcular respuesta de cada neurona de salida
            self.Disparar()
            self.Propagar()    
            self.Disparar()
            self.Propagar()

            # Comprobar predicciones
            predicciones.append([self.capas[-1].neuronas[j].valor_salida for j in range(len(t))])            
        
        return predicciones

    @property
    def frontera_decision(self):
        """
        Calculo de las fronteras de decisión de las neuronas de la capa de salida.
        Returns:
            list(str): Lista con las fronteras de decisión para cada neurona de salida.
        """
        fronteras = []
        aux = {-1.0: '', 1.0: '+', 0.0: '+'}
        for j in range(len(self.capas[-1].neuronas)):
            s = ''.join([aux[np.sign(self.capas[0].neuronas[i].conexiones[j].peso)] + f'{self.capas[0].neuronas[i].conexiones[j].peso:.03f}·x{i+1}' for i in range(len(self.capas[0].neuronas) - 1)])  # Limitar hasta el penúltimo ya que el bias es un caso especial
            s += aux[np.sign(self.capas[0].neuronas[-1].conexiones[j].peso)] + f'{self.capas[0].neuronas[-1].conexiones[j].peso:.03f} = 0'
            fronteras.append(s)

        return fronteras
