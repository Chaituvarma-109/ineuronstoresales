from collections import namedtuple

DataIngestionConfig = namedtuple('DataIngestionConfig',
                                 ['DATA_INGESTION_TRAIN_DATA_DOWNLOAD_URL', 'DATA_INGESTION_TEST_DATA_DOWNLOAD_URL',
                                  'DATA_INGESTION_DATA_DIR'])

# 'report_file_path', 'report_page_file_path'
DatavalidationConfig = namedtuple('DatavalidationConfig', ['schema_file_path'])

DataTransformationConfig = namedtuple('DataTransformationConfig', ['Item_Type_Combined', 'Years_Established',
                                                                   'Item_Fat_Content', 'Item_Visibility',
                                                                   'transformed_train_dir', 'transformed_test_dir',
                                                                   'preprocessed_obj_file_path']
                                      )

TrainingPipelineConfig = namedtuple("TrainingPipelineConfig", ["artifact_dir"])
