from easycli.exceptions import InvalidCommandNameException


def validate_command_name(name):
    if len(name) == 0:
        InvalidCommandNameException(name)

    if name[0] == '-':
        InvalidCommandNameException(name)

    if '=' in name or ' ' in name:
        InvalidCommandNameException(name)
