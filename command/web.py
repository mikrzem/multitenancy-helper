from command import GenericCommand
from result.result import CommandSink
from web import app
from webbrowser import open


class WebCommand(GenericCommand):

    def __init__(self, port: int, sink: CommandSink):
        super(WebCommand, self).__init__(sink)
        self.port = port

    def validate(self):
        if not self.port:
            self.sink.queue_error('Missing port')
        self.sink.check_error_queue()

    def execute(self):
        self.sink.object('Starting web application') \
            .field('port', str(self.port))
        open('http://localhost:' + str(self.port))
        app.run(port=self.port)
