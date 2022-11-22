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
DATA_INGESTION_ARTIFACT_DIR = "data_ingestion"
DATA_INGESTION_DATA_DIR_KEY = 'data'
DATA_INGESTION_TRAIN_DATA_DOWNLOAD_URL = 'train_dataset_url'
DATA_INGESTION_TEST_DATA_DOWNLOAD_URL = 'test_dataset_url'
DATA_INGESTION_INGESTED_DIR_NAME_KEY = "ingested_dir"
DATA_INGESTION_TRAIN_DIR_KEY = "ingested_train_dir"
DATA_INGESTION_TEST_DIR_KEY = "ingested_test_dir"

# Data Validation related variables
DATA_VALIDATION_CONFIG_KEY = "data_validation_config"
DATA_VALIDATION_SCHEMA_FILE_NAME_KEY = "schema_file_name"
DATA_VALIDATION_SCHEMA_DIR_KEY = "schema_dir"

# Data Transformation related variables
DATA_TRANSFORMATION_ARTIFACT_DIR = "data_transformation"
DATA_TRANSFORMATION_CONFIG_KEY = "data_transformation_config"
DATA_TRANSFORMATION_ITEM_TYPE_COMBINED = "Item_Type_Combined"
DATA_TRANSFORMATION_YEARS_ESTABLISHED = "Years_Established"
DATA_TRANSFORMATION_ITEM_FAT_CONTENT = "Item_Fat_Content"
DATA_TRANSFORMATION_ITEM_VISIBILITY = "Item_Visibility"
DATA_TRANSFORMATION_DIR_NAME_KEY = "transformed_dir"
DATA_TRANSFORMATION_TRAIN_DIR_NAME_KEY = "transformed_train_dir"
DATA_TRANSFORMATION_TEST_DIR_NAME_KEY = "transformed_test_dir"
DATA_TRANSFORMATION_PREPROCESSING_DIR_KEY = "preprocessing_dir"
DATA_TRANSFORMATION_PREPROCESSED_FILE_NAME_KEY = "preprocessed_object_file_name"

COLUMN_OUTLET_ESTABLISHMENT_YEAR = "Outlet_Establishment_Year"
COLUMN_ITEM_IDENTIFIER = "Item_Identifier"
COLUMN_ITEM_FAT_CONTENT = "Item_Fat_Content"
COLUMN_ITEM_ITEM_VISIBILITY = "Item_Visibility"
DATASET_SCHEMA_COLUMNS_KEY = "columns"

NUMERICAL_COLUMN_KEY = "numerical_columns"
CATEGORICAL_COLUMN_KEY = "categorical_columns"

TARGET_COLUMN_KEY = "target_column"

# Model Training related variables
MODEL_TRAINER_ARTIFACT_DIR = "model_trainer"
MODEL_TRAINER_CONFIG_KEY = "model_trainer_config"
MODEL_TRAINER_TRAINED_MODEL_DIR_KEY = "trained_model_dir"
MODEL_TRAINER_TRAINED_MODEL_FILE_NAME_KEY = "model_file_name"
MODEL_TRAINER_BASE_ACCURACY_KEY = "base_accuracy"
MODEL_TRAINER_MODEL_CONFIG_DIR_KEY = "model_config_dir"
MODEL_TRAINER_MODEL_CONFIG_FILE_NAME_KEY = "model_config_file_name"
