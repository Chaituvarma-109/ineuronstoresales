import os

from datetime import datetime


def get_current_time_stamp():
    return f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"


ROOT_DIR = os.getcwd()

CONFIG_DIR = "config"
CONFIG_FILENAME = "config.yaml"
CONFIG_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_DIR, CONFIG_FILENAME)

CURRENT_TIME_STAMP = get_current_time_stamp()

# Training pipline related variable
TRAINING_PIPELINE_CONFIG_KEY = 'training_pipeline_config'
TRAINING_PIPELINE_ARTIFACT_DIR_KEY = 'artifact_dir'
TRAINING_PIPELINE_NAME_KEY = 'pipeline_name'

# Data Ingestion related variables
DATA_INGESTION_CONFIG_KEY = 'data_ingestion_config'
DATA_INGESTION_DATA_DIR_KEY = 'data'
DATA_INGESTION_TRAIN_DATA_DOWNLOAD_URL = 'train_dataset_url'
DATA_INGESTION_TEST_DATA_DOWNLOAD_URL = 'test_dataset_url'
