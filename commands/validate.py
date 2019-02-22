from commands import GenericCommand
from configuration.index import get_configuration, select_configurations
from connection.database import DatabaseConnection, Error


class ValidateCommand(GenericCommand):

    def __init__(self, name: str, group: str, check_all: bool):
        self.name = name
        self.group = group
        self.check_all = check_all

    def validate(self):
        if not self.name and not self.check_all:
            raise Exception('Use --all to check all configurations')

    def execute(self):
        if self.name:
            self.validate_name(self.name)
        elif self.check_all:
            print('Validating all configurations')
            for configuration in select_configurations():
                self.validate_configuration(configuration)
        else:
            print('Use --all to check all configurations')

    def validate_name(self, name):
        configuration = get_configuration(name)
        if not configuration.loaded:
            print('Configuration {name} does not exist'.format(name=name))
        else:
            print('Configuration {name} exists'.format(name=name))
            self.validate_configuration(configuration)

    def validate_configuration(self, configuration):
        print('Validating configuration: {name}'.format(name=configuration.name))
        try:
            with DatabaseConnection(configuration) as connection:
                print('Successfully connected to database configuration: {name}'.format(name=configuration.name))
                self.validate_connection(configuration, connection)
        except Error as error:
            print('Failed to connect to database: {name} \r\n{error}'.format(
                name=configuration.name,
                error=str(error.args)
            ))

    def validate_connection(self, configuration, connection: DatabaseConnection):
        for schema in configuration.get_schemas(self.group):
            try:
                connection.use_schema(schema)
                print('Successfully connected to schema: {schema}'.format(schema=schema))
            except Error as error:
                print('Failed to connect to schema: {schema} \r\n{error}'.format(
                    schema=schema,
                    error=str(error.args)
                ))
