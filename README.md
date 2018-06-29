# Climb

## What is Climb

Climb is a Python package for creating powerfull CLI. Climb is inspired by command line tools like Git and Kubectl where commands are groupped together.

## Installation

Install and update using pip

    pip install git+https://github.com/WellDone2094/climb.git

## Example

This is all you need to know to write a simple CLI using Climb

```
import climb

cli = climb.Cli()


@cli.group('area')
@cli.command('triangle')
@cli.argument('base', 'b', argType=float)
@cli.argument('height', 'h', argType=float)
def calulate_traingle_area(base, height):
    print(base * height / 2)


@cli.group('area')
@cli.command('cube')
@cli.argument('height', 'h', argType=float, variable='a')
@cli.argument('width', 'w', argType=float, variable='b', default=1)
@cli.argument('depth', 'd', argType=float, variable='c', default=1)
def calulate_area_cube(a, b, c):
    print(a * b * c)


@cli.command('sum')
@cli.argument('a', argType=float)
@cli.argument('b', argType=float)
def calulate_sum(a, b):
    print(a + b)


cli.run()
```

And the result

```
$ python example.py area triangle --base 6 -h 4
12.0

$ python example.py area cube -h=1 -d=2 -w=3
6.0

$ python example.py area cube 4 --depth=10
40.0

$ python example.py sum 5 6
11.0

$ python example.py
area
    triangle --base=<float> --height=<float>
    cube --height=<float> [--width]=<float> [--depth]=<float>

sum -a=<float> -b=<float>
```

## Future feature

- boolean flag such as --debug and --no-debug
- more advance argument type such as path, range and list
- argument inference using mypi type notation
- improved man page
