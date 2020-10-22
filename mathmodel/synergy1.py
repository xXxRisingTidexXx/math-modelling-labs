from typing import Callable, Any, Tuple
from numpy import ndarray, array, full
from plotly.subplots import make_subplots
from plotly.graph_objs import Scatter3d
from scipy.integrate import solve_ivp


def main():
    """
    TODO
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
    rk23 = solve_ivp(rossler, span, y0, 'RK23')
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
    rk45 = solve_ivp(rossler, span, y0)
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
    dop853 = solve_ivp(rossler, span, y0, 'DOP853')
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
    euler = solve_ivp_euler(rossler, span, array([1.0, 1.0, 1.0]))
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


def rossler(_, y: ndarray) -> ndarray:
    """
    TODO
    """
    return array([-y[1] - y[2], y[0] + 0.2 * y[1], 0.2 + y[2] * (y[0] - 5.7)])


def solve_ivp_euler(
    f: Callable[[Any, ndarray], ndarray],
    span: Tuple[float, float],
    y0: ndarray,
    steps: int = 10000
) -> ndarray:
    """
    TODO
    """
    y, dt = full((steps, len(y0)), y0), (span[1] - span[0]) / steps
    for i in range(1, steps):
        y[i] = y[i - 1] + dt * f(0, y[i - 1])
    return y.T


if __name__ == '__main__':
    main()
