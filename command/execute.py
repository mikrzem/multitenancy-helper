import re
from typing import List

import sys

from command import GenericCommand
from configuration.index import get_configuration, select_configurations
from configuration.target import TargetConfiguration
from connection.database import DatabaseConnection, Error
from result.result import CommandSink, CommandSinkObject


class ExecuteCommand(GenericCommand):

    def __init__(self,
                 name: str,
                 group: str,
                 query: str,
                 file: str,
                 transaction: bool,
                 check_all: bool,
                 continue_on_error: bool,
                 sink: CommandSink):
        super(ExecuteCommand, self).__init__(sink)
        self.name = name
        self.group = group
        self.query = query
        self.file = file
        self.transaction = transaction
        self.check_all = check_all
        self.continue_on_error = continue_on_error

    def validate(self):
        if not self.name and not self.check_all:
            self.sink.queue_error('Use --all to check all configurations')
        if not self.query and not self.file:
            self.sink.queue_error('Provide query text or file')
        self.sink.check_error_queue()

    def execute(self):
        if self.name:
            configuration = get_configuration(self.name)
            if not configuration.loaded:
                self.sink.error('Configuration {name} not loaded'.format(name=self.name))
            self.run_query(configuration, self.sink.object(configuration.name))
        elif self.check_all:
            for configuration in select_configurations():
                self.run_query(configuration, self.sink.object(configuration.name))

    def run_query(self, configuration: TargetConfiguration, sink: CommandSinkObject):
        queries = self.find_queries()
        with DatabaseConnection(configuration) as connection:
            for schema in configuration.get_schemas(self.group):
                schema_sink = sink.object('Executing queries on schema {schema}'.format(schema=schema))
                try:
                    self.run_queries_on_schema(queries, connection, schema, schema_sink)
                except Error as error:
                    schema_sink.field(
                        'Failed to execute queries on {name} / {schema} with error:'.format(
                            name=self.name,
                            schema=schema
                        ),
                        str(error.args)
                    )

    def find_queries(self) -> List[str]:
        if self.query:
            return self.read_query_lines(self.query.splitlines())
        elif self.file:
            return self.read_query_file(self.file)
        else:
            return []

    def read_query_file(self, file: str) -> List[str]:
        with open(file) as query_file:
            return self.read_query_lines(query_file)

    def read_query_lines(self, lines) -> List[str]:
        result = []
        statement = ""
        for line in lines:
            if re.match(r'--', line):  # ignore sql comment lines
                continue
            if not re.search(r'[^-;]+;', line):  # keep appending lines that don't end in ';'
                statement = statement + " " + line
            else:  # when you get a line ending in ';' then exec statement and reset for next statement
                result.append(statement + " " + line)
                statement = ""
        return list(filter(lambda x: bool(x.strip()), result))

    def run_queries_on_schema(self,
                              queries: List[str],
                              connection: DatabaseConnection,
                              schema: str,
                              sink: CommandSinkObject):
        connection.use_schema(schema)
        try:
            if self.transaction:
                connection.disable_autocommit()
                with connection.transaction() as transaction:
                    sink.field('transaction', 'true')
                    self.execute_queries(connection, queries, sink)
                    transaction.commit()
            else:
                sink.field('transaction', 'false')
                connection.use_autocommit()
                self.execute_queries(connection, queries, sink)
        except Exception as error:
            print(error)
            if not self.continue_on_error:
                raise error

    def execute_queries(self, connection: DatabaseConnection, queries: List[str], sink: CommandSinkObject):
        index = 1
        for query in queries:
            query_sink = sink.object(str(index))
            index += 1
            query_sink.field('Executing query', query)
            response = connection.execute(query)
            if response.success:
                query_sink.field('Query success', 'true')
                query_sink.field('Query changed rows', response.rows)
            else:
                query_sink.field('Query success', 'false')
                raise Exception('Failed to execute query')
