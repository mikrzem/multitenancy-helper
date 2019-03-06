from command import GenericCommand
from result.result import CommandSink


class BlankCommand(GenericCommand):

    def __init__(self, sink: CommandSink):
        super(BlankCommand, self).__init__(sink)

    def execute(self):
        self.sink.field('result', 'Not actions taken')
