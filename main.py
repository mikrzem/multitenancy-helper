from arguments import parser
from command.parser import parse_command


def main():
    arguments = parser.parse_args()
    command = parse_command(arguments)
    command.validate()
    command.execute()


if __name__ == '__main__':
    main()
