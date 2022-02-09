import pathlib

ROOT_PATH = pathlib.Path(__file__).parent.parent.parent.resolve()
DATASET_PATH = ROOT_PATH.joinpath('data/HT_Sensor_dataset.dat')
METADATA_PATH = ROOT_PATH.joinpath('data/HT_Sensor_metadata.dat')
