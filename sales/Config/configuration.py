import os
import sys

from sales.Entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DatavalidationConfig
from sales.Exception.customexception import SalesException
from sales.Logger.log import logging
from sales.Constants import *
from sales.utils.util import read_yaml_file


class Configuration:
    def __init__(self, config_file_path: str = CONFIG_FILE_PATH, current_time_stamp: str = CURRENT_TIME_STAMP):
        self.config_info = read_yaml_file(file_path=config_file_path)
        self.training_pipeline_config = self.get_training_pipeline_config()
        self.timestamp = current_time_stamp

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        try:
            data_digestion_data_dir = os.path.join(ROOT_DIR, DATA_INGESTION_DATA_DIR_KEY)

            data_ingestion_info = self.config_info[DATA_INGESTION_CONFIG_KEY]

            train_dataset_download_url = data_ingestion_info[DATA_INGESTION_TRAIN_DATA_DOWNLOAD_URL]
            test_dataset_download_url = data_ingestion_info[DATA_INGESTION_TEST_DATA_DOWNLOAD_URL]

            data_ingestion_config = DataIngestionConfig(
                DATA_INGESTION_TRAIN_DATA_DOWNLOAD_URL=train_dataset_download_url,
                DATA_INGESTION_TEST_DATA_DOWNLOAD_URL=test_dataset_download_url,
                DATA_INGESTION_DATA_DIR=data_digestion_data_dir
            )

            logging.info(f"Data Ingestion Config: {data_ingestion_config}")
            return data_ingestion_config
        except Exception as e:
            raise SalesException(e, sys) from e

    def get_data_validation_config(self) -> DatavalidationConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir
            data_validation_artifact_dir = os.path.join(artifact_dir, DATA_VALIDATION_ARTIFACT_DIR_NAME, self.timestamp)

            data_validation_info = self.config_info[DATA_VALIDATION_CONFIG_KEY]

            schema_file_path = os.path.join(ROOT_DIR, data_validation_info[DATA_VALIDATION_SCHEMA_DIR_KEY],
                                            data_validation_info[DATA_VALIDATION_SCHEMA_FILE_NAME_KEY])

            report_file_path = os.path.join(data_validation_artifact_dir,
                                            data_validation_info[DATA_VALIDATION_REPORT_FILE_NAME_KEY])

            report_page_file_path = os.path.join(data_validation_artifact_dir,
                                                 data_validation_info[DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY])

            data_validation_config = DatavalidationConfig(schema_file_path=schema_file_path,
                                                          report_file_path=report_file_path,
                                                          report_page_file_path=report_page_file_path)

            logging.info(f"Data Validation Config: {data_validation_config}")
            return data_validation_config
        except Exception as e:
            raise SalesException(e, sys) from e

    def get_training_pipeline_config(self) -> TrainingPipelineConfig:
        try:
            training_pipeline_config = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            artifact_dir = os.path.join(ROOT_DIR, training_pipeline_config[TRAINING_PIPELINE_NAME_KEY],
                                        training_pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY])
            training_pipeline_config = TrainingPipelineConfig(artifact_dir=artifact_dir)
            logging.info(f'training pipeline config: {training_pipeline_config}')
            return training_pipeline_config
        except Exception as e:
            raise SalesException(e, sys) from e
