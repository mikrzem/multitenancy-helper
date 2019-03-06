from command import GenericCommand
from configuration.index import get_configuration, select_configurations
from connection.database import DatabaseConnection, Error
from result.result import CommandSink, CommandSinkObject
from configuration.target import TargetConfiguration


class ValidateCommand(GenericCommand):

    def __init__(self, name: str, group: str, check_all: bool, sink: CommandSink):
        super(ValidateCommand, self).__init__(sink)
        self.name = name
        self.group = group
        self.check_all = check_all

    def validate(self):
        if not self.name and not self.check_all:
            self.sink.queue_error('Use --all to check all configurations')
        self.sink.check_error_queue()

    def execute(self):
        if self.name:
            self.validate_name(self.name)
        elif self.check_all:
            print('Validating all configurations')
            for configuration in select_configurations():
                self.validate_configuration(configuration, self.sink.object(configuration.name))
        else:
            self.sink.error('Use --all to check all configurations')

    def validate_name(self, name: str):
        configuration = get_configuration(name)
        if not configuration.loaded:
            self.sink.field('Configuration does not exist', name)
        else:
            self.sink.field('Configuration exists', name)
            self.validate_configuration(configuration, self.sink.object(name))

    def validate_configuration(self, configuration: TargetConfiguration, sink: CommandSinkObject):
        sink.field('Validating', 'true')
        try:
            with DatabaseConnection(configuration) as connection:
                sink.field('Connection', 'true')
                self.validate_connection(configuration, connection, sink)
        except Error as error:
            sink.field('Connection', 'false')
            sink.field('Error', str(error.args))

    def validate_connection(self, configuration, connection: DatabaseConnection, sink: CommandSinkObject):
        schema_sink = sink.object('Schemas')
        for schema in configuration.get_schemas(self.group):
            inner_sink = schema_sink.object(schema)
            try:
                connection.use_schema(schema)
                inner_sink.field('Connection', 'true')
            except Error as error:
                inner_sink.field('Connection', 'false')
                inner_sink.field('Error', str(error.args))
