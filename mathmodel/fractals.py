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
                [paint(x, y) for x in linspace(3.4, -3.4, 1600)]
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
        margin={'t': 0, 'r': 0, 'b': 0, 'l': 0}
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
    figure.write_image('images/julia.png', width=1600, height=800)


def paint(x: float, y: float) -> float:
    """
    Функція обчислення "інтенсивності" точки. Ця величина необхідна, аби за шкалою
    [0, 1] мати змогу співставити числа в пікселях й кольори. При чому, х та у -
    координати зображення, що вже нормалізовані за шириною і висотою.
    """
    z = complex(x, y)
    n, stop = 0, 50
    while abs(z) <= 10 and n < stop:
        z = z ** 2 + 0.285 + 0.01j
        n += 1
    return n / stop


def burning_ship():
    """
    Функція обчислення й рендерингу "Корабля, що палає" - своєрідного фракталу Ресслера.
    Довідка: https://en.wikipedia.org/wiki/Burning_Ship_fractal . Принцип обрахунку
    інтенсивності точок такий самий, як і в попередньому фракталі.
    """
    figure = Figure()
    figure.add_trace(
        Heatmap(
            z=[
                [draw(x, y) for x in linspace(-2.9, 2.3, 1600)]
                for y in linspace(0.7, -1.9, 800)
            ],
            zmin=0,
            zmax=1,
            hoverinfo='skip',
            colorscale=[
                [0, 'rgb(103, 0, 31)'],
                [0.2, 'rgb(178, 24, 43)'],
                [0.4, 'rgb(214, 96, 77)'],
                [0.6, 'rgb(244, 165, 130)'],
                [0.8, 'rgb(77, 77, 77)'],
                [1, 'rgb(0, 0, 0)']
            ],
            showscale=False
        )
    )
    figure.update_layout(
        showlegend=False,
        margin={'t': 0, 'r': 0, 'b': 0, 'l': 0},
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
    figure.write_image('images/burning_ship.png', width=1600, height=800)


def draw(x: float, y: float) -> float:
    """
    Функція обчислення "інтенсивності" точки. Ця величина необхідна, аби за шкалою
    [0, 1] мати змогу співставити числа в пікселях й кольори. При чому, х та у -
    координати зображення, що вже нормалізовані за шириною і висотою.
    """
    z, c = 0, complex(x, y)
    n, stop = 0, 50
    while abs(z) <= 4 and n < stop:
        z = complex(abs(z.real), abs(z.imag)) ** 2 + c
        n += 1
    return n / stop


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
