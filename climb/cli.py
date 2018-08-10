"""Cli class."""
import sys

from climb.argument import Argument
from climb.command import Command
from climb.group import Group
from climb.utils import validate_command_name


class Cli():
    """Command line class."""

    def __init__(self, description=None):
        """Constructor.

        Parameters
        ----------
        description: str
            CLI description that will be display in man page.

        """
        self.commands = set()
        self.default_command = None
        self.parse_tree = {}
        self.base_group = Group()
        self.description = description

    def group(self, name):
        """Specify a command group.

        Parameters
        ----------
        name: str
            Group name

        """
        validate_command_name(name)

        def decorator(f):
            self._create_command(f)
            f.__climb__.add_group(name)
            return f

        return decorator

    def command(self, name, description=None):
        """Add a CLI command.

        Parameters
        ----------
        name: str
            Command name.
        description: str
            Command description to be used inside man page, default None.

        """
        validate_command_name(name)

        def decorator(f):
            self._create_command(f)
            self.commands.add(f.__climb__)
            f.__climb__.name = name
            f.__climb__.description = description

            return f

        return decorator

    def argument(self, *args, **kwargs):
        """Specify an argument for a command.

        Parameters
        ----------
        Check climb.argument.Argument constructor.

        """
        arg = Argument(*args, **kwargs)

        def decorator(f):
            self._create_command(f)

            f.__climb__.add_argument(arg)
            return f

        return decorator

    def _create_command(self, f):
        """Ensure that function f has variable __climb__."""
        if not hasattr(f, '__climb__'):
            f.__climb__ = Command(f)

    def run(self):
        """Parse program arguments."""
        self.base_group.commands = self.commands
        self.base_group.build_parse_tree()
        self.base_group.run(sys.argv[1:])
