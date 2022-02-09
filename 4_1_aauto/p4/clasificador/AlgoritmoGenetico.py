from numpy.core.numeric import indices
from clasificador import Clasificador
from Datos import Datos
import numpy as np
import random
import copy


class AlgoritmoGenetico(Clasificador):
    """Clasificador con Algoritmo Genético.
    
    Attributes:
        val_por_attr (list): Posibles valores para cada atributo del conjunto
        de datos.
        m (int): Cantidad de reglas por individuo.
        cruce (str): Tipo de cruce para las reglas ('intra' o 'inter').
        mutacion (str): Tipo de mutación ('std_single', 'std_multi').
        n (int): Tamaño de la población.
        n_epoch (int): Número de épocas de ejecución.
    """

    CRUCES = ['intra', 'inter']
    MUTACIONES = ['std_single', 'std_multi']

    def __init__(self, val_por_attr, m=1, cruce=CRUCES[0], 
                 mutacion=MUTACIONES[0], n=50, n_epoch=100, elitismo=0.05, debug=False):
        """Genera el objeto
        
        Args:
        """
        if cruce not in self.CRUCES:
            raise ValueError(f'El tipo de cruce debe ser uno de los siguientes: {self.CRUCES}')
        if mutacion not in self.MUTACIONES:
            raise ValueError(f'El tipo de mutación debe ser uno de los siguientes: {self.MUTACIONES}')
        
        self.val_por_attr = [sorted(l) for l in val_por_attr]
        self.m = m
        self.tipo_cruce = cruce
        self.tipo_mutacion = mutacion
        self.n = n
        self.n_epoch = n_epoch
        self.debug = debug
        self.elitismo = elitismo

        self._determinar_estructura_reglas()

    def _determinar_estructura_reglas(self):
        """Determina la estructura de las reglas. Configura internamente que
        longitud de cadena es necesaria para cada atributo y la longitud total
        de cada regla.
        """
        self.n_val_attr = [len(x) for x in self.val_por_attr]
        self.long_regla = sum(self.n_val_attr) + 1

    def _generar_poblacion(self):
        """Genera la población de conjuntos de reglas con longitud variable.

        Args:
            valores_por_atributo (list): Posibles valores para cada atributo
        """
        self.poblacion = [None]*self.n

        # Cada individuo de la población se genera de forma aleatoria
        for i in range(self.n):
            # Determinar aleatoriamente cuantas reglas contendrá el individuo
            n_reglas = random.randint(1, self.m)

            # Determinar el individuo de forma aleatoria (cada bit 0 o 1)
            individuo = []
            for j in range(n_reglas):
                regla = [0]*self.long_regla
                while (regla.count(0) == self.long_regla or regla.count(1) == self.long_regla):
                    regla = [random.randint(0, 1) for k in range(self.long_regla)]
                individuo.append(regla)

            self.poblacion[i] = individuo

    def cruce(self, ind1, ind2):
        """Cruce de dos individuos dependiendo del tipo de cruce definido

        Args:
            ind1 (list): Individuo 1.
            ind2 (list): Individuo 2.

        Returns:
            tuple(list): Vástagos generados.
        """
        return getattr(self, '_cruce_' + self.tipo_cruce)(ind1, ind2)

    def _cruce_intra(self, ind1, ind2):
        """Cruce de dos individuos de tipo Intra.

        1. Se elige una regla de cada individuo.
        2. Se escoge un punto de corte.
        3. Se cruzan los individuos solo en la regla seleccionada.

        Args:
            ind1 (list): Individuo 1.
            ind2 (list): Individuo 2.

        Returns:
            tuple(list): Vástagos generados.
        """
        regla_1 = random.randint(0, len(ind1) - 1)
        regla_2 = random.randint(0, len(ind2) - 1)
        punto_corte = random.randint(0, self.long_regla - 1)

        v1 = copy.deepcopy(ind1)
        v2 = copy.deepcopy(ind2)

        v1[regla_1][punto_corte:], v2[regla_2][punto_corte:] = \
            ind2[regla_2][punto_corte:], ind1[regla_1][punto_corte:]

        return v1, v2

    def _cruce_inter(self, ind1, ind2):
        """Cruce de dos individuos de tipo Inter.

        1. Se escoge punto de corte.
        2. Se cruzan los individuos "globalmente" en ese punto (puede afectar a
        varias reglas).

        Args:
            ind1 (list): Individuo 1.
            ind2 (list): Individuo 2.

        Returns:
            tuple(list): Vástagos generados.
        """
        try:
            corte = random.randint(1, min(len(ind1), len(ind2)) - 1)
        except ValueError:
            corte = 1
        
        v1 = copy.deepcopy(ind1)
        v2 = copy.deepcopy(ind2)

        v1[corte:], v2[corte:] = ind2[corte:], ind1[corte:]

        return v1, v2

    def mutacion(self, ind):
        """Mutación de un individuo dependiendo del tipo elegido.

        Args:
            ind (list): Individuo.

        Returns:
            list: Individuo mutado.
        """
        return getattr(self, '_mutacion_' + self.tipo_mutacion)(ind)

    def _mutacion_std_single(self, ind):
        """Mutación de tipo std_single (solo muta una regla).

        Args:
            ind (list): Individuo.

        Returns:
            list: Individuo mutado.
        """
        try:
            regla_mutada = random.randint(0, len(ind) - 1)
        except ValueError:
            regla_mutada = 0

        ind_m = copy.deepcopy(ind)
        p_m = 1.0 / self.long_regla

        for i in range(self.long_regla):
            modificacion = np.random.choice([0, 1], p=[1 - p_m, p_m])
            ind_m[regla_mutada][i] = (ind_m[regla_mutada][i] + modificacion) % 2

        return ind_m

    def _mutacion_std_multi(self, ind):
        """Mutación de tipo std_multi (se pueden mutar todas las reglas).

        Args:
            ind (list): Individuo.

        Returns:
            list: Individuo mutado.
        """
        ind_m = copy.deepcopy(ind)
        p_m = 1.0 / (self.long_regla * len(ind))

        for r in range(len(ind)):
            for i in range(self.long_regla):
                modificacion = np.random.choice([0, 1], p=[1 - p_m, p_m])
                ind_m[r][i] = (ind_m[r][i] + modificacion) % 2

        return ind_m

    def _evaluar_regla(self, rule, data):
        """Evaluar las reglas de un individuo con una regla concreta.

        Args:
            rule (list): Regla
            data (np.ndarray): Dato que evaluar.

        Returns:
            int: Clasificación.
        """
        pos_bit = 0

        for attr in range(len(self.n_val_attr)):
            pos_attr_value = self.val_por_attr[attr].index(data[attr])
            if rule[pos_bit + pos_attr_value] == 0:
                # Default: devolver -1 si la regla no se dispara
                return -1

            pos_bit += self.n_val_attr[attr]


        return rule[-1]

    def evaluar(self, ind, data):
        """Evaluar las reglas de un individuo con un dato concreto.

        Args:
            ind (list): Individuo.
            data (np.ndarray): Dato que evaluar.

        Returns:
            int: Clasificación.
        """
        clasificaciones = []

        for r in ind:
            # Cada regla del individuo se evalua sobre data
            clasificaciones.append(self._evaluar_regla(r, data))

        count_0 = clasificaciones.count(0)
        count_1 = clasificaciones.count(1)

        if count_0 > count_1:
            return 0
        elif count_1 > count_0:
            return 1
        elif count_0 != 0:
            return 0
        else:
            return -1    

    def fitness(self, ind, datostrain):
        """Función de fitness para los individuos definida como el % de 
        aciertos sobre los datos de entrenamiento.

        Args:
            ind (list): Individuo.
            datostrain (np.ndarray): Datos de entrenamiento.

        Returns:
            double: Fitness.
        """

        aciertos = 0

        for i in range(datostrain.shape[0]):
            ev = self.evaluar(ind, datostrain[i])

            if ev == datostrain[i][-1]:
                aciertos += 1

        return aciertos / datostrain.shape[0]

    def entrenamiento(self, datostrain, nominalAtributos):
        """Entrena el clasificador.

        Args:
            datosTrain (2D np.ndarray): Datos de entrenamiento.
            nominalAtributos (list(boolean)): Lista con los tipos de atributo (nominal o no).
        """
        if self.debug:
            print(''.join(['=']*30))

        self.log_best_fitness = []
        self.log_avg_fitness = []

        # 1. Crear población
        self._generar_poblacion()

        # 2. Bucle de generaciones
        for epoch in range(self.n_epoch):
            fitness_generacion = [self.fitness(ind, datostrain) for ind in self.poblacion]

            self.log_best_fitness.append(max(fitness_generacion))
            self.log_avg_fitness.append(np.mean(fitness_generacion))

            if self.debug and (epoch % 5) == 0:
                print(f"GEN {epoch:03}: Max={self.log_best_fitness[-1]:.4f}, Mean={self.log_avg_fitness[-1]:.4f}, Std={np.std(fitness_generacion):.8f}")            

            # 2a. Elitismo
            nueva_poblacion = []

            limite_elitismo = round(self.n * self.elitismo)
            indices_elitismo = np.argpartition(fitness_generacion, -limite_elitismo)[-limite_elitismo:]
            for indice in indices_elitismo:
                nueva_poblacion.append(self.poblacion[indice])

            # 2b. Mientras se necesite: progenitores, cruce y mutación
            while len(nueva_poblacion) < self.n:
                new_inds = random.choices(self.poblacion, fitness_generacion, k=2)
                
                new_inds[0], new_inds[1] = self.cruce(new_inds[0], new_inds[1])

                # Elegir si se mutan o no
                for i in range(2):
                    if random.random() <= (1.0 / self.n): 
                        new_inds[i] = self.mutacion(new_inds[i])

                # Se añaden a la nueva población
                for i in range(2):
                    if len(nueva_poblacion) < self.n:
                        nueva_poblacion.append(new_inds[i])
                
            self.poblacion = nueva_poblacion
        
        fitness_generacion = [self.fitness(ind, datostrain) for ind in self.poblacion]
        self.best_ind = self.poblacion[np.argpartition(fitness_generacion, -1)[-1:][0]]

        if self.debug:
            print(f"GEN {epoch:03}: Max={max(fitness_generacion):.4f}, Mean={np.mean(fitness_generacion):.4f}, Std={np.std(fitness_generacion):.8f}")
        
        return
    
    def clasifica(self, datostest, nominalAtributos):
        """Realiza la clasificación de los datos proporcionados.

        Args:
            datosTest (2D np.ndarray): Datos de validación.
            nominalAtributos (list(boolean)): Lista con los tipos de atributo (nominal o no).

        Returns:
            (list(Any)): Lista con las predicciones realizadas por el clasificador.
        """
        predicciones = []

        for i in range(datostest.shape[0]):
            ev = self.evaluar(self.best_ind, datostest[i])
            predicciones.append(ev)
        
        return predicciones
