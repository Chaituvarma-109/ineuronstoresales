import os
import sys

import pandas as pd

from sales.Exception.customexception import SalesException
from sales.utils.util import load_object


class SalesData:

    def __init__(self,
                 longitude: float,
                 latitude: float,
                 housing_median_age: float,
                 total_rooms: float,
                 total_bedrooms: float,
                 population: float,
                 households: float,
                 median_income: float,
                 ocean_proximity: str,
                 median_house_value: float = None
                 ):
        try:
            self.longitude = longitude
            self.latitude = latitude
            self.housing_median_age = housing_median_age
            self.total_rooms = total_rooms
            self.total_bedrooms = total_bedrooms
            self.population = population
            self.households = households
            self.median_income = median_income
            self.ocean_proximity = ocean_proximity
            self.median_house_value = median_house_value
        except Exception as e:
            raise SalesException(e, sys) from e

    def get_sales_input_data_frame(self):

        try:
            sales_input_dict = self.get_sales_data_as_dict()
            return pd.DataFrame(sales_input_dict)
        except Exception as e:
            raise SalesException(e, sys) from e

    def get_sales_data_as_dict(self):
        try:
            input_data = {
                "longitude": [self.longitude],
                "latitude": [self.latitude],
                "housing_median_age": [self.housing_median_age],
                "total_rooms": [self.total_rooms],
                "total_bedrooms": [self.total_bedrooms],
                "population": [self.population],
                "households": [self.households],
                "median_income": [self.median_income],
                "ocean_proximity": [self.ocean_proximity]}
            return input_data
        except Exception as e:
            raise SalesException(e, sys)


class SalesPredictor:

    def __init__(self, model_dir: str):
        try:
            self.model_dir = model_dir
        except Exception as e:
            raise SalesException(e, sys) from e

    def get_latest_model_path(self):
        try:
            folder_name = list(map(int, os.listdir(self.model_dir)))
            latest_model_dir = os.path.join(self.model_dir, f"{max(folder_name)}")
            file_name = os.listdir(latest_model_dir)[0]
            latest_model_path = os.path.join(latest_model_dir, file_name)
            return latest_model_path
        except Exception as e:
            raise SalesException(e, sys) from e

    def predict(self, X):
        try:
            model_path = self.get_latest_model_path()
            model = load_object(file_path=model_path)
            Item_Outlet_Sales = model.predict(X)
            return Item_Outlet_Sales
        except Exception as e:
            raise SalesException(e, sys) from e
