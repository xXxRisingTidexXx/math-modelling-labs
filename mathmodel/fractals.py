from argparse import ArgumentParser
from typing import List, Union
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
    build(
        [
            [paint(x, y) for x in linspace(3.4, -3.4, 1600)]
            for y in linspace(1.7, -1.7, 800)
        ],
        'inferno',
        'images/julia.png'
    )


def build(
    z: List[List[float]],
    scale: Union[str, List[List[Union[float, str]]]],
    path: str
):
    """
    Тут будується графік, після чого зображення зберігається у файл.
    """
    figure = Figure()
    figure.add_trace(Heatmap(z=z, zmin=0, zmax=1, colorscale=scale, showscale=False))
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
    figure.write_image(path, width=1600, height=800)


def paint(x: float, y: float) -> float:
    """
    Функція обчислення "інтенсивності" точки. Ця величина необхідна, аби за шкалою
    [0, 1] мати змогу співставити числа в пікселях й кольори. При чому, х та у -
    координати зображення, що вже нормалізовані за шириною і висотою.
    """
    z, n, stop = x + y * 1j, 0, 50
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
    build(
        [
            [draw(x, y) for x in linspace(-2.9, 2.3, 1600)]
            for y in linspace(0.7, -1.9, 800)
        ],
        [
            [0, 'rgb(103, 0, 31)'],
            [0.2, 'rgb(178, 24, 43)'],
            [0.4, 'rgb(214, 96, 77)'],
            [0.6, 'rgb(244, 165, 130)'],
            [0.8, 'rgb(77, 77, 77)'],
            [1, 'rgb(0, 0, 0)']
        ],
        'images/burning_ship.png'
    )


def draw(x: float, y: float) -> float:
    """
    Функція обчислення "інтенсивності" точки. Ця величина необхідна, аби за шкалою
    [0, 1] мати змогу співставити числа в пікселях й кольори. При чому, х та у -
    координати зображення, що вже нормалізовані за шириною і висотою.
    """
    z, n, stop = 0, 0, 50
    while abs(z) <= 4 and n < stop:
        z = complex(abs(z.real), abs(z.imag)) ** 2 + x + y * 1j
        n += 1
    return n / stop


def mandelbrot():
    """
    Алгоритм побудови множини Мандельброта за описаними вище ітеративними принципами.
    Детальніше: https://en.wikipedia.org/wiki/Mandelbrot_set .
    """
    build(
        [
            [render(x, y) for x in linspace(-2.9, 2.1, 1600)]
            for y in linspace(1.25, -1.25, 800)
        ],
        [
            [0, 'rgb(77, 0, 75)'],
            [0.2, 'rgb(129, 15, 124)'],
            [0.4, 'rgb(136, 65, 157)'],
            [0.6, 'rgb(140, 107, 177)'],
            [0.8, 'rgb(77, 77, 77)'],
            [1, 'rgb(0, 0, 0)']
        ],
        'images/mandelbrot.png'
    )


def render(x: float, y: float) -> float:
    """
    Обчислює інтенсивність кольору в точці.
    """
    z, n, stop = 0, 0, 50
    while abs(z) <= 2 and n < stop:
        z = z ** 2 + x + y * 1j
        n += 1
    return n / stop


if __name__ == '__main__':
    fractals = {'julia': julia, 'burning-ship': burning_ship, 'mandelbrot': mandelbrot}
    parser = ArgumentParser(description='Beautiful discrete fractal visualizations')
    # Аргумент командного рядка для ідентифікації обраного фрактала.
    parser.add_argument(
        '-f',
        default='julia',
        help=f'figure name (available ones: {", ".join(fractals.keys())})'
    )
    args = parser.parse_args()
    if args.f not in fractals:
        print('There\'re no functions with such a name')
    else:
        fractals[args.f]()
