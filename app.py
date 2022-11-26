import json
import os

from flask import Flask, request
from flask import render_template

from sales.Entity.sales_predictor import SalesPredictor, SalesData
from sales.Logger.log import logging
from sales.Constants import CONFIG_DIR

ROOT_DIR = os.getcwd()
LOG_FOLDER_NAME = "logs"
PIPELINE_FOLDER_NAME = "sales"
SAVED_MODELS_DIR_NAME = "saved_models"
MODEL_CONFIG_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_DIR, "model.yaml")
LOG_DIR = os.path.join(ROOT_DIR, LOG_FOLDER_NAME)
PIPELINE_DIR = os.path.join(ROOT_DIR, PIPELINE_FOLDER_NAME)
MODEL_DIR = os.path.join(ROOT_DIR, SAVED_MODELS_DIR_NAME)

SALES_DATA_KEY = "sales_data"
ITEM_OUTLET_SALES_KEY = "item_outlet_sales"

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        logging.info("rendering index.html template.")
        return render_template('index.html')
    except Exception as e:
        logging.exception(f"error: {e}")
        return str(e)


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    context = {
        SALES_DATA_KEY: None,
        ITEM_OUTLET_SALES_KEY: None
    }

    if request.method == 'POST':
        Item_Identifier = request.form['Item_Identifier']
        Item_Weight = float(request.form['Item_Weight'])
        Item_Fat_Content = request.form['Item_Fat_Content']
        Item_Visibility = float(request.form['Item_Visibility'])
        Item_Type = request.form['Item_Type']
        Item_MRP = float(request.form['Item_MRP'])
        Outlet_Identifier = request.form['Outlet_Identifier']
        Outlet_Establishment_Year = int(request.form['Outlet_Establishment_Year'])
        Outlet_Size = request.form['Outlet_Size']
        Outlet_Location_Type = request.form['Outlet_Location_Type']
        Outlet_Type = request.form['Outlet_Type']

        sales_data = SalesData(Item_Identifier=Item_Identifier,
                               Item_Weight=Item_Weight,
                               Item_Fat_Content=Item_Fat_Content,
                               Item_Visibility=Item_Visibility,
                               Item_Type=Item_Type,
                               Item_MRP=Item_MRP,
                               Outlet_Identifier=Outlet_Identifier,
                               Outlet_Establishment_Year=Outlet_Establishment_Year,
                               Outlet_Size=Outlet_Size,
                               Outlet_Location_Type=Outlet_Location_Type,
                               Outlet_Type=Outlet_Type,
                               )
        sales_df = sales_data.get_sales_input_data_frame()
        logging.info(f"{'>'*30}prediction started{'<'*30}")
        sales_predictor = SalesPredictor(model_dir=MODEL_DIR)
        item_outlet_sales_value = sales_predictor.predict(X=sales_df)
        logging.info(f"{'>' * 30}prediction over{'<' * 30}")
        context = {
            SALES_DATA_KEY: sales_data.get_sales_data_as_dict(),
            ITEM_OUTLET_SALES_KEY: item_outlet_sales_value,
        }
        return render_template('predict.html', context=context)
    return render_template("predict.html", context=context)


if __name__ == "__main__":
    app.run(debug=True)
