from itertools import product
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.multiclass import OneVsRestClassifier
from classify import RESULTS_PATH
import pathlib
from datetime import datetime
import numpy as np


NB = [{'clf': MultinomialNB(), 'id': 'NBMultinomial'}, {'clf': GaussianNB(), 'id': 'NBGaussian'}]
KNN = [{'clf': KNeighborsClassifier(n_neighbors=n), 'id': f'KNN[K={n}]'} for n in range(5, 101, 5)]
LR = [{'clf': LogisticRegression(multi_class='multinomial'), 'id': 'LR'}]
RF = [{'clf': RandomForestClassifier(n_estimators=n), 'id': f'RFo[n={n}]'} for n in range(10, 201, 25)]
SGD = [{'clf': OneVsRestClassifier(SGDClassifier(loss='log', learning_rate='constant', eta0=c)), 'id': 'SGD_OVR[c={:.1f}]'.format(c)} for c in list(np.linspace(0.1, 1.0, 10))]
NN = []

sizes = list(range(25, 101, 25))
layers = sizes + [(x,y) for x in sizes for y in sizes]

for layer in layers:
    NN.append({'clf': MLPClassifier(hidden_layer_sizes=layer), 'id': f'MLP[hidden={layer}]'})

CLASSIFIERS = NB + KNN + LR + RF + SGD + NN

RESULT_FILE_PATH = RESULTS_PATH.joinpath(f'results_{datetime.now()}.txt'.replace(' ', '_').replace(':', '.'))
