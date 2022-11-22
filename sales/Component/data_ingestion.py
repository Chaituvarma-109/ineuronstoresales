import os
import sys

import pandas as pd

from sklearn.model_selection import train_test_split
from six.moves import urllib

from sales.Entity.artifact_entity import DataIngestionArtifact
from sales.Entity.config_entity import DataIngestionConfig
from sales.Exception.customexception import SalesException
from sales.Logger.log import logging


class Dataingestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            logging.info(f"{'=' * 20}Data Ingestion log started.{'=' * 20}")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise SalesException(e, sys) from e

    def download_housing_data(self) -> None:
        """
        downloads dataset from the specified url.
        Returns: DataIngestionArtifact

        """
        try:
            train_dataset_url = self.data_ingestion_config.DATA_INGESTION_TRAIN_DATA_DOWNLOAD_URL
            test_dataset_url = self.data_ingestion_config.DATA_INGESTION_TEST_DATA_DOWNLOAD_URL

            data_dir = self.data_ingestion_config.DATA_INGESTION_DATA_DIR

            os.makedirs(data_dir, exist_ok=True)

            train_file_name = os.path.basename(train_dataset_url)
            test_file_name = os.path.basename(test_dataset_url)

            train_file_path = os.path.join(data_dir, train_file_name)
            test_file_path = os.path.join(data_dir, test_file_name)

            logging.info(f"Downloading file from: {train_dataset_url} into directory: {train_file_path}")
            urllib.request.urlretrieve(train_dataset_url, train_file_path)
            logging.info(f"file {train_file_path} has been downloaded successfully.")
            logging.info(f"Downloading file from: {test_dataset_url} into directory: {test_file_path}")
            urllib.request.urlretrieve(test_dataset_url, test_file_path)
            logging.info(f"file {test_file_path} has been downloaded successfully.")

        except Exception as e:
            raise SalesException(e, sys) from e

    def split_data_as_train_test(self) -> DataIngestionArtifact:
        try:
            data_dir = self.data_ingestion_config.DATA_INGESTION_DATA_DIR

            file_name = os.listdir(data_dir)[3]

            sales_train_file_path = os.path.join(data_dir, file_name)

            logging.info(f"Reading csv file: [{sales_train_file_path}]")
            sales_train_df = pd.read_csv(sales_train_file_path)

            sales_train, sales_test = train_test_split(sales_train_df, test_size=0.2, random_state=42)

            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir, file_name)
            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir, file_name)

            os.makedirs(self.data_ingestion_config.ingested_train_dir, exist_ok=True)
            logging.info(f"Exporting training dataset to file: [{train_file_path}]")
            sales_train.to_csv(train_file_path, index=False)

            os.makedirs(self.data_ingestion_config.ingested_test_dir, exist_ok=True)
            logging.info(f"Exporting test dataset to file: [{test_file_path}]")
            sales_test.to_csv(test_file_path, index=False)

            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path,
                                                            test_file_path=test_file_path, is_ingested=True,
                                                            msg=f"Data ingestion completed successfully.")
            logging.info(f"Data Ingestion artifact:[{data_ingestion_artifact}]")
            return data_ingestion_artifact

        except Exception as e:
            raise SalesException(e, sys) from e

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            # self.download_housing_data()
            return self.split_data_as_train_test()
        except Exception as e:
            raise SalesException(e, sys) from e

    def __del__(self):
        logging.info(f"{'>>' * 20}Data Ingestion log completed.{'<<' * 20} \n\n")
