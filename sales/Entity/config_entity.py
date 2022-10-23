from collections import namedtuple

DataIngestionConfig = namedtuple('DataIngestionConfig',
                                 ['DATA_INGESTION_TRAIN_DATA_DOWNLOAD_URL', 'DATA_INGESTION_TEST_DATA_DOWNLOAD_URL',
                                  'DATA_INGESTION_DATA_DIR'])

DatavalidationConfig = namedtuple('DatavalidationConfig', ['schema_file_path', 'report_file_path',
                                                           'report_page_file_path'])

TrainingPipelineConfig = namedtuple("TrainingPipelineConfig", ["artifact_dir"])
