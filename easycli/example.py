import easycli

cli = easycli.Cli()


@cli.group('area')
@cli.command('triangle')
@cli.argument('base', 'b', arg_type=float)
@cli.argument('height', 'h', arg_type=float)
def calulate_traingle_area(base, height):
    print(base * height / 2)


@cli.group('area')
@cli.command('cube')
@cli.argument('height', 'h', arg_type=float, variable='a')
@cli.argument('width', 'w', arg_type=float, variable='b', default=1)
@cli.argument('depth', 'd', arg_type=float, variable='c', default=1)
def calulate_area_cube(a, b, c):
    """
    Calculate area of a cube

    Arguments
    ---------
    a: int
    b: int
    c: int
    """
    print(a * b * c)


@cli.command('sum-mul')
@cli.argument('num', arg_type=float, n_args='N')
@cli.argument('times', arg_type=float, n_args=1)
def calulate_sum_mul(num, times):
    print(sum(num) * times)


@cli.command('test')
@cli.argument('a', arg_type=str, choice=['a', 'b', 'c'], n_args='N')
def test(a):
    print(a)


cli.run()
