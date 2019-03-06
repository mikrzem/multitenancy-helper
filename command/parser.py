from command import GenericCommand
from command.blank import BlankCommand
from command.execute import ExecuteCommand
from command.target import TargetCommand
from command.validate import ValidateCommand
from command.view import ViewCommand
from result.print import PrintCommandSink
from command.web import WebCommand


def parse_command(arguments) -> GenericCommand:
    if arguments.command == 'target':
        return TargetCommand(
            arguments.name,
            arguments.host,
            arguments.port,
            arguments.username,
            arguments.password,
            arguments.group,
            arguments.schema,
            arguments.remove,
            PrintCommandSink()
        )
    elif arguments.command == 'view':
        return ViewCommand(
            arguments.name,
            PrintCommandSink()
        )
    elif arguments.command == 'validate':
        return ValidateCommand(
            arguments.name,
            arguments.group,
            arguments.all,
            PrintCommandSink()
        )
    elif arguments.command == 'execute':
        return ExecuteCommand(
            arguments.name,
            arguments.group,
            arguments.query,
            arguments.file,
            arguments.transaction,
            arguments.all,
            PrintCommandSink()
        )
    elif arguments.command == 'web':
        return WebCommand(
            arguments.port,
            PrintCommandSink()
        )
    else:
        return BlankCommand(PrintCommandSink())
