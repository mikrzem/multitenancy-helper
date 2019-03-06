from result.result import CommandSink


class GenericCommand(object):

    def __init__(self, sink: CommandSink):
        self.sink = sink

    def execute(self):
        pass

    def validate(self):
        pass
