from climb.exceptions import DuplicateArgumentException, TooManyArgumentsException


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
        arg_index = 0
        allow_positional = True
        while arg_index < len(args):
            if arg_index >= len(self.arguments):
                raise TooManyArgumentsException(len(self.arguments))
            arg = args[arg_index]

            # positional argument
            if arg[0] != '-' and allow_positional:
                self.arguments[arg_index].set_value(arg)
                arg_index += 1
                continue

            # disable positional argument when the first non positional argument
            # is found
            allow_positional = False

            # key argument. Ex -v or --verbose
            arg_name = arg.split('=')[0]
            if arg_name not in self.arguments_map:
                print('Invalid argument {}'.format(arg_name))
                exit(1)

            if len(arg.split('=')) > 1:
                value = arg[arg.find('=') + 1:]
                self.arguments_map[arg_name].set_value(value)
            else:
                arg_index += 1
                if arg_index >= len(args):
                    print('Missing value for argument {}'.format(arg))
                    exit(1)
                self.arguments_map[arg_name].set_value(args[arg_index])

            arg_index += 1

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
