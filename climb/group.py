from climb.exceptions import CommandNameConflictException
from climb.command import Command


class Group():
    def __init__(self, name=None, lv=0):
        self.name = name
        self.parse_tree = {}
        self.lv = lv
        self.commands = set()

    def add_command(self, cmd):
        self.commands.add(cmd)

    def build_parse_tree(self):
        for cmd in self.commands:
            # add command to tree
            if len(cmd.groups) == self.lv:
                # check if a group or cmd with same name exists
                if cmd.name in self.parse_tree:
                    raise CommandNameConflictException(cmd)

                self.parse_tree[cmd.name] = cmd
                continue

            # add group to tree
            if cmd.groups[self.lv] in self.parse_tree:
                # check if a group or cmd with same name exists
                if isinstance(self.parse_tree[cmd.groups[self.lv]], Command):
                    raise CommandNameConflictException(cmd)
            else:
                # create new group
                self.parse_tree[cmd.groups[self.lv]] = Group(
                    cmd.groups[self.lv], self.lv + 1)

            # add cmd to existsing group
            self.parse_tree[cmd.groups[self.lv]].add_command(cmd)

        # parse all subgroups
        for group in self.parse_tree.values():
            group.build_parse_tree()

    def run(self, args):
        if len(args) == 0:
            self.print_help()
            exit(1)

        if args[0] not in self.parse_tree:
            exit_code = 0
            if args[0] != '-h' and args[0] != '--help':
                print("Invalid argument '{}'".format(args[0]))
                exit_code = 1

            self.print_help()
            exit(exit_code)

        self.parse_tree[args[0]].run(args[1:])

    def print_help(self):
        if self.name is not None:
            print('    ' * (self.lv - 1) + self.name)
        for command in self.parse_tree.values():
            command.print_help()

    def print(self):
        print('\t' * (self.lv - 1) + (self.name or 'BaseGroup'))
        for g in self.parse_tree.values():
            g.print()
