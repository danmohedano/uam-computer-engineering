:- begin_tests(exercise1).
:- include(code_2391_daniel_mohedano_silvia_sopenna).
test(1) :-
    sum_pot_prod([1,2,3],[3,4,5], 1, X),
    X = 26,
    !.
test(2) :-
    sum_pot_prod([1,2,3],[3,4,5], 2, X),
    X =:= 298,
    !.
test(3) :-
    \+ sum_pot_prod([1,2,3],[3,4,5], -1, _).
test(4) :-
    \+ sum_pot_prod([1,2,3],[3,4,5,6], 3, _).
:- end_tests(exercise1).

:- begin_tests(exercise2).
:- include(code_2391_daniel_mohedano_silvia_sopenna).
test(1) :-
    segundo_penultimo([1,2], X, Y), 
    X =:= 2,
    Y =:= 1.
test(2) :-
    segundo_penultimo([1,2,3], X, Y),
    X =:= 2,  
    Y =:= 2.
test(3) :-
    segundo_penultimo([1,2,3,4], X, Y),
    X =:= 2,
    Y =:= 3.
test(4) :-
    \+ segundo_penultimo([1], _, _).
:- end_tests(exercise2).

:- begin_tests(exercise3).
:- include(code_2391_daniel_mohedano_silvia_sopenna).
test(1) :-
    sublista(['a','b','c','d','e'], 2, 4, 'b', X),
    X = ['b','c','d'].
test(2) :-
    \+ sublista(['a','b','c','d','e'], 2, 4, 'f', _).
test(3) :-
    \+ sublista(['a','b','c','d','e'], 5, 4, 'b', _).
:- end_tests(exercise3).

:- begin_tests(exercise4).
:- include(code_2391_daniel_mohedano_silvia_sopenna).
test(1) :-
    espacio_lineal(0, 1, 5, L),
    L = [0, 0.25, 0.5, 0.75, 1.0].
test(2) :-
    espacio_lineal(0, 1, 100, L),
    L = [0, 0.01010101, 0.02020202, 0.03030303, 0.04040404, 0.05050505, 0.06060606, 0.07070707,
    0.08080808, 0.09090909, 0.1010101 , 0.11111111, 0.12121212, 0.13131313, 0.14141414, 0.15151515,
    0.16161616, 0.17171717, 0.18181818, 0.19191919, 0.2020202 , 0.21212121, 0.22222222, 0.23232323,
    0.24242424, 0.25252525, 0.26262626, 0.27272727, 0.28282828, 0.29292929, 0.3030303 , 0.31313131,
    0.32323232, 0.33333333, 0.34343434, 0.35353535, 0.36363636, 0.37373737, 0.38383838, 0.39393939,
    0.4040404 , 0.41414141, 0.42424242, 0.43434343, 0.44444444, 0.45454545, 0.46464646, 0.47474747,
    0.48484848, 0.49494949, 0.50505051, 0.51515152, 0.52525253, 0.53535354, 0.54545455, 0.55555556,
    0.56565657, 0.57575758, 0.58585859, 0.5959596 , 0.60606061, 0.61616162, 0.62626263, 0.63636364,
    0.64646465, 0.65656566, 0.66666667, 0.67676768, 0.68686869, 0.6969697 , 0.70707071, 0.71717172,
    0.72727273, 0.73737374, 0.74747475, 0.75757576, 0.76767677, 0.77777778, 0.78787879, 0.7979798
    , 0.80808081, 0.81818182, 0.82828283, 0.83838384, 0.84848485, 0.85858586, 0.86868687, 0.87878788,
    0.88888889, 0.8989899 , 0.90909091, 0.91919192, 0.92929293, 0.93939394, 0.94949495, 0.95959596,
    0.96969697, 0.97979798, 0.98989899, 1].
test(3) :-
    \+ espacio_lineal(2,0,3,_).
:- end_tests(exercise4).

:- begin_tests(exercise5).
:- include(code_2391_daniel_mohedano_silvia_sopenna).
test(1) :-
    normalizar([3,4,5], X),
    X = [0.25, 0.3333333333333333, 0.4166666666666667].
test(2) :-
    normalizar([1,2,3,4,5], X),
    X = [0.06666666666666667, 0.13333333333333333, 0.2, 0.26666666666666666, 0.3333333333333333].
test(3) :-
    \+ normalizar([-1,2,3,4,5], _).
:- end_tests(exercise5).

:- begin_tests(exercise6).
:- include(code_2391_daniel_mohedano_silvia_sopenna).
test(1) :-
    divergencia_kl([0.2, 0.3, 0.5], [0.2, 0.3, 0.5], D), 
    D =:= 0.0.
test(2) :-
    divergencia_kl([0.5, 0.3, 0.2], [0.2, 0.3, 0.5], D), 
    D =:= 0.27488721956224654.
test(3) :-
    divergencia_kl([0.98, 0.01, 0.01], [0.01, 0.01, 0.98], D),
    D =:= 4.447418454310455.
test(4) :-
    \+ divergencia_kl([0.99, 0.0, 0.01], [0.01, 0.01, 0.98], _).
test(5) :-
    \+ divergencia_kl([0.2,0.3,0.6], [0.1,0.5,0.4], _).
:- end_tests(exercise6).
