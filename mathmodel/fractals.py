from plotly.graph_objects import Figure, Heatmap


def main():
    """
    Основна функція обчислення й побудови фрактала. Вся задача зводиться до того, що
    обирається растр певної розмірності, чиї пікселі й виступають дискретними точками,
    які належать чи не належать множині Жюліа. В результаті обчислюється ймовірність
    віднощення піксела до фракталу, де 0 - повна екзальтація, а 1 - цілковите занурення.
    В якості базового чарту використовується теплова карта, адже саме вона надає зручний
    інтерфейс для заповнення квадратних комірок.
    """
    figure = Figure()
    width, height = 1000, 500
    figure.add_trace(
        Heatmap(
            z=[
                [paint(j / width, i / height) for j in range(width)]
                for i in range(height)
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
        plot_bgcolor='black',
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


def paint(x: float, y: float, stop: int = 100) -> float:
    """
    Функція обчислення "інтенсивності" точки. Ця величина необхідна, аби за шкалою
    [0, 1] мати змогу співставити числа в пікселях й кольори. При чому, х та у -
    координати зображення, що вже нормалізовані за шириною і висотою.
    """
    z = complex(x * 3 - 1.5, y * 3 - 1.5)
    n = 0
    while abs(z) <= 10 and n < stop:
        z = z ** 2 - 0.7269 + 0.1889j
        n += 1
    return n / stop


if __name__ == '__main__':
    main()
