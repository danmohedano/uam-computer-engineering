write_log(S) :- open('error_logs.txt', append, Out), write(Out, S), write(Out, '\n'), close(Out).

/***************
* EJERCICIO 1. sum_pot_prod/4
*
*	ENTRADA:
*		X: Vector de entrada de numeros de valor real.
*		Y: Vector de entrada de numeros de valor real.
*		Potencia: Numero de valor entero, potencia.
*	SALIDA:
*		Resultado: Numero de valor real resultado de la operacion sum_pot_prod. 
*
****************/
/* Error checking */
sum_pot_prod(L1, L2, _, _) :- length(L1, N1), length(L2, N2), dif(N1, N2), write_log('ERROR 1.2 Longitud'), !, fail.
sum_pot_prod(_, _, Potencia, _) :- Potencia < 0, write_log('ERROR 1.1 Potencia.'), !, fail.

/* Main rule */
sum_pot_prod(L1, L2, Potencia, Resultado) :- sum_pot_prod_calc(L1, L2, Potencia, Resultado).

/* Base case of the recursion */
sum_pot_prod_calc([], [], _, 0).

/* Recursion rule */
sum_pot_prod_calc([Xi|X], [Yi|Y], Potencia, Resultado) :- 
    sum_pot_prod_calc(X, Y, Potencia, R2), 
    Ri is (Xi*Yi)**Potencia, 
    Resultado is R2+Ri, 
    !.

/***************
* EJERCICIO 2. segundo_penultimo/3
*
*       ENTRADA:
*               L: Lista de entrada de numeros de valor real.
*       SALIDA:
*               X : Numero de valor real. Segundo elemento.
*		        Y : Numero de valor real. Penultimo elemento.
*
****************/

/* Error checking */
segundo_penultimo([], _, _) :- write_log('ERROR 2.1 Longitud.'), !, fail.
segundo_penultimo([_], _, _) :- write_log('ERROR 2.1 Longitud.'), !, fail.

/* Main rule */
segundo_penultimo(L, X, Y) :- segundo(L, X), penultimo(L, Y), !.

/* Base case for the recursion of penultimate */
penultimo([Penultimo,_|[]], Y) :- Y is Penultimo.

/* Recursive search for penultimate */
penultimo([_|Rest], Y) :- penultimo(Rest, Y).

/* Second rule */
segundo([_,S|_], X) :- X is S. 

/***************
* EJERCICIO 3. sublista/5
*
*       ENTRADA:
*		L: Lista de entrada de cadenas de texto.
*		Menor: Numero de valor entero, indice inferior.
*		Mayor: Numero de valor entero, indice superior.
*		E: Elemento, cadena de texto.
*       SALIDA:
*		Sublista: Sublista de salida de cadenas de texto.
*
****************/
/* Error checking */
sublista(_, Menor, _, _, _) :- Menor < 1, write_log('ERROR 3.2 Indices'), !, fail.
sublista(_, Menor, Mayor, _, _) :- Menor > Mayor, write_log('ERROR 3.2 Indices'), !, fail.
sublista(L, _, Mayor, _, _) :- length(L, X), Mayor > X, write_log('ERROR 3.2 Indices'), !, fail.

/* Main rule */
sublista(L, Menor, Mayor, E, Sublista) :-
    sublista_calc(L, Menor, Mayor, E, Sublista),
    contains(E, Sublista),
    !.   

/* Recursive calculation of contains */
contains(E, [E|_]).
contains(E, [_|Rest]) :- contains(E, Rest).
contains(_, []) :- write_log('ERROR 3.1 Elemento'), !, fail.

/* Search for the start of the sublist */
sublista_calc([_|Rest], Menor, Mayor, E, Sublista) :- 
    Menor > 1, 
    NewMenor is Menor-1, 
    NewMayor is Mayor-1, 
    sublista_calc(Rest, NewMenor, NewMayor, E, Sublista), 
    member(E, Sublista), 
    !.

/* Build the sublist until its end */
sublista_calc([First|Rest], Menor, Mayor, E, Sublista) :- 
    Menor is 1, 
    Mayor > 1, 
    NewMayor is Mayor-1, 
    Sublista = [First|SubSublista], 
    sublista_calc(Rest, Menor, NewMayor, E, SubSublista).
sublista_calc([First|_], 1, 1, _, [First]).

