import os
import sys

from sales.Entity.config_entity import (DataIngestionConfig, TrainingPipelineConfig, DatavalidationConfig,
                                        DataTransformationConfig)
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

            data_validation_info = self.config_info[DATA_VALIDATION_CONFIG_KEY]

            schema_file_path = os.path.join(ROOT_DIR, data_validation_info[DATA_VALIDATION_SCHEMA_DIR_KEY],
                                            data_validation_info[DATA_VALIDATION_SCHEMA_FILE_NAME_KEY])

            data_validation_config = DatavalidationConfig(schema_file_path=schema_file_path)

            logging.info(f"Data Validation Config: {data_validation_config}")
            return data_validation_config
        except Exception as e:
            raise SalesException(e, sys) from e

    def get_data_transformation_config(self) -> DataTransformationConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir
            data_transformation_artifact_dir = os.path.join(artifact_dir, DATA_TRANSFORMATION_ARTIFACT_DIR,
                                                            self.timestamp)

            data_transformation_info = self.config_info[DATA_TRANSFORMATION_CONFIG_KEY]

            item_type_combined = data_transformation_info[DATA_TRANSFORMATION_ITEM_TYPE_COMBINED]
            years_established = data_transformation_info[DATA_TRANSFORMATION_YEARS_ESTABLISHED]
            item_fat_content = data_transformation_info[DATA_TRANSFORMATION_ITEM_FAT_CONTENT]
            item_visibility = data_transformation_info[DATA_TRANSFORMATION_ITEM_VISIBILITY]

            preprocessed_obj_file_path = os.path.join(
                data_transformation_artifact_dir,
                data_transformation_info[DATA_TRANSFORMATION_PREPROCESSING_DIR_KEY],
                data_transformation_info[DATA_TRANSFORMATION_PREPROCESSED_FILE_NAME_KEY]
            )

            transformed_train_dir = os.path.join(data_transformation_artifact_dir,
                                                 data_transformation_info[DATA_TRANSFORMATION_DIR_NAME_KEY],
                                                 data_transformation_info[DATA_TRANSFORMATION_TRAIN_DIR_NAME_KEY])

            transformed_test_dir = os.path.join(data_transformation_artifact_dir,
                                                data_transformation_info[DATA_TRANSFORMATION_DIR_NAME_KEY],
                                                data_transformation_info[DATA_TRANSFORMATION_TEST_DIR_NAME_KEY])

            data_transformation_config = DataTransformationConfig(
                Item_Type_Combined=item_type_combined,
                Years_Established=years_established,
                Item_Fat_Content=item_fat_content,
                Item_Visibility=item_visibility,
                transformed_train_dir=transformed_train_dir,
                transformed_test_dir=transformed_test_dir,
                preprocessed_obj_file_path=preprocessed_obj_file_path,
            )

            logging.info(f"Data transformation config: {data_transformation_config}")
            return data_transformation_config
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
