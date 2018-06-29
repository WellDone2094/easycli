"""Climb CLI arguments."""


class Argument():
    """Argument class."""

    def __init__(self,
                 name,
                 shortName=None,
                 argType=str,
                 required=None,
                 variable=None,
                 default=None):
        """Constructor.

        Parameters
        ----------
        name: str
            Argument name without '--'.
        shortName: str
            Single character argument, default None.
        argType: type
            Argument type, default str.
        required: bool
            If True the argument is required.
        variable: str
            Name of the argument inside the function, if None `name` will be
            used. Default None.
        default: any
            Default value to use if argument is not required. Default None

        """
        assert (shortName is None or len(shortName) == 1)

        self.name = '--' + name if len(name) > 1 else '-' + name
        self.shortName = shortName if shortName is None else '-' + shortName
        self.argType = argType
        self.variable = variable or name
        self.default = default
        self.required = required or self.default is None
        self.value = None

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
            self.value = self.argType(value)
        except ValueError as e:
            print("Error while parsing value `{}` for argument '{}'".format(
                value, self.name))
            print(e)
            exit(1)
