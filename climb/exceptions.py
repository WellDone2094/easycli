class NotClimbCommandException(Exception):
    def __init__(self, f):
        self.message = 'Function {} is not registered as Clif command'.format(
            f.__name__)


class DuplicateArgumentException(Exception):
    def __init__(self, f, arg):
        self.message = 'Function {} already has an argument called {} or another \
        argument is defined for variable {}'.format(f.__name__, arg.name,
                                                    arg.variable)


class CommandNameConflictException(Exception):
    def __init__(self, cmd):
        self.message = 'A group or a command with this name already exists at this \
        level. {}'.format(cmd)


class InvalidCommandNameException(Exception):
    def __init__(self, name):
        self.message = "Command and group name cannot be empty, start with '-' and \
        contain '=' or empty space. {}".format(name)