/***************
* EJERCICIO 4. espacio_lineal/4
*
*       ENTRADA:
*               Menor: Numero de valor entero, valor inferior del intervalo.
*               Mayor: Numero de valor entero, valor superior del intervalo.
*               Numero_elementos: Numero de valor entero, numero de valores de la rejilla.
*       SALIDA:
*               Rejilla: Vector de numeros de valor real resultante con la rejilla.
*
****************/
/* Error checking */
espacio_lineal(Menor, Mayor, _, _) :- Menor > Mayor, write_log('ERROR 4.1 Indices'), !, fail.
espacio_lineal(_, _, Numero_elementos, _) :- Numero_elementos < 1, write_log('ERROR 4.2 Numero elementos'), !, fail.

/* Main rule */
espacio_lineal(Menor, Mayor, Numero_elementos, Rejilla) :- Step is (Mayor-Menor)/(Numero_elementos-1), espacio_lineal_calc(Menor, Mayor, Numero_elementos, Rejilla, Step), !.

/* Recurisive generation of a list containing equally spaced elements with 'Step'*/
espacio_lineal_calc(Menor, Mayor, N_elem, Rejilla, Step) :- 
    N_elem > 0,
    Rejilla = [Menor|NextRejilla],
    NewMenor is Menor+Step,
    NewN_elem is N_elem-1,
    espacio_lineal_calc(NewMenor, Mayor, NewN_elem, NextRejilla, Step).
espacio_lineal_calc(_, _, 0, [], _).

/***************
* EJERCICIO 5. normalizar/2
*
*       ENTRADA:
*		Distribucion_sin_normalizar: Vector de numeros reales de entrada. Distribucion sin normalizar.
*       SALIDA:
*		Distribucion: Vector de numeros reales de salida. Distribucion normalizada.
*
****************/
/* Main rule */
normalizar(Distribucion_sin_normalizar, Distribucion) :- sum_dist(Distribucion_sin_normalizar, Z), normalizar_calc(Distribucion_sin_normalizar, Z, Distribucion), !.

/* Recursive calculation of the summation of the distribution */
sum_dist([], 0).
sum_dist([First|_], _) :-
    First < 0,
    write_log('ERROR 5.1 Negativos'),
    !,
    fail.
sum_dist([First|Rest], Z) :-
    sum_dist(Rest, Z2),
    Z is Z2+First.

/* Recursive generation of the normalized distribution */
normalizar_calc([], _, []).
normalizar_calc([First|Rest], Z, Normalizada) :-
    Element is First/Z,
    Normalizada = [Element|NextNormalizada],
    normalizar_calc(Rest, Z, NextNormalizada).


/***************
* EJERCICIO 6. divergencia_kl/3
*
*       ENTRADA:
*		D1: Vector de numeros de valor real. Distribucion.
*		D2: Vector de numeros de valor real. Distribucion.
*       SALIDA:
*		KL: Numero de valor real. Divergencia KL.
*
****************/
/* Calculation of the summation of a list */
sum_list([], 0).
sum_list([First|Rest], S) :-
    sum_list(Rest, S2),
    S is First+S2.

/* Error checking */
divergencia_kl(D1, _, _) :- sum_list(D1, Z), dif(Z, 1.0), write_log('ERROR 6.2 Divergencia KL definida solo para distribuciones'), !, fail.
divergencia_kl(_, D2, _) :- sum_list(D2, Z), dif(Z, 1.0), write_log('ERROR 6.2 Divergencia KL definida solo para distribuciones'), !, fail.
divergencia_kl(D1, D2, _) :- length(D1, L1), length(D2, L2), dif(L1, L2), write_log('ERROR 6.3 Longitudes'), !, fail.

/* Main rule */
divergencia_kl(D1, D2, KL) :- divergencia_kl_calc(D1, D2, KL), !.

/* Recursive calculation of the operation */
divergencia_kl_calc([], [], 0).
divergencia_kl_calc([First|_], _, _) :- First =< 0, write_log('ERROR 6.1 Divergencia KL no definida'), !, fail.
divergencia_kl_calc(_, [First|_], _) :- First =< 0, write_log('ERROR 6.1 Divergencia KL no definida'), !, fail.
divergencia_kl_calc([F1|D1], [F2|D2], KL) :-
    divergencia_kl_calc(D1, D2, KL2),
    Division is F1/F2,
    KL is KL2+(F1*log(Division)).



/***************
* EJERCICIO 7. producto_kronecker/3
*
*       ENTRADA:
*		Matriz_A: Matriz de numeros de valor real.
*		Matriz_B: Matriz de numeros de valor real.
*       SALIDA:
*		Matriz_bloques: Matriz de bloques (matriz de matrices) de numeros reales.
*
****************/
/*producto_kronecker(Matriz_A, Matriz_B, Matriz_bloques) :- print('Error. Este ejercicio no esta implementado todavia.'), !, fail.*/

