from argparse import ArgumentParser
from typing import Callable, Any, Tuple
from numpy import ndarray, array, full
from plotly.subplots import make_subplots
from plotly.graph_objs import Scatter3d
from scipy.integrate import solve_ivp


def main(f: Callable[[Any, ndarray], ndarray]):
    """
    Ключова функція візуалізації вирішень ЗДУ. В якості методів присутні 3 вбудовані
    механізми - метод Рунге-Кутта порядку 3(2), порядку 5(4) і порядку 8 - й 1
    самописний спосіб через метод Ейлера.
    """
    spec = {'type': 'scene'}
    figure = make_subplots(
        2,
        2,
        specs=[[spec, spec], [spec, spec]],
        horizontal_spacing=0.02,
        vertical_spacing=0.02
    )
    span, y0 = (0, 150), array([0.0, 0.0, 1.0])
    rk23 = solve_ivp(f, span, y0, 'RK23')
    figure.add_trace(
        Scatter3d(
            name='RK23',
            x=rk23.y[0],  # noqa
            y=rk23.y[1],  # noqa
            z=rk23.y[2],  # noqa
            mode='lines',
            line={'color': 'red'}
        ),
        row=1,
        col=1
    )
    rk45 = solve_ivp(f, span, y0)
    figure.add_trace(
        Scatter3d(
            name='RK45',
            x=rk45.y[0],  # noqa
            y=rk45.y[1],  # noqa
            z=rk45.y[2],  # noqa
            mode='lines',
            line={'color': 'magenta'}
        ),
        row=1,
        col=2
    )
    dop853 = solve_ivp(f, span, y0, 'DOP853')
    figure.add_trace(
        Scatter3d(
            name='DOP853',
            x=dop853.y[0],  # noqa
            y=dop853.y[1],  # noqa
            z=dop853.y[2],  # noqa
            mode='lines',
            line={'color': 'purple'}
        ),
        row=2,
        col=1
    )
    euler = solve_ivp_euler(f, span, array([1.0, 1.0, 1.0]))
    figure.add_trace(
        Scatter3d(
            name='Euler',
            x=euler[0],
            y=euler[1],
            z=euler[2],
            mode='lines',
            line={'color': 'blue'}
        ),
        row=2,
        col=2
    )
    figure.update_layout(margin={'t': 30, 'r': 30, 'b': 30, 'l': 30})
    figure.show()


def solve_ivp_euler(
    f: Callable[[Any, ndarray], ndarray],
    span: Tuple[float, float],
    y0: ndarray,
    steps: int = 10000
) -> ndarray:
    """
    Рукописний варіант вирішення ЗДУ методом Ейлера.
    """
    y, dt = full((steps, len(y0)), y0), (span[1] - span[0]) / steps
    for i in range(1, steps):
        y[i] = y[i - 1] + dt * f(0, y[i - 1])
    return y.T


def rossler(_, y: ndarray) -> ndarray:
    """
    Функція правих частинь рівнянь атрактора Рьослера.
    """
    return array([-y[1] - y[2], y[0] + 0.2 * y[1], 0.2 + y[2] * (y[0] - 5.7)])


if __name__ == '__main__':
    # Перелік функцій - правих частин систем рівнянь динамічних систем.
    fs = {'rossler': rossler}
    parser = ArgumentParser(description='Colorful attractor visualizations')
    # Аргумент командного рядка для ідентифікації обраного графіка.
    parser.add_argument(
        '-f',
        default='rossler',
        help=f'dynamic system name (available ones: {", ".join(fs.keys())})'
    )
    args = parser.parse_args()
    if args.f not in fs:
        print('There\'re no functions with such a name')
    else:
        main(fs[args.f])
