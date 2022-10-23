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

# Data Validation related variables
DATA_VALIDATION_CONFIG_KEY = "data_validation_config"
DATA_VALIDATION_SCHEMA_FILE_NAME_KEY = "schema_file_name"
DATA_VALIDATION_SCHEMA_DIR_KEY = "schema_dir"
DATA_VALIDATION_ARTIFACT_DIR_NAME = "data_validation"
DATA_VALIDATION_REPORT_FILE_NAME_KEY = "report_file_name"
DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY = "report_page_file_name"
