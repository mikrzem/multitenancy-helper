from command import GenericCommand
from configuration.target import TargetConfiguration
from configuration.index import get_configuration, select_configurations
from result.result import CommandSink
import json


class ViewCommand(GenericCommand):

    def __init__(self, name: str, sink: CommandSink):
        super(ViewCommand, self).__init__(sink)
        self.name = name

    def execute(self):
        if self.name:
            self.show_configuration(get_configuration(self.name))
        else:
            print('Viewing all configurations')
            for configuration in select_configurations():
                self.show_configuration(configuration)

    def show_configuration(self, configuration: TargetConfiguration):
        view_sink = self.sink.object('Configuration: ' + configuration.name)
        view_sink.field('Host', configuration.host)
        view_sink.field('Port', str(configuration.port))
        view_sink.field('Username', configuration.username)
        view_sink.field('Password', configuration.password)
        view_sink.list('Schemas').entries(configuration.schemas)
        groups_sink = view_sink.object('Groups')
        for group_name, group in configuration.groups.items():
            groups_sink.list(group_name).entries(group)
