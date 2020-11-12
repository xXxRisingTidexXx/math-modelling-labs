from argparse import ArgumentParser
from plotly.graph_objects import Figure, Heatmap
from numpy import linspace


def julia():
    """
    Основна функція обчислення й побудови фрактала. Вся задача зводиться до того, що
    обирається растр певної розмірності, чиї пікселі й виступають дискретними точками,
    які належать чи не належать множині Жюліа. В результаті обчислюється ймовірність
    віднощення піксела до фракталу, де 0 - повна екзальтація, а 1 - цілковите занурення.
    В якості базового чарту використовується теплова карта, адже саме вона надає зручний
    інтерфейс для заповнення комірок (https://en.wikipedia.org/wiki/Julia_set).
    """
    figure = Figure()
    figure.add_trace(
        Heatmap(
            z=[
                [paint(x, y) for x in linspace(-3.4, 3.4, 1600)]
                for y in linspace(1.7, -1.7, 800)
            ],
            zmin=0,
            zmax=1,
            hoverinfo='skip',
            colorscale='inferno',
            showscale=False
        )
    )
    figure.update_layout(
        showlegend=False,
        plot_bgcolor='white',
        margin={'t': 30, 'r': 20, 'b': 30, 'l': 20}
    )
    figure.update_xaxes(
        showticklabels=False,
        showgrid=False,
        showline=False,
        zeroline=False
    )
    figure.update_yaxes(
        scaleanchor='x',
        scaleratio=1,
        showticklabels=False,
        showgrid=False,
        showline=False,
        zeroline=False
    )
    figure.show()


def paint(x: float, y: float) -> float:
    """
    Функція обчислення "інтенсивності" точки. Ця величина необхідна, аби за шкалою
    [0, 1] мати змогу співставити числа в пікселях й кольори. При чому, х та у -
    координати зображення, що вже нормалізовані за шириною і висотою.
    """
    z = complex(x, y)
    n, stop = 0, 50
    while abs(z) <= 10 and n < stop:
        z = z ** 2 - 0.8j
        n += 1
    return n / stop


def burning_ship():
    """
    TODO
    https://en.wikipedia.org/wiki/Lyapunov_fractal
    """
    figure = Figure()
    figure.add_trace(
        Heatmap(
            z=[
                [draw(x, y) for x in linspace(-2.2, 1.8, 1600)]
                for y in linspace(1, -1, 800)
            ],
            zmin=0,
            zmax=1,
            hoverinfo='skip',
            colorscale='hot',
            showscale=False
        )
    )
    figure.update_layout(
        showlegend=False,
        margin={'t': 30, 'r': 20, 'b': 30, 'l': 20},
        plot_bgcolor='white'
    )
    figure.update_xaxes(
        showticklabels=False,
        showgrid=False,
        showline=False,
        zeroline=False
    )
    figure.update_yaxes(
        scaleanchor='x',
        scaleratio=1,
        showticklabels=False,
        showgrid=False,
        showline=False,
        zeroline=False
    )
    figure.show()


def draw(x: float, y: float) -> float:
    """
    TODO
    """
    z, c = 0, complex(x, y)
    n, stop = 0, 50
    while abs(z) <= 4 and n < stop:
        z = complex(abs(z.real), abs(z.imag)) ** 2 + c
        n += 1
    return 1 - n / stop


if __name__ == '__main__':
    fs = {'julia': julia, 'burning-ship': burning_ship}
    parser = ArgumentParser(description='Beautiful discrete fractal visualizations')
    # Аргумент командного рядка для ідентифікації обраного фрактала.
    parser.add_argument(
        '-f',
        default='julia',
        help=f'figure name (available ones: {", ".join(fs.keys())})'
    )
    args = parser.parse_args()
    if args.f not in fs:
        print('There\'re no functions with such a name')
    else:
        fs[args.f]()
