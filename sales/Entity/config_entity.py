from collections import namedtuple

DataIngestionConfig = namedtuple('DataIngestionConfig',
                                 ['DATA_INGESTION_TRAIN_DATA_DOWNLOAD_URL', 'DATA_INGESTION_TEST_DATA_DOWNLOAD_URL',
                                  'DATA_INGESTION_DATA_DIR'])

TrainingPipelineConfig = namedtuple("TrainingPipelineConfig", ["artifact_dir"])
