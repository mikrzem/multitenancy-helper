import re
from typing import List

from commands import GenericCommand
from configuration.index import get_configuration, select_configurations
from configuration.target import TargetConfiguration
from connection.database import DatabaseConnection, Error


class ExecuteCommand(GenericCommand):

    def __init__(self, name: str, group: str, query: str, file: str, transaction: bool, check_all: bool):
        self.name = name
        self.group = group
        self.query = query
        self.file = file
        self.transaction = transaction
        self.check_all = check_all

    def validate(self):
        if not self.name and not self.check_all:
            raise Exception('Use --all to check all configurations')

    def execute(self):
        if self.name:
            configuration = get_configuration(self.name)
            if not configuration.loaded:
                raise Exception('Configuration {name} not loaded'.format(name=self.name))
            self.run_query(configuration)
        elif self.check_all:
            for configuration in select_configurations():
                self.run_query(configuration)

    def run_query(self, configuration: TargetConfiguration):
        queries = self.find_queries()
        connection = DatabaseConnection(configuration)
        for schema in configuration.get_schemas(self.group):
            try:
                self.run_queries_on_schema(queries, connection, schema)
            except Error as error:
                print(
                    'Failed to execute queries on {name} / {schema} with error:\r\n{error}'.format(
                        name=self.name,
                        schema=schema,
                        error=str(error.args)
                    )
                )

    def find_queries(self) -> List[str]:
        if self.query:
            return [self.query]
        elif self.file:
            return self.read_query_file(self.file)
        else:
            return []

    def read_query_file(self, file: str) -> List[str]:
        result = []
        statement = ""
        for line in open(file):
            if re.match(r'--', line):  # ignore sql comment lines
                continue
            if not re.search(r'[^-;]+;', line):  # keep appending lines that don't end in ';'
                statement = statement + " " + line
            else:  # when you get a line ending in ';' then exec statement and reset for next statement
                result.append(statement + " " + line)
                statement = ""
        return result

    def run_queries_on_schema(self, queries: List[str], connection: DatabaseConnection, schema: str):
        connection.use_schema(schema)
        if self.transaction:
            with connection.transaction() as transaction:
                self.execute_queries(connection, queries)
                transaction.commit()
        else:
            self.execute_queries(connection, queries)

    def execute_queries(self, connection: DatabaseConnection, queries: List[str]):
        for query in queries:
            print('Executing query: ' + query)
            response = connection.execute(query)
            if response.success:
                print('Query changed {rows} rows'.format(rows=response.rows))
            else:
                raise Exception('Failed to execute query')
