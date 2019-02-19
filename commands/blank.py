from commands import GenericCommand


class BlankCommand(GenericCommand):

    def execute(self):
        print('Not actions taken')
