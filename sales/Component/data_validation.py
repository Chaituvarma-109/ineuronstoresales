import os.path
import sys
import json

import pandas as pd

from sales.Config.configuration import DatavalidationConfig
from sales.Entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from sales.Exception.customexception import SalesException
from sales.utils.util import read_yaml_file
from sales.Logger.log import logging


class DataValidation:
    def __init__(self, data_valid_config: DatavalidationConfig, data_ingestion_artifact: DataIngestionArtifact):
        try:
            logging.info(f"{'>>' * 30}Data Validation log started.{'<<' * 30} ")
            self.data_validation_config = data_valid_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise SalesException(e, sys) from e

    def get_train_and_test_df(self) -> tuple[str, str]:
        """
        reads the train and test csv files.
        Returns: test and train files.

        """
        try:
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            return train_df, test_df
        except Exception as e:
            raise SalesException(e, sys) from e

    @staticmethod
    def check_col_names(df_col: list[str], schema_df_col: list[str]) -> bool:
        """
        this method checks column names of the dataset
        Args:
            df_col: list of columns from the dataset
            schema_df_col: list of columns names from the schema yaml file.

        Returns: true if column names matches else returns false.

        """
        try:
            check_name = False
            for col_name in df_col:
                if col_name not in schema_df_col:
                    return check_name
            check_name = True
            return check_name
        except Exception as e:
            raise SalesException(e, sys) from e

    @staticmethod
    def check_domain_names(df_val: list[str], schema_val: list[str]) -> bool:
        """
        checks the values of the given columns.
        Args:
            df_val: list of values of columns
            schema_val: list of specified values from the schema yaml file.

        Returns: true if domain values matches else false

        """
        try:
            domain_name = False
            for col_name in df_val:
                if col_name not in schema_val:
                    return domain_name
            domain_name = True
            return domain_name
        except Exception as e:
            raise SalesException(e, sys) from e

    def is_train_test_file_exists(self) -> bool:
        """
        this method checks whether train and test files existed in the specified path or not
        Returns:
            returns true if files exists else returns false.
        """
        try:
            logging.info("checking if training and test file is available")
            train_file_path_exists = False
            test_file_path_exists = False

            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            train_file_path_exists = os.path.exists(train_file_path)
            test_file_path_exists = os.path.exists(test_file_path)

            is_available = train_file_path_exists and test_file_path_exists
            logging.info(f"is training and test file exists? -> {is_available}")

            if not is_available:
                train_file_path = self.data_ingestion_artifact.train_file_path
                test_file_path = self.data_ingestion_artifact.test_file_path
                message = f"Training file: {train_file_path} or test file: {test_file_path} is not present."
                raise Exception(message)

            return is_available
        except Exception as e:
            raise SalesException(e, sys) from e

    def validate_dataset_schema(self) -> bool:
        """
        this method validates the dataset i.e, checks files and columns of the datasets.
        Returns:
            returns true if the dataset is ok else returns false.
        """
        try:
            validation_status = False

            schema_file_path = self.data_validation_config.schema_file_path
            config_info = read_yaml_file(schema_file_path)

            train_df, test_df = self.get_train_and_test_df()

            train_df_col = train_df.columns
            test_df_col = test_df.columns

            df_item_fat_content = train_df['Item_Fat_Content'].unique()
            df_outlet_size = train_df['Outlet_Size'].unique()
            df_outlet_loc_type = train_df['Outlet_Location_Type'].unique()
            df_outlet_type = train_df['Outlet_Type'].unique()

            numerical_col = config_info['numerical_columns']
            categorical_col = config_info['categorical_columns']
            target_col = config_info['target_column']

            domain_val = config_info['domain_value']
            item_fat_content = domain_val['Item_Fat_Content']
            outlet_size = domain_val['Outlet_Size']
            outlet_loc_type = domain_val['Outlet_Location_Type']
            outlet_type = domain_val['Outlet_Type']

            schema_train_cols = numerical_col + categorical_col + target_col
            schema_test_cols = numerical_col + categorical_col + target_col

            train_len_col = (len(train_df_col) == len(schema_train_cols))
            test_len_col = (len(test_df_col) == len(schema_test_cols))

            train_col_names = self.check_col_names(train_df_col, schema_train_cols)
            test_col_names = self.check_col_names(test_df_col, schema_test_cols)

            item_fat_val = self.check_domain_names(df_item_fat_content, item_fat_content)
            outlet_size_val = self.check_domain_names(df_outlet_size, outlet_size)
            outlet_loc_type_val = self.check_domain_names(df_outlet_loc_type, outlet_loc_type)
            outlet_type_val = self.check_domain_names(df_outlet_type, outlet_type)

            length_cols = train_len_col and test_len_col
            col_names = train_col_names and test_col_names
            domain_names = item_fat_val and outlet_size_val and outlet_loc_type_val and outlet_type_val

            if length_cols and col_names and domain_names:
                validation_status = True

            return validation_status
        except Exception as e:
            raise SalesException(e, sys) from e

    def initiate_data_validation(self):
        try:
            self.is_train_test_file_exists()
            self.validate_dataset_schema()

            data_validation_artifact = DataValidationArtifact(
                schema_file_path=self.data_validation_config.schema_file_path,
                is_validated=True,
                message="Data Validation performed successfully."
            )
            logging.info(f"Data Validation Artifact: {data_validation_artifact}")

            return data_validation_artifact

        except Exception as e:
            raise SalesException(e, sys) from e

    def __del__(self):
        logging.info(f"{'>>' * 30}Data Validation log completed.{'<<' * 30} \n\n")
