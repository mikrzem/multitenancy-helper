from result.result import CommandSinkList, CommandSink
import datetime


def indent_prefix(indent: int) -> str:
    return str(datetime.datetime.now()) + ' ' + ('  ' * indent)


class PrintCommandSinkList(CommandSinkList):

    def __init__(self, indent: int):
        super(PrintCommandSinkList, self).__init__()
        self.indent = indent

    def entry(self, value: str):
        print(indent_prefix(self.indent) + value)


class PrintCommandSink(CommandSink):

    def __init__(self, indent: int = 0):
        super(PrintCommandSink, self).__init__()
        self.indent = indent

    def list(self, name: str) -> CommandSinkList:
        print(indent_prefix(self.indent) + '[' + name + ']')
        return PrintCommandSinkList(self.indent + 1)

    def field(self, name: str, value: str):
        print(indent_prefix(self.indent) + name + ': ' + value)

    def object(self, name: str) -> CommandSink:
        print(indent_prefix(self.indent) + '{' + name + '}')
        return PrintCommandSink(self.indent + 1)

    def _log_error(self, description):
        print(description)
