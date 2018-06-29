import sys

from climb.argument import Argument
from climb.command import Command
from climb.group import Group
from climb.utils import validate_command_name


class Cli():
    def __init__(self):
        self.commands = set()
        self.default_command = None
        self.parse_tree = {}
        self.baseGroup = Group()

    def group(self, name):
        validate_command_name(name)

        def decorator(f):
            self._create_command(f)
            f.__clif__.add_group(name)
            return f

        return decorator

    def command(self, name):
        validate_command_name(name)

        def decorator(f):
            self._create_command(f)
            self.commands.add(f.__clif__)
            f.__clif__.name = name

            return f

        return decorator

    def argument(self,
                 name,
                 shortName=None,
                 argType=str,
                 required=False,
                 variable=None,
                 default=None):
        arg = Argument(name, shortName, argType, required, variable, default)

        def decorator(f):
            self._create_command(f)

            f.__clif__.add_argument(arg)
            return f

        return decorator

    def _create_command(self, f):
        if not hasattr(f, '__clif__'):
            f.__clif__ = Command(f)

    def run(self):
        self.baseGroup.commands = self.commands
        self.baseGroup.build_parse_tree()
        self.baseGroup.run(sys.argv[1:])

    def print(self):
        self.baseGroup.print()
