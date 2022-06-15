import numpy as np
import copy


class RedNeuronal:
    """RedNeuronal

    Attributes:
        capas(list): Capas que componen la red neuronal.
    """
    def __init__(self):
        self.capas = []

    def Inicializar(self):
        for capa in self.capas:
            capa.Inicializar()

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

    def retropropagacion(self, alpha, epochs, wait, x_train, y_train, x_val, y_val, conf):
        """
        Algoritmo de retropropagación.
        Args:
            alpha: Constante de aprendizaje.
            epochs: Máximo número de épocas.
            wait: Paciencia de la condición de parada.
            x_train: Patrones de entrenamiento.
            y_train: Clases de entrenamiento.
            x_val: Patrones de validación.
            y_val: Clases de validación.
            conf: Si deben generarse las matrices de confusión.
        Returns:

        """
        accuracy_val_max = 0
        wait_counter = 0

        if x_val is not None:
            print('#Epoch\tECM\tAcc(Train)\tAcc(Validation)')
        else:
            print('#Epoch\tECM\tAcc(Train)')

        for epoch in range(epochs):
            for x, t in zip(x_train, y_train):
                self.Inicializar()
                # FeedForward
                # Establecer activaciones de la entrada                    
                for i in range(len(x)):
                    self.capas[0].neuronas[i].valor_entrada = x[i]

                # Propagar la información completamente
                for capa in self.capas:
                    capa.Disparar()
                    capa.Propagar()

                # Retropropagación de errores y actualización de pesos
                # Capa de salida
                deltas = []
                for k in range(len(self.capas[-1].neuronas)):
                    # Cálculo del error
                    neurona_k = self.capas[-1].neuronas[k]
                    deriv = neurona_k.fn_2(neurona_k.valor_entrada)
                    delta_k = (t[k] - neurona_k.valor_salida)*deriv
                    deltas.append(delta_k)

                    # Cálculo de la corrección del peso
                    for j in range(len(self.capas[-2].neuronas)):
                        neurona_j = self.capas[-2].neuronas[j]
                        delta_wjk = alpha*delta_k*neurona_j.valor_salida
                        neurona_j.conexiones[k].peso_anterior = neurona_j.conexiones[k].peso
                        neurona_j.conexiones[k].peso += delta_wjk

                
                # Resto de capas ocultas
                for c in range(len(self.capas) - 2, 0, -1):
                    # Cada neurona j de la capa oculta
                    deltas_nuevos = []
                    for j in range(len(self.capas[c].neuronas) - 1):
                        neurona_j = self.capas[c].neuronas[j]
                        
                        # Cálculo del error
                        delta_in_j = sum([deltas[k]*neurona_j.conexiones[k].peso_anterior for k in range(len(deltas))])
                        delta_j = delta_in_j*neurona_j.fn_2(neurona_j.valor_entrada)
                        deltas_nuevos.append(delta_j)
                        
                        for i in range(len(self.capas[c-1].neuronas)):
                            neurona_i = self.capas[c-1].neuronas[i]
                            delta_vij = alpha*delta_j*neurona_i.valor_salida
                            neurona_i.conexiones[j].peso_anterior = neurona_i.conexiones[j].peso
                            neurona_i.conexiones[j].peso += delta_vij
                            
                    deltas = deltas_nuevos
                
            # Cálculo ECM y Accuracy sobre train
            ecm = 0.0
            accuracy_train = 0.0

            for x, t in zip(x_train, y_train):
                self.Inicializar()
                # Establecer activaciones de neuronas de entrada
                for i in range(len(x)):
                    self.capas[0].neuronas[i].valor_entrada = x[i]

                # Propagar la información completamente
                for capa in self.capas:
                    capa.Disparar()
                    capa.Propagar()

                # Comprobar clasificación iterando por cada neurona de salida
                salidas = []
                for j in range(len(t)):
                    ecm += (self.capas[-1].neuronas[j].valor_salida - t[j])**2
                    salidas.append(self.capas[-1].neuronas[j].valor_salida)
      
                if t[np.argmax(salidas)] == 1:
                    accuracy_train += 1
                
            accuracy_train /= len(y_train)
            ecm /= len(y_train)

            if x_val is not None:
                # Accuracy conjunto de validación
                salidas_validacion = self.evaluar(x_val)
                accuracy_val = 0
                for i in range(len(salidas_validacion)):
                    if y_val[i][np.argmax(salidas_validacion[i])] == 1:
                        accuracy_val += 1

                accuracy_val /= len(y_val)

                print(f'{epoch+1}\t{ecm:.4f}\t{accuracy_train:.4f}\t{accuracy_val:.4f}')

                if conf:
                    with open('matrices_confusion.txt', 'a') as f:
                        f.write(f'{self.matriz_confusion(salidas_validacion, y_val)}\n')

                # Comprobación de la condición de parada
                if accuracy_val_max < accuracy_val:
                    # Si se mejora el accuracy, resetear paciencia
                    wait_counter = 0
                    accuracy_val_max = accuracy_val
                else:
                    wait_counter += 1
                    if wait_counter >= wait:
                        break
            else:
                print(f'{epoch+1}\t{ecm:.4f}\t{accuracy_train:.4f}')
               
    def evaluar(self, x_test):
        """
        Evaluación de la red.
        Args:
            x_test: Datos de test.

        Returns:
            list: Predicciones
        """
        predicciones = []

        for x in x_test:
            # Establecer activaciones de neuronas de entrada
            self.Inicializar()
            for i in range(len(x)):
                self.capas[0].neuronas[i].valor_entrada = x[i]

            # Propagar la información completamente
            for capa in self.capas:
                capa.Disparar()
                capa.Propagar()

            # Comprobar predicciones
            predicciones.append([n.valor_salida for n in self.capas[-1].neuronas])            
        
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

    @property
    def pesos(self):
        pesos = []
        for n in self.capas[-2].neuronas:
            pesos.append([x.peso for x in n.conexiones])

        return pesos

    @staticmethod
    def matriz_confusion(predicciones, clases):
        matriz = np.zeros([len(clases[0]), len(clases[0])])

        for i in range(len(predicciones)):
            matriz[np.argmax(clases[i]), np.argmax(predicciones[i])] += 1

        return matriz
