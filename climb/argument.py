"""Climb CLI arguments."""


class Argument():
    """Argument class."""

    def __init__(self,
                 name,
                 short_name=None,
                 arg_type=str,
                 n_args=1,
                 required=None,
                 variable=None,
                 default=None):
        """Constructor.

        Parameters
        ----------
        name: str
            Argument name without '--'.
        short_name: str
            Single character argument, default None.
        arg_type: type
            Argument type, default str.
        required: bool
            If True the argument is required.
        variable: str
            Name of the argument inside the function, if None `name` will be
            used. Default None.
        default: any
            Default value to use if argument is not required. Default None

        """
        assert (short_name is None or len(short_name) == 1)

        self.name = '--' + name if len(name) > 1 else '-' + name
        self.short_name = short_name if short_name is None else '-' + short_name
        self.arg_type = arg_type
        self.variable = variable or name
        self.required = required or default is None
        self.value = default
        self.is_used = False

        if (isinstance(n_args, int) and n_args > 0) or n_args == 'N':
            self.n_args = n_args
        else:
            raise ValueError("n_args must be an integer > 0 or N")

    def __eq__(self, arg):
        """Equality operator."""
        return arg.name == self.name or self.variable == arg.variable

    def set_value(self, values):
        """Set argument value.

        Parameters
        ----------
        value: str
            value read from sys.argv

        """
        if self.is_used:
            print("Duplicated argument", self.name)
            exit(1)

        if self.n_args != 'N' and len(values) != self.n_args:
            print("Expected {} values for {}".format(self.n_args, self.name))
            exit(1)

        values_t = []
        self.is_used = True
        for v in values:
            try:
                values_t.append(self.arg_type(v))
            except ValueError as e:
                print(
                    "Error while parsing value `{}` for argument '{}'".format(
                        v, self.name))
                print(e)
                exit(1)

        if self.n_args == 1:
            self.value = values_t[0]
        else:
            self.value = values_t


def split_args(args):
    """Parse argument list and associate value to keyword."""
    arg_index = 0
    allow_positional = True
    pos_args = []
    kwargs = {}
    while arg_index < len(args):
        arg = args[arg_index]

        # positional argument
        if arg[0] != '-' and allow_positional:
            pos_args.append(arg)
            arg_index += 1
            continue

        # disable positional argument when the first non positional argument
        # is found
        allow_positional = False

        if arg[0] != '-':
            raise ValueError('Invalid argument `{}`'.format(arg[0]))

        if '=' in arg:
            # parse argument using '=' to assing value
            key, *value = arg.split('=')
            values = ['='.join(value)]
            arg_index += 1
        else:
            key = arg
            arg_index += 1
            values = []
            for arg in args[arg_index:]:
                # stop at the next keyword
                if arg[0] == '-':
                    break
                values.append(arg)
                arg_index += 1

        if key in kwargs:
            print('{} already used'.format(key))
            exit(1)

        kwargs[key] = values

    return pos_args, kwargs
