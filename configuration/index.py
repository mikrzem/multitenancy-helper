from configuration import app_directory
from configuration.target import TargetConfiguration
from typing import List
import os
import json

index_file_path = os.path.join(app_directory, '.index.json')
configurations: List[str] = []

try:
    with open(index_file_path, encoding='utf-8') as source_file:
        configurations = json.load(source_file)
except OSError:
    pass


def get_configuration(name: str) -> TargetConfiguration:
    return TargetConfiguration(name)


def add_configuration(name: str):
    if name not in configurations:
        configurations.append(name)
        with open(index_file_path, 'w', encoding='utf-8') as target_file:
            json.dump(configurations, target_file, ensure_ascii=False)
            print('Updated configuration index')


def select_configurations() -> List[TargetConfiguration]:
    return list(map(get_configuration, configurations))
