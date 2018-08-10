"""Climb CLI arguments."""


class Argument():
    """Argument class."""

    def __init__(self,
                 name,
                 short_name=None,
                 arg_type=str,
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

    def __eq__(self, arg):
        """Equality operator."""
        return arg.name == self.name or self.variable == arg.variable

    def set_value(self, value):
        """Set argument value.

        Parameters
        ----------
        value: str
            value read from sys.argv

        """
        try:
            self.value = self.arg_type(value)
            self.is_used = True
        except ValueError as e:
            print("Error while parsing value `{}` for argument '{}'".format(
                value, self.name))
            print(e)
            exit(1)
