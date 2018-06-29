class Argument():
    def __init__(self,
                 name,
                 shortName=None,
                 argType=str,
                 required=False,
                 variable=None,
                 default=None):

        assert (shortName is None or len(shortName) == 1)

        self.name = '--' + name if len(name) > 1 else '-' + name
        self.shortName = shortName if shortName is None else '-' + shortName
        self.argType = argType
        self.required = required
        self.variable = variable or name
        self.default = default
        self.value = None

    def __eq__(self, arg):
        return arg.name == self.name or self.variable == arg.variable

    def set_value(self, value):
        try:
            self.value = self.argType(value)
        except ValueError as e:
            print("Error while parsing value `{}` for argument '{}'".format(
                value, self.name))
            print(e)
            exit(1)
