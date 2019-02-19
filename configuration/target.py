from configuration import app_directory
from typing import List, Dict
import json
import os


class TargetConfiguration:

    def __init__(self, name: str):
        self.name = name
        self.host: str = ''
        self.port: int = 0
        self.username: str = ''
        self.password: str = ''
        self.schemas: List[str] = []
        self.groups: Dict[str, List[str]] = {}
        try:
            with open(self.file_path(), encoding='utf-8') as source_file:
                self.__dict__ = json.load(source_file)
            self.loaded = True
        except OSError:
            self.loaded = False
        self.name = name

    def file_path(self) -> str:
        return os.path.join(app_directory, self.name + '.json')

    def save(self):
        with open(self.file_path(), 'w', encoding='utf-8') as target_file:
            json.dump(
                self.serialized(),
                target_file,
                ensure_ascii=False,
                indent=4,
                sort_keys=True
            )

    def add_schemas(self, group: str, schemas: List[str]):
        if group and group not in self.groups:
            self.groups[group] = []
        for schema in schemas:
            if schema not in self.schemas:
                self.schemas.append(schema)
            if group and schema not in self.groups[group]:
                self.groups[group].append(schema)

    def remove_schemas(self, group: str, schemas: List[str]):
        if group and group not in self.groups:
            print('Group {group} does not exist.'.format(group=group))
            return
        for schema in schemas:
            if group:
                if schema in self.groups[group]:
                    self.groups[group].remove(schema)
            else:
                if schema in self.schemas:
                    self.schemas.remove(schema)
        if group and not self.groups[group]:
            self.groups.pop(group, None)

    def get_schemas(self, group: str = '') -> List[str]:
        if not group:
            return self.schemas
        elif group in self.groups:
            return self.groups[group]
        else:
            return []

    def serialized(self):
        copy = self.__dict__.copy()
        copy.pop('name', None)
        copy.pop('loaded', None)
        return copy
