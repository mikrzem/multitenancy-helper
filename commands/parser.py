from commands import GenericCommand
from commands.blank import BlankCommand
from commands.execute import ExecuteCommand
from commands.target import AddTargetCommand
from commands.validate import ValidateCommand
from commands.view import ViewCommand


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
    elif arguments.command == 'execute':
        return ExecuteCommand(
            arguments.name,
            arguments.group,
            arguments.query,
            arguments.file,
            arguments.transaction,
            arguments.all
        )
    else:
        return BlankCommand()
