from commands import GenericCommand
from commands.target import AddTargetCommand
from commands.blank import BlankCommand
from commands.view import ViewCommand
from commands.validate import ValidateCommand


def parse_command(arguments) -> GenericCommand:
    if arguments.command == 'target':
        return AddTargetCommand(
            arguments.name,
            arguments.host,
            arguments.port,
            arguments.username,
            arguments.password,
            arguments.group,
            arguments.schema,
            arguments.remove
        )
    elif arguments.command == 'view':
        return ViewCommand(
            arguments.name
        )
    elif arguments.command == 'validate':
        return ValidateCommand(
            arguments.name,
            arguments.group,
            arguments.all
        )
    else:
        return BlankCommand()
