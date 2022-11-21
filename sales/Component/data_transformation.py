import sys

import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

from sales.Entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact
from sales.Entity.config_entity import DataTransformationConfig
from sales.utils.util import read_yaml_file, load_data, save_numpy_array_data, save_object
from sales.Exception.customexception import SalesException
from sales.Logger.log import logging
from sales.Constants import *


class FeatureGenerator(BaseEstimator, TransformerMixin):
    def __init__(self, col_type, col_names=None):
        self.col_type = col_type
        self.col_names = col_names

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        try:
            if isinstance(X, np.ndarray):
                X = pd.DataFrame(X, columns=self.col_names)
            if self.col_type == 'categorical':
                X['Item_Type_Combined'] = X['Item_Identifier'].apply(lambda x: x[0:2]).map({
                    'FD': 'Food',
                    'NC': 'Non-Consumable',
                    'DR': 'Drinks'
                })
                X['Item_Fat_Content'] = X['Item_Fat_Content'].replace(['low fat', 'LF', 'reg'],
                                                                      ['Low Fat', 'Low Fat', 'Regular'], inplace=True)
            if self.col_type == 'numerical':
                X['Years_Established'] = X['Outlet_Establishment_Year'].apply(lambda x: 2022 - x)
                X['Item_Visibility'] = X['Item_Visibility'].replace(0, X['Item_Visibility'].mean())

            return X
        except Exception as e:
            raise SalesException(e, sys) from e


class DataTransformation:
    def __init__(self, data_ingestion_config: DataIngestionArtifact, data_validation_config: DataValidationArtifact,
                 data_transformation_config: DataTransformationConfig):
        try:
            logging.info(f"{'>>' * 30}Data Transformation log started.{'<<' * 30} ")
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_config = data_ingestion_config
            self.data_validation_config = data_validation_config
        except Exception as e:
            raise SalesException(e, sys) from e

    def get_transformer_object(self) -> ColumnTransformer:
        try:
            schema_file_path = self.data_validation_config.schema_file_path

            dataset_schema = read_yaml_file(file_path=schema_file_path)

            numerical_columns = dataset_schema['numerical_columns']
            categorical_columns = dataset_schema['categorical_columns']

            num_pipeline = Pipeline(steps=[
                ('impute', SimpleImputer(strategy='mean')),
                ('feature_generator', FeatureGenerator(
                    col_type='numerical',
                    col_names=numerical_columns,
                )),
                ('scaling', StandardScaler())
            ])

            cat_pipeline = Pipeline(steps=[
                ('impute', SimpleImputer(strategy='most_frequent')),
                ('feature_generator', FeatureGenerator(
                    col_type='categorical',
                    col_names=categorical_columns,
                )),
                ('one hot encoding', OneHotEncoder(sparse=False)),
                ('scaling', StandardScaler(with_mean=False))
            ])

            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            preprocessing = ColumnTransformer([
                ('num_pipeline', num_pipeline, numerical_columns),
                ('cat_pipeline', cat_pipeline, categorical_columns),
            ])
            return preprocessing
        except Exception as e:
            raise SalesException(e, sys) from e

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info(f"Obtaining preprocessing object.")
            preprocessing_obj = self.get_transformer_object()

            logging.info(f"Obtaining training and test file path.")
            # getting train and test file paths
            train_file_path = self.data_ingestion_config.train_file_path
            test_file_path = self.data_ingestion_config.test_file_path

            schema_file_path = self.data_validation_config.schema_file_path

            train_df = load_data(file_path=train_file_path, schema_file_path=schema_file_path)
            test_df = load_data(file_path=test_file_path, schema_file_path=schema_file_path)

            schema = read_yaml_file(file_path=schema_file_path)

            target_column_name = schema[TARGET_COLUMN_KEY]

            logging.info(f"Splitting input and target feature from training dataframe.")
            input_feature_train_df = train_df.drop(columns=target_column_name, axis=1)
            target_feature_train_df = train_df[target_column_name]

            logging.info(f"Applying preprocessing object on training dataframe and testing dataframe")
            input_feature_train_array = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_array = preprocessing_obj.transform(test_df)

            train_arr = np.c_[input_feature_train_array, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_array]

            transformed_train_dir = self.data_transformation_config.transformed_train_dir
            transformed_test_dir = self.data_transformation_config.transformed_test_dir

            train_file_name = os.path.basename(train_file_path).replace(".csv", ".npz")
            test_file_name = os.path.basename(test_file_path).replace(".csv", ".npz")

            transformed_train_file_path = os.path.join(transformed_train_dir, train_file_name)
            transformed_test_file_path = os.path.join(transformed_test_dir, test_file_name)

            logging.info(f"Saving transformed training and testing array.")

            save_numpy_array_data(file_path=transformed_train_file_path, array=train_arr)
            save_numpy_array_data(file_path=transformed_test_file_path, array=test_arr)

            preprocessing_object_file_path = self.data_transformation_config.preprocessed_obj_file_path

            logging.info(f"Saving preprocessing object.")
            save_object(file_path=preprocessing_object_file_path, obj=preprocessing_obj)

            data_transformation_artifact = DataTransformationArtifact(
                is_transformed=True, message="Data transformation successfully.",
                transformed_train_file_path=transformed_train_file_path,
                transformed_test_file_path=transformed_test_file_path,
                preprocessed_obj_file_path=preprocessing_object_file_path
            )

            logging.info(f"Data transformation artifact: {data_transformation_artifact}")
            return data_transformation_artifact

        except Exception as e:
            raise SalesException(e, sys) from e

    def __del__(self):
        logging.info(f"{'>>' * 30}Data Transformation log completed.{'<<' * 30} \n\n")
