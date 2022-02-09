from data_handling import *
from representation import *
from classify import *
from configuration import *
from datetime import datetime
import argparse
import logging
import os



# Configure logging
logging.basicConfig(level=logging.INFO, format='(%(asctime)s)FAAProyect-%(levelname)s: %(message)s')

def gen_graphs_function():
    # Handle creation of directories relevant
    if not os.path.exists(GRAPH_PATH):
        os.mkdir(GRAPH_PATH)
    if not os.path.exists(EXPERIMENT_GRAPH_PATH):
        os.mkdir(EXPERIMENT_GRAPH_PATH)
    
    # Load, handle data and generate graphs
    logging.info('Starting graph generation.')
    metadata, data = load_data()
    data_list = data_per_experiment(data)
    generate_graphs(data_list, metadata)
    logging.info('Graph generation complete.')


def test():
    pass


def execute():
    # Handle creation of relevant directories
    if not os.path.exists(GRAPH_PATH):
        os.mkdir(GRAPH_PATH)
    if not os.path.exists(CONFUSION_GRAPH_PATH):
        os.mkdir(CONFUSION_GRAPH_PATH)
    if not os.path.exists(ROC_SPACE_GRAPH_PATH):
        os.mkdir(ROC_SPACE_GRAPH_PATH)
    if not os.path.exists(RESULTS_PATH):
        os.mkdir(RESULTS_PATH)

    # Construct data according to filters
    logging.info('Starting execute.')
    metadata, data = load_data()
    data_list = data_per_experiment(data)
    filter_data(data_list, metadata, filter_experiments=[47, 76], filter_attrs=['R5'], filter_stimulus=True)
    clean_data(data_list, metadata)
    final_data = pd.concat(data_list.values())
    X = final_data.to_numpy()[:,:-1]
    y = final_data.to_numpy()[:,-1]
    logging.info('Data loaded and processed.')

    with open(RESULT_FILE_PATH, 'a') as f:
        f.write('Id\tPrecision\tStd\n')

    # Iterate through each classifier
    cms = []
    for element in CLASSIFIERS:
        logging.info(f'Executing {element["id"]}...')
        score, std = score_classifier(element['clf'], X, y, 5)

        with open(RESULT_FILE_PATH, 'a') as f:
            f.write('{}\t{:.6f}\t{:.6f}\n'.format(element['id'], score, std))

        # Generate confusion matrix with results
        cm = build_confusion_matrix(element['clf'], X, y)
        display_confusion_matrix(cm, element['id'], element['id'])
        cms.append(cm)

    display_roc_space(cms, [x['id'][0:3] for x in CLASSIFIERS])  


def stats():
    logging.info('Loading data.')
    metadata, data = load_data()
    data_list = data_per_experiment(data)
    filter_data(data_list, metadata)
    clean_data(data_list, metadata)
    final_data = pd.concat(data_list.values())
    logging.info('Data loaded.')
    print('Experiments:')
    print(metadata['class'].value_counts())
    print('Description of data:')
    print(final_data.describe())
    print(final_data['class'].value_counts())


def main():
    # Configure ArgumentParser
    parser = argparse.ArgumentParser(description='Main program for FAA Project.')
    parser.add_argument('--gen_graphs', action='store_true', help='Generation of data for all experiments.')
    parser.add_argument('--test', action='store_true')
    parser.add_argument('--execute', action='store_true', help='Execute the classifier testing.')
    parser.add_argument('--stats', action='store_true', help='Calculate statistics of data.')

    args = parser.parse_args()

    if args.gen_graphs:
        gen_graphs_function()
    elif args.test:
        test()
    elif args.execute:
        execute()
    elif args.stats:
        stats()


if __name__ == '__main__':
    main()