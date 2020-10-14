from argparse import ArgumentParser, ArgumentTypeError
from plotly.graph_objs import Figure
from mathmodel.layers import Layer


def str2bool(value):
    """
    Функція-конвертер аргументу консолі з рядкової в логічну величину.
    """
    if isinstance(value, bool):
        return value
    if value.lower() in {'yes', 'true', 't', 'y', '1'}:
        return True
    elif value.lower() in {'no', 'false', 'f', 'n', '0'}:
        return False
    else:
        raise ArgumentTypeError('Boolean value expected.')


def main(is_oblasts_filled: bool, is_roads_visible: bool):
    """
    Головна функція програми, яка виконує малювання (рендеринг) карти. Вона
    почергово створює усі необхідні рівні в порядку накладання - області,
    міста, річки й дороги. Після цього кожен рівень розміщує на загальному
    "полотні" дані з файлів й текстові анотації (для міст). В кінці полотно
    масштабується за віссю Y, аби результуюча картинка не була розтягнена.
    Варто зазначити, що бібліотека для малювання дозволяє інтерактивно
    взаємодіяти з отриманою картою, але в дуже мінімальних межах -
    переважно через те, що карта відмальовує надто велику кількість
    багатокутників і точок. Дана бібліотека не призначена для малювання ГІС,
    для цього куди краще підійдуть спеціалізовані графічні двигуни й дані в
    більш специфічному форматі - наприклад, shapefile або KML, але це
    виходить за межі даної лабораторної.
    """
    layers = [
        Layer(
            'oblasts',
            is_filled=is_oblasts_filled,
            outer_fill_color='#ebf2e7',
            outer_line_color='#b46198',
            outer_line_width=2
        ),
        Layer(
            'cities',
            is_named=True,
            outer_fill_color='#a1a0a0',
            outer_line_color='#656464',
            outer_line_width=1,
            inner_fill_color='#ebf2e7',
            inner_line_color='#ebf2e7'
        ),
        Layer(
            'rivers',
            outer_fill_color='#9fcee5',
            outer_line_color='#2a5eea',
            outer_line_width=1,
            inner_fill_color='#ebf2e7',
            inner_line_color='#2a5eea',
            inner_line_width=1
        ),
        Layer(
            'roads',
            is_visible=is_roads_visible,
            outer_line_color='#ffb732',
            outer_line_width=2
        )
    ]
    figure = Figure()
    for layer in layers:
        scatters, annotations = layer.render2d()
        figure.add_traces(scatters)
        for annotation in annotations:
            figure.add_annotation(**annotation)
    figure.update_layout(plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
    figure.update_xaxes(
        showline=True,
        linewidth=2,
        linecolor='#8b8b8b',
        mirror=True
    )
    figure.update_yaxes(
        scaleanchor='x',
        scaleratio=1.5,
        showline=True,
        linewidth=2,
        linecolor='#8b8b8b',
        mirror=True
    )
    figure.show()


if __name__ == '__main__':
    # Для керування рендерингом використовуються CLI-опції.
    parser = ArgumentParser(
        description='Renders interactive GIS of Dnipropetrovska oblast\''
    )
    # Цей прапор вимикає заповнення областей кольором.
    parser.add_argument(
        '-o',
        type=str2bool,
        default=False,
        help='disable oblast filling',
        nargs='?',
        const=True
    )
    # А цей приховує дороги, аби прискорити малювання.
    parser.add_argument(
        '-r',
        type=str2bool,
        default=False,
        help='disable road rendering',
        nargs='?',
        const=True
    )
    args = parser.parse_args()
    main(not args.o, not args.r)
