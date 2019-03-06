from command import GenericCommand
from typing import List
from configuration.target import TargetConfiguration
from configuration.index import get_configuration, add_configuration
from result.result import CommandSink


class TargetCommand(GenericCommand):

    def __init__(self,
                 name: str,
                 host: str,
                 port: int,
                 username: str,
                 password: str,
                 group: str,
                 schemas: List[str],
                 remove: List[str],
                 sink: CommandSink):
        super(TargetCommand, self).__init__(sink)
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
            sink = self.sink.object('Updating configuration')
        else:
            sink = self.sink.object('Creating configuration')
        sink.field('Name', self.configuration.name)
        if self.host:
            self.configuration.host = self.host
            sink.field('Host', self.host)
        if self.port:
            self.configuration.port = self.port
            sink.field('Port', str(self.port))
        if self.username:
            self.configuration.username = self.username
            sink.field('Username', self.username)
        if self.password:
            self.configuration.password = self.password
            sink.field('Password', self.password)
        if self.schemas:
            self.configuration.add_schemas(self.group, self.schemas)
            add_schema_sink = sink.object('Added schemas')
            add_schema_sink.field('Group', self.group)
            add_schema_sink.list('Schemas').entries(self.schemas)
        if self.remove:
            self.configuration.remove_schemas(self.group, self.remove)
            remove_schema_sink = sink.object('Removed schemas')
            remove_schema_sink.field('Group', self.group)
            remove_schema_sink.list('Schemas').entries(self.remove)
        self.configuration.save()
        self.sink.field('Saved configuration', self.configuration.name)
        add_configuration(self.configuration.name)

    def validate(self):
        if not self.name:
            self.sink.error('Missing name')
        self.configuration = get_configuration(self.name)
        if not self.host and not self.configuration.host:
            self.sink.queue_error('Missing host')
        if not self.port and not self.configuration.port:
            self.sink.queue_error('Missing port')
        if not self.username and not self.configuration.username:
            self.sink.queue_error('Missing username')
        if not self.password and not self.configuration.password:
            self.sink.queue_error('Missing password')
        self.sink.check_error_queue()
