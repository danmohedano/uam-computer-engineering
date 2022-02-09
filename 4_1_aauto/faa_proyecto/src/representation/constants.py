import pathlib
from data_handling import ROOT_PATH

GRAPH_PATH = ROOT_PATH.joinpath('graphs')
EXPERIMENT_GRAPH_PATH = GRAPH_PATH.joinpath('experiments')
CONFUSION_GRAPH_PATH = GRAPH_PATH.joinpath('confusion_matrices')
ROC_SPACE_GRAPH_PATH = GRAPH_PATH.joinpath('roc_space')