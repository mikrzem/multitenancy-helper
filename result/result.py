from __future__ import annotations
from result.error import ValidationError
from typing import List


class CommandSinkList(object):
    def entry(self, value: str):
        pass

    def entries(self, values: List[str]):
        for entry in values:
            self.entry(entry)


class CommandSinkObject(object):
    def list(self, name: str) -> CommandSinkList:
        pass

    def field(self, name: str, value: str):
        pass

    def object(self, name: str) -> CommandSinkObject:
        pass


class CommandSink(CommandSinkObject):

    def __init__(self):
        self.errors = list()

    def error(self, description: str):
        self._log_error(description)
        self._raise_error(description)

    def _raise_error(self, description: str):
        raise ValidationError(description)

    def _log_error(self, description):
        pass

    def queue_error(self, description: str):
        self.errors.append(description)

    def check_error_queue(self):
        if self.errors:
            for error in self.errors:
                self._log_error(error)
            self._raise_error('Error queue not empty')
