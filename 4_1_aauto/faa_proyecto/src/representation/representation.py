import matplotlib.pyplot as plt
from .constants import EXPERIMENT_GRAPH_PATH, CONFUSION_GRAPH_PATH, ROC_SPACE_GRAPH_PATH
import logging
from sklearn.metrics import ConfusionMatrixDisplay
from classify import build_roc_space


def experiment_graph(exp_counter, data, metadata):
    """Generates the graph representation of an experiment.

    Args:
        exp_counter (int): Experiment counter.
        data (pd.Dataframe): Data for the experiment.
        metadata (pd.Dataframe): General metadata.
    """
    # Log action
    logging.info(f'Generating graph for EXP#{exp_counter}...')

    fig = plt.figure(figsize=(7,13))
    fig.tight_layout()
    gs = fig.add_gridspec(6, hspace=0)
    axs = gs.subplots(sharex=True)
    
    fig.suptitle(f'Experimento {exp_counter}: {metadata.loc[exp_counter]["class"]}')
    axs[0].plot(data['time'], data['Humidity'])
    axs[1].plot(data['time'], data['Temp.'])
    axs[2].plot(data['time'], data['R1'])
    axs[2].plot(data['time'], data['R4'])
    axs[3].plot(data['time'], data['R2'])
    axs[3].plot(data['time'], data['R3'])
    axs[4].plot(data['time'], data['R5'])
    axs[4].plot(data['time'], data['R6'])
    axs[5].plot(data['time'], data['R7'])
    axs[5].plot(data['time'], data['R8'])
    
    for ax in axs:
        ax.set_xlabel('Tiempo (h)')
        ax.grid(True)
        ax.axvline(x=0, color='black')
        ax.axvline(x=metadata.iloc[exp_counter]['dt'], color='black')
        
    axs[0].set_ylabel('H (%)')
    axs[1].set_ylabel('T (C)')
    axs[2].set_ylabel('$R_{1,4}$')
    axs[3].set_ylabel('$R_{2,3}$')
    axs[4].set_ylabel('$R_{5,6}$')
    axs[5].set_ylabel('$R_{7,8}$')
    plt.savefig(EXPERIMENT_GRAPH_PATH.joinpath(f'{exp_counter}.jpeg'))
    plt.close(fig)


def generate_graphs(data_list, metadata):
    """Generate graphs for every existing experiment.

    Args:
        data_list (dict): Data per experiment.
        metadata (pd.Dataframe): General metadata.
    """
    for x in data_list.keys():
        experiment_graph(x, data_list[x], metadata)   


def display_confusion_matrix(cm, title, file_name):
    """Displays a confusion matrix.

    Args:
        cm (np.ndarray): Confusion matrix.
        title (str): Figure title.
        file_name (str): File name.
    """
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['background', 'banana', 'wine'])
    disp.plot()
    plt.title(title)
    plt.savefig(CONFUSION_GRAPH_PATH.joinpath(f'{file_name}.png'), bbox_inches='tight')
    plt.close()


def display_roc_space(cms, names):
    """Displays the ROC space for the classifier given the confusion matrix.

    Args:
        cms (list(np.ndarray)): Confusion matrices.
        names (list(str)): Classifier names.
    """
    classes = ['background', 'banana', 'wine']

    fprs = []
    tprs = []
    for cm in cms:
        fpr, tpr = build_roc_space(cm)
        fprs.append(fpr)
        tprs.append(tpr)

    for i in range(3):
        plt.title(f'Espacio ROC: {classes[i]}')
        plt.plot([0,1], [0,1])
        plt.legend(['Random'], loc=4)

        for j in range(len(fprs)):
            plt.plot(fprs[j][i], tprs[j][i], '.', ms=15)
            plt.annotate(names[j], (fprs[j][i], tprs[j][i]), fontsize=7)

        plt.xlabel('FPR')
        plt.ylabel('TPR')
        plt.grid(True)
        plt.xlim([-0.1,1.1])
        plt.ylim([-0.1,1.1])
        
        plt.savefig(ROC_SPACE_GRAPH_PATH.joinpath(f'{classes[i]}.png'), bbox_inches='tight')
        plt.close()
