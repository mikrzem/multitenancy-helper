from commands import GenericCommand
from typing import List
from configuration.target import TargetConfiguration
from configuration.index import get_configuration, add_configuration


class AddTargetCommand(GenericCommand):

    def __init__(
            self,
            name: str,
            host: str,
            port: int,
            username: str,
            password: str,
            group: str,
            schemas: List[str],
            remove: List[str]
    ):
        self.name: str = name
        self.host: str = host
        self.port: int = port
        self.username: str = username
        self.password: str = password
        self.group: str = group
        self.schemas: List[str] = schemas
        self.remove: List[str] = remove
        self.configuration: TargetConfiguration = None

    def execute(self):
        if self.configuration.loaded:
            print('Updating configuration: ' + self.configuration.name)
        else:
            print('Creating configuration: ' + self.configuration.name)
        if self.host:
            self.configuration.host = self.host
            print('Set host: ' + self.host)
        if self.port:
            self.configuration.port = self.port
            print('Set port: ' + str(self.port))
        if self.username:
            self.configuration.username = self.username
            print('Set username: ' + self.username)
        if self.password:
            self.configuration.password = self.password
            print('Set password: <set>')
        if self.schemas:
            self.configuration.add_schemas(self.group, self.schemas)
            print('Added schemas')
        if self.remove:
            self.configuration.remove_schemas(self.group, self.remove)
            print('Removed schemas')
        self.configuration.save()
        print('Saved configuration: ' + self.configuration.name)
        add_configuration(self.configuration.name)

    def validate(self):
        if not self.name:
            raise Exception('Missing name')
        self.configuration = get_configuration(self.name)
        if not self.host and not self.configuration.host:
            raise Exception('Missing host')
        if not self.port and not self.configuration.port:
            raise Exception('Missing port')
        if not self.username and not self.configuration.username:
            raise Exception('Missing username')
        if not self.password and not self.configuration.password:
            raise Exception('Missing password')