/***************
* EJERCICIO 8a. distancia_euclidea/3
*
*       ENTRADA:
*               X1: Vector de numeros de valor real. 
*               X2: Vector de numeros de valor real.
*       SALIDA:
*               D: Numero de valor real. Distancia euclidea.
*
****************/
/*distancia_euclidea(X1, X2, D) :- print('Error. Este ejercicio no esta implementado todavia.'), !, fail.*/

/***************
* EJERCICIO 8b. calcular_distancias/3
*
*       ENTRADA:
*               X_entrenamiento: Matriz de numeros de valor real donde cada fila es una instancia representada por un vector.
*               X_test: Matriz de numeros de valor real donde cada fila es una instancia representada por un vector. Instancias sin etiquetar.
*       SALIDA:
*               Matriz_resultados: Matriz de numeros de valor real donde cada fila es un vector con la distancia de un punto de test al conjunto de entrenamiento X_entrenamiento.
*
****************/
/*calcular_distancias(X_entrenamiento, X_test, Matriz_resultados) :- print('Error. Este ejercicio no esta implementado todavia.'), !, fail.*/

/***************
* EJERCICIO 8c. predecir_etiquetas/4
*
*       ENTRADA:
*               Y_entrenamiento: Vector de valores alfanumericos de una distribucion categorica. Cada etiqueta corresponde a una instancia de X_entrenamiento.
*               K: Numero de valor entero.
*               Matriz_resultados: Matriz de numeros de valor real donde cada fila es un vector con la distancia de un punto de test al conjunto de entrenamiento X_entrenamiento.
*       SALIDA:
*               Y_test: Vector de valores alfanumericos de una distribucion categorica. Cada etiqueta corresponde a una instancia de X_test.
*
****************/
/*predecir_etiquetas(Y_entrenamiento, K, Matriz_resultados, Y_test) :- print('Error. Este ejercicio no esta implementado todavia.'), !, fail.*/

/***************
* EJERCICIO 8d. predecir_etiqueta/4
*
*       ENTRADA:
*               Y_entrenamiento: Vector de valores alfanumericos de una distribucion categorica. Cada etiqueta corresponde a una instancia de X_entrenamiento.
*               K: Numero de valor entero.
*               Vec_distancias: Vector de valores reales correspondiente a una fila de Matriz_resultados.
*       SALIDA:
*               Etiqueta: Elemento de valor alfanumerico.
*
****************/
/*predecir_etiqueta(Y_entrenamiento, K, Vec_distancias, Etiqueta) :- print('Error. Este ejercicio no esta implementado todavia.'), !, fail.*/

/***************
* EJERCICIO 8e. calcular_K_etiquetas_mas_relevantes/4
*
*       ENTRADA:
*               Y_entrenamiento: Vector de valores alfanumericos de una distribucion categorica. Cada etiqueta corresponde a una instancia de X_entrenamiento.
*               K: Numero de valor entero.
*               Vec_distancias: Vector de valores reales correspondiente a una fila de Matriz_resultados.
*       SALIDA:
*		K_etiquetas: Vector de valores alfanumericos de una distribucion categorica.
*
****************/
/*calcular_K_etiquetas_mas_relevantes(Y_entrenamiento, K, Vec_distancias, K_etiquetas) :- print('Error. Este ejercicio no esta implementado todavia.'), !, fail.*/

/***************
* EJERCICIO 8f. calcular_etiqueta_mas_relevante/2
*
*       ENTRADA:
*               K_etiquetas: Vector de valores alfanumericos de una distribucion categorica.
*       SALIDA:
*               Etiqueta: Elemento de valor alfanumerico.
*
****************/
/*calcular_etiqueta_mas_relevante(K_etiquetas, Etiqueta) :- print('Error. Este ejercicio no esta implementado todavia.'), !, fail.*/

/***************
* EJERCICIO 8g. k_vecinos_proximos/5
*
*       ENTRADA:
*		X_entrenamiento: Matriz de numeros de valor real donde cada fila es una instancia representada por un vector.
*		Y_entrenamiento: Vector de valores alfanumericos de una distribucion categorica. Cada etiqueta corresponde a una instancia de X_entrenamiento.
*		K: Numero de valor entero.
*		X_test: Matriz de numeros de valor real donde cada fila es una instancia representada por un vector. Instancias sin etiquetar.
*       SALIDA:
*		Y_test: Vector de valores alfanumericos de una distribucion categorica. Cada etiqueta corresponde a una instancia de X_test.
*
****************/
/*k_vecinos_proximos(X_entrenamiento, Y_entrenamiento, K, X_test, Y_test) :- print('Error. Este ejercicio no esta implementado todavia.'), !, fail.*/