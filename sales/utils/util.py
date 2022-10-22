import yaml
import sys
import os
import dill

from sales.Exception.customexception import SalesException


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
