from commands import GenericCommand
from configuration.target import TargetConfiguration
from configuration.index import get_configuration, select_configurations
import json


class ViewCommand(GenericCommand):

    def __init__(self, name: str = ""):
        self.name = name

    def execute(self):
        if self.name:
            self.show_configuration(get_configuration(self.name))
        else:
            print('Viewing all configurations')
            for configuration in select_configurations():
                self.show_configuration(configuration)

    def show_configuration(self, configuration: TargetConfiguration):
        print('Viewing configuration: ' + configuration.name)
        print(json.dumps(configuration.serialized(), indent=4, sort_keys=True))
