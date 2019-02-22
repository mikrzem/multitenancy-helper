from mysql.connector import CMySQLConnection, connect, Error
from mysql.connector.cursor_cext import CMySQLCursor

from configuration.target import TargetConfiguration


class DatabaseResponse:
    def __init__(self, success: bool, rows: int = 0):
        self.success = success
        self.rows = rows


class DatabaseTransaction:
    def __init__(self, connection: CMySQLConnection):
        self.connection = connection
        self.finalized = False

    def __enter__(self):
        self.connection.start_transaction()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.finalized:
            self.rollback()

    def rollback(self):
        self.connection.rollback()
        self.finalized = True

    def commit(self):
        self.connection.commit()
        self.finalized = True


class DatabaseConnection:

    def __init__(self, configuration: TargetConfiguration):
        self.configuration = configuration
        self.connection: CMySQLConnection = None
        self.cursor: CMySQLCursor = None

    def __enter__(self):
        self.connection = connect(
            user=self.configuration.username,
            password=self.configuration.password,
            host=self.configuration.host,
            port=self.configuration.port
        )
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()

    def use_schema(self, name: str):
        self.cursor.execute('USE ' + name)

    def execute(self, query: str) -> DatabaseResponse:
        try:
            self.cursor.execute(query)
            return DatabaseResponse(True, self.cursor.rowcount)
        except Error as error:
            print('Error executing statement {query}: \r\n{error}'.format(
                query=query,
                error=str(error.args)
            ))
            return DatabaseResponse(False)

    def transaction(self):
        return DatabaseTransaction(self.connection)
