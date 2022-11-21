import pandas as pd
import numpy as np
import yaml
import sys
import os
import dill

from sales.Exception.customexception import SalesException
from sales.Constants import DATASET_SCHEMA_COLUMNS_KEY


def write_yaml_file(file_path: str, data: dict = None):
    """
    Creates yaml file
    :param file_path: path of file
    :param data: dict
    :return:
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as yaml_file:
            if data is None:
                yaml.dump(data, yaml_file)
    except Exception as e:
        raise SalesException(e, sys) from e


def read_yaml_file(file_path: str) -> dict:
    """
    reads yaml file
    :param file_path:
    :return:
    """
    try:
        with open(file_path) as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise SalesException(e, sys) from e


def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise SalesException(e, sys) from e


def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise SalesException(e, sys) from e


def save_object(file_path: str, obj):
    """
    file_path: str
    obj: Any sort of object
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise SalesException(e, sys) from e


def load_object(file_path: str):
    """
    file_path: str
    """
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise SalesException(e, sys) from e


def load_data(file_path: str, schema_file_path: str) -> pd.DataFrame:
    try:
        dataset_schema = read_yaml_file(schema_file_path)
        schema = dataset_schema[DATASET_SCHEMA_COLUMNS_KEY]

        df = pd.read_csv(file_path)

        error_msg = ''
        for column in df.columns:
            if column in schema.keys():
                df[column].astype(schema[column])
            else:
                error_msg = f"{error_msg} \nColumn: [{column}] is not in the schema."

        if len(error_msg) > 0:
            raise Exception(error_msg)

        return df
    except Exception as e:
        raise SalesException(e, sys) from e
