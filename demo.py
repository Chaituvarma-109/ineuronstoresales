import os

from sales.Pipeline.pipeline import Pipeline
from sales.Config.configuration import Configuration
from sales.Logger.log import logging


def main():
    try:
        config_path = os.path.join("config", 'config.yaml')
        pipeline = Pipeline(Configuration(config_file_path=config_path))
        pipeline.start()
        logging.info("main function execution completed.")
    except Exception as e:
        logging.error(f"{e}")
        print(e)


if __name__ == "__main__":
    main()
