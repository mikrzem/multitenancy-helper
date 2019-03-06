from result.result import CommandSinkList, CommandSink
from typing import List
from collections import OrderedDict


class JsonCommandSinkList(CommandSinkList):
    def __init__(self, entry_list: List[str]):
        super(JsonCommandSinkList, self).__init__()
        self.entry_list = entry_list

    def entry(self, value: str):
        self.entry_list.append(value)


class JsonCommandSink(CommandSink):
    def __init__(self, container: OrderedDict = None):
        super(JsonCommandSink, self).__init__()
        self.container = container
        if self.container is None:
            self.container = OrderedDict()

    def list(self, name: str) -> CommandSinkList:
        result = list()
        self.container[name] = result
        return JsonCommandSinkList(result)

    def field(self, name: str, value: str):
        self.container[name] = value

    def object(self, name: str) -> CommandSink:
        result = OrderedDict()
        self.container[name] = result
        return JsonCommandSink(result)

    def _log_error(self, description):
        if 'Errors' not in self.container:
            self.container['Errors'] = list()
        self.container['Errors'].append(description)
