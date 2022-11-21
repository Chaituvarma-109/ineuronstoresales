import os
import sys

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

    def download_housing_data(self) -> DataIngestionArtifact:
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

            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path,
                                                            test_file_path=test_file_path, is_ingested=True,
                                                            msg="Data ingestion completed successfully.")

            logging.info(f"Data Ingestion artifact:[{data_ingestion_artifact}]")
            return data_ingestion_artifact
        except Exception as e:
            raise SalesException(e, sys) from e

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            return self.download_housing_data()
        except Exception as e:
            raise SalesException(e, sys) from e

    def __del__(self):
        logging.info(f"{'>>' * 20}Data Ingestion log completed.{'<<' * 20} \n\n")
