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
    """Calculate area of a cube 
    
    Arguments
    ---------
    a: int
    b: int
    c: int
    """
    print(a * b * c)


@cli.command('sum')
@cli.argument('a', argType=float)
@cli.argument('b', argType=float)
def calulate_sum(a, b):
    print(a + b)


cli.run()
