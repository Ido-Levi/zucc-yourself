import sys
import pathlib
import logging
import json

from importlib import import_module
from typing import List, Optional, Dict
from glob import glob

from os.path import join, exists

from collector_base import CollectorService
from consts import get_data_collection_services_path, get_personal_data_filepath, \
    get_log_root_folder_path


class CollectionManager(object):
    __slots__ = ('data_collection_services',
                 'personal_data',
                 'logger',
                 )

    def __init__(self, data_collection_services: Optional[List[CollectorService]] = None,
                 personal_data: Optional[Dict] = None):

        self.logger: logging.Logger = logging.getLogger('data_collection_logger')
        self.setup_logger()
        self.data_collection_services: List[CollectorService] = data_collection_services \
            if data_collection_services else self.get_all_data_collection_services()
        self.personal_data: Dict = personal_data if personal_data \
            else self.get_personal_data_json()

    def setup_logger(self) -> None:
        """
        Initialize the logger
        :return: Nothing
        """
        level = logging.INFO

        self.logger.setLevel(level)

        fh = logging.FileHandler(join(get_log_root_folder_path(),
                                      'data_collection_log.txt'))
        fh.setLevel(level)

        ch = logging.StreamHandler()
        ch.setLevel(level)

        self.logger.addHandler(ch)
        self.logger.addHandler(fh)

    def get_all_data_collection_services(self) -> List[CollectorService]:
        """
        Gets all the data collection services dynamically
        :return: All the data collection services
        """
        all_data_collection_services: List[CollectorService] = []

        all_services_path = get_data_collection_services_path()
        all_unloaded_services = glob(join(all_services_path, '*.py'))
        self.logger.info(f'Starting to load all the data collection services - '
                         f'there are {len(all_unloaded_services)} services')
        sys.path.append(all_services_path)

        for unloaded_dcs in all_unloaded_services:
            try:
                module_name = pathlib.Path(unloaded_dcs).stem
                self.logger.info(f'Trying to load {module_name}')
                dcs = import_module(module_name)
                all_data_collection_services.append(dcs.init_data_collection_service())
                self.logger.info(f'Successfully loaded {module_name}!')
            except Exception as ex:
                self.logger.info(f'Failed to load {module_name} :(\n{ex}')

        return all_data_collection_services

    # TODO: Encrypt the personal data file in a gpg/ other way to make sure that
    #  zucc's dream won't come true
    def get_personal_data_json(self) -> Dict:
        """
        Gets all the personal data as a json
        :return: All of my valuable personal data in a json form
        """
        try:
            personal_data_filepath = get_personal_data_filepath()
            if not exists(personal_data_filepath):
                return {}
            personal_data_file = open(personal_data_filepath, 'r')
            personal_data = json.load(personal_data_file)
            personal_data_file.close()
            return personal_data
        except Exception as ex:
            self.logger.error(f'Reading the personal data file has failed!\n{ex}')
            sys.exit(1)


if __name__ == '__main__':
    s = CollectionManager()
