from numpy import ndarray, array
from plotly.graph_objs import Figure, Scatter3d
from scipy.integrate import solve_ivp


def main():
    figure = Figure()
    solution = solve_ivp(lambda t, y: rossler(y), [0, 150], [0, 0, 1])
    figure.add_trace(
        Scatter3d(x=solution.y[0], y=solution.y[1], z=solution.y[2], mode='lines')  # noqa
    )
    figure.show('chrome')


def rossler(y: ndarray) -> ndarray:
    return array([-y[1] - y[2], y[0] + 0.2 * y[1], 0.2 + y[2] * (y[0] - 5.7)])


if __name__ == '__main__':
    main()
