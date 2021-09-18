import os


def get_data_collection_services_path() -> str:
    return os.environ.get('DATA_COLLECTION_SERVICES_PATH',
                          '/home/idol/zucc/src/data_collection_services')


def get_personal_data_filepath() -> str:
    return os.environ.get('DATA_COLLECTION_DATA_JSON_PATH',
                          '/storage/personal_data_collection/zuccs_dream.json')


def get_log_root_folder_path() -> str:
    return os.environ.get('DATA_COLLECTION_ROOT_LOG_PATH',
                          '/home/idol/data_collection_logs')
