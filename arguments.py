import argparse

parser = argparse.ArgumentParser(description='Executes sql queries against multiple databases.')
subparsers = parser.add_subparsers(dest='command')
# target arguments
target_parser = subparsers.add_parser(
    'target',
    help='add another target database or modify configuration'
)
target_parser.add_argument(
    '--name',
    help='name of database configuration',
    action='store',
    required=True
)
target_parser.add_argument(
    '--host',
    help='database host configuration',
    action='store'
)
target_parser.add_argument(
    '--port',
    help='database port configuration',
    action='store',
    type=int
)
target_parser.add_argument(
    '--username',
    help='database username configuration',
    action='store'
)
target_parser.add_argument(
    '--password',
    help='database password configuration',
    action='store'
)
target_parser.add_argument(
    '--group',
    help='name of group of database schemas',
    action='store'
)
target_parser.add_argument(
    '-s', '--schema',
    help='database schema to add to group and configuration',
    action='append'
)
target_parser.add_argument(
    '-r', '--remove',
    help='database schema to remove from group or configuration',
    action='append'
)
# view arguments
view_parser = subparsers.add_parser(
    'view',
    help='view current configuration'
)
view_parser.add_argument(
    '--name',
    help='name of database configuration',
    action='store'
)
# execute arguments
execute_parser = subparsers.add_parser(
    'execute',
    help='execute script on selected databases'
)
execute_parser.add_argument(
    '--name',
    help='name of database configuration',
    action='store'
)
execute_parser.add_argument(
    '--group',
    help='name of group of database schemas',
    action='store'
)
execute_parser.add_argument(
    '--query',
    help='sql query to execute',
    action='store'
)
execute_parser.add_argument(
    '--file',
    help='file with sql query to execute',
    action='store'
)
execute_parser.add_argument(
    '--transaction',
    help='use transaction and rollback on error',
    action='store_true'
)
# validate arguments
validate_parser = subparsers.add_parser(
    'validate',
    help='validate current configurations'
)
validate_parser.add_argument(
    '--name',
    help='name of database configuration',
    action='store'
)
validate_parser.add_argument(
    '--group',
    help='name of group of database schemas',
    action='store'
)
validate_parser.add_argument(
    '--all',
    help='confirms that all configurations are to be checked',
    action='store_true'
)
