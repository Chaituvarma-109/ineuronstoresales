import sys

from sales.Entity.artifact_entity import DataIngestionArtifact
from sales.Exception.customexception import SalesException
from sales.Component.data_ingestion import Dataingestion
from sales.Config.configuration import Configuration
from sales.Logger.log import logging


class Pipeline:
    def __init__(self, config: Configuration = Configuration()):
        try:
            self.config = config
        except Exception as e:
            raise SalesException(e, sys) from e

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            data_ingestion = Dataingestion(data_ingestion_config=self.config.get_data_ingestion_config())
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise SalesException(e, sys) from e

    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
        except Exception as e:
            raise SalesException(e, sys) from e
