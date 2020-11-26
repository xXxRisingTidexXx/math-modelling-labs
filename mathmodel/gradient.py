from numpy import meshgrid, sin, linspace
from plotly.subplots import make_subplots
from plotly.graph_objs import Surface, Scatter3d, Scatter


def main():
    x, y, z = [0], [0], [f(0, 0)]
    h, i = 0.1, 0
    while len(z) == 1 or abs(z[-2] - z[-1]) >= 0.0001:
        xi = x[-1] + (f(x[-1] + h, y[-1]) - z[-1]) / h
        yi = y[-1] + (f(x[-1], y[-1] + h) - z[-1]) / h
        x, y, z = x + [xi], y + [yi], z + [f(xi, yi)]
        if z[-2] >= z[-1]:
            h *= 0.5
        i += 1
    figure = make_subplots(
        cols=3,
        specs=[[{'type': 'xy'}, {'type': 'scene'}, {'type': 'scene'}]]
    )
    xg, yg = meshgrid(linspace(-2, 2, 100), linspace(-0.2, 1, 100))
    figure.add_trace(Scatter(x=x, y=y, name=''), row=1, col=1)
    figure.add_trace(Surface(x=xg, y=yg, z=f(xg, yg)), row=1, col=2)
    figure.add_trace(Scatter3d(x=x, y=y, z=z, name=''), row=1, col=2)
    xg, yg = meshgrid(linspace(-5, 5, 200), linspace(-5, 5, 200))
    figure.add_trace(Surface(x=xg, y=yg, z=f(xg, yg)), row=1, col=3)
    figure.add_trace(Scatter3d(x=x, y=y, z=z, name=''), row=1, col=3)
    figure.update_layout(
        title=f'x = {x[-1]:.4f}, y = {y[-1]:.4f}, z = {z[-1]:.4f}, h = {h}, i = {i}',
        showlegend=False
    )
    figure.show()


def f(x, y):
    return sin(x - 9) * sin(y - 5.4)


if __name__ == '__main__':
    main()
