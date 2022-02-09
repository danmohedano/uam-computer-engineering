import pandas as pd
from .constants import DATASET_PATH, METADATA_PATH
import logging
import numpy as np


def load_data():
    """Carga los datos de metadata y dataset.

    Returns:
        pd.Dataframe: Metadata,
        pd.Dataframe: Data
    """
    # Cargar datos
    metadata = pd.read_csv(METADATA_PATH, sep=r'\t+', engine='python')
    data = pd.read_csv(DATASET_PATH, sep=r'\s+', engine='python')

    return metadata, data


def data_per_experiment(data):
    """

    Args:
        data (pd.Dataframe):

    Returns:
        list: Lista con los dataframe para cada experimento.
    """
    data_list = {}

    for exp in data['id'].unique():
        data_list[exp] = data[data['id'] == exp]

    return data_list


def filter_data(data_per_exp, metadata, filter_experiments=[], filter_attrs=[], filter_stimulus=False):
    """Filter out non-relevant data.

    Args:
        data_per_exp (dict): Dictionary with data per experiment.
        metadata (pd.Dataframe): General metadata.
        filter_experiments (list): Experiments that should be filtered out.
        filter_attrs (list): Attributes that should be filtered out.
        filter_stimulus (boolean): If the data should only be limited to the stimulus insertion window.
    """
    # Filter experiments
    for exp in filter_experiments:
        data_per_exp.pop(exp, None)
    
    for exp in data_per_exp:
        # Filter attributes
        data_per_exp[exp] = data_per_exp[exp].drop(filter_attrs, axis=1)

        # Filter stimulus
        if filter_stimulus:
            new_val = data_per_exp[exp].loc[(0 <= data_per_exp[exp].time) & (data_per_exp[exp].time <= metadata.iloc[exp]['dt'])].copy()
            data_per_exp[exp] = new_val



def clean_data(data_per_exp, metadata):
    """Cleans the data in order to be used by a classifier.

    This process includes the removal of the 'time' attribute, the removal of
    the 'id' attribute and the addition of the 'class' attribute.

    Args:
        data_per_exp (dict): Dictionary with data per experiment.
        metadata (pd.Dataframe): General metadata.
    """
    for exp in data_per_exp:
        # Add class attribute
        data_per_exp[exp]['class'] = 'background'
        data_per_exp[exp].loc[(0 <= data_per_exp[exp].time) & (data_per_exp[exp].time <= metadata.iloc[exp]['dt']), ['class']] = metadata.iloc[exp]['class']
        
        # Remove time attribute
        data_per_exp[exp] = data_per_exp[exp].drop('time', axis=1)

        # Remove id attribute
        data_per_exp[exp] = data_per_exp[exp].drop('id', axis=1)

        
    
    
