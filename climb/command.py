from climb.exceptions import DuplicateArgumentException, TooManyArgumentsException
from climb.argument import split_args


class Command():
    def __init__(self, function, argument_inference=False):
        self.groups = []
        self.name = None
        self.description = None
        self.f = function
        self.arguments = []
        self.arguments_map = {}
        self.info = function.__doc__.split('\n')[
            0] if function.__doc__ is not None else ''
        self.full_info = function.__doc__ or ''
        if argument_inference:
            pass
            # self.infer_arguments()

    def add_group(self, name):
        self.groups.insert(0, name)

    def add_argument(self, arg):
        if arg in self.arguments:
            raise DuplicateArgumentException(self.f, arg)
        self.arguments.insert(0, arg)
        self.arguments_map[arg.name] = arg
        if arg.short_name is not None:
            self.arguments_map[arg.short_name] = arg

    def parse_args(self, args):
        pos, kwargs = split_args(args)

        pos_i = 0
        arg_i = 0
        while pos_i < len(pos):
            if arg_i >= len(self.arguments):
                raise TooManyArgumentsException(len(self.arguments))
            n_args = self.arguments[arg_i].n_args
            if isinstance(n_args, int):
                self.arguments[arg_i].set_value(pos[pos_i:pos_i + n_args])
                pos_i += n_args
            else:
                self.arguments[arg_i].set_value(pos[pos_i:])
                pos_i = len(pos)
            arg_i += 1

        for key, value in kwargs.items():
            self.arguments_map[key].set_value(value)

    def run(self, args):
        if '-h' in args or '--help' in args:
            self.print_help()
            return

        try:
            self.parse_args(args)
        except TooManyArgumentsException as e:
            print(e.message)
            return
        function_args = {arg.variable: arg.value for arg in self.arguments}

        for arg in self.arguments:
            if arg.required and not arg.is_used:
                print('Missing {}'.format(arg.name))
                exit(1)

        self.f(**function_args)

    def build_parse_tree(self):
        pass

    def print_help(self):
        line = self.info + '\n\n' + self.name + ' '
        for arg in self.arguments:
            if arg.required:
                line += '{}=<{}> '.format(arg.name, arg.arg_type.__name__)
            else:
                line += '[{}]=<{}> '.format(arg.name, arg.arg_type.__name__)

        print(line)

    def __str__(self):
        return '.'.join(self.groups + [self.name])
