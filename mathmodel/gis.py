from argparse import ArgumentParser, ArgumentTypeError
from json import loads
from pathlib import Path
from typing import Any, Dict, List, Iterable, Tuple, Optional
from plotly.graph_objs import Figure, Scatter
from numpy import array
from shapely.geometry import shape


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
        scatters, annotations = layer.render()
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


class Layer:
    """
    Сутність, що відповідає за малювання 1 шару ГІС. В якості полів класу містить
    перелік полів екземпляру й кореневу директорію репозиторію для коректного
    підвантаження даних із GeoJSON-файлів. Варто зазначити, що всі координати
    задано у WGS 84. Детальніше про GeoJSON: https://geojson.org/ .
    """
    __slots__ = [
        '_path',
        '_is_visible',
        '_is_filled',
        '_is_named',
        '_outer_fill_color',
        '_outer_line_color',
        '_outer_line_width',
        '_inner_fill_color',
        '_inner_line_color',
        '_inner_line_width'
    ]
    _root_dir = Path(__file__).parent.parent

    def __init__(
        self,
        name: str,
        is_visible: bool = True,
        is_filled: bool = True,
        is_named: bool = False,
        outer_fill_color: str = '#fff',
        outer_line_color: str = '#fff',
        outer_line_width: int = 0,
        inner_fill_color: str = '#fff',
        inner_line_color: str = '#fff',
        inner_line_width: int = 0
    ):
        """
        Конструктор класу. Ініціалізує поля для шляху файлу з координатами, кольорів
        заливки й стилів кордонів зовнішнього й внутрішніх кілець полігонів.
        """
        self._path = self._root_dir / f'layers/{name}.geojson'
        self._is_visible = is_visible
        self._is_filled = is_filled
        self._is_named = is_named
        self._outer_fill_color = outer_fill_color
        self._outer_line_color = outer_line_color
        self._outer_line_width = outer_line_width
        self._inner_fill_color = inner_fill_color
        self._inner_line_color = inner_line_color
        self._inner_line_width = inner_line_width

    def render(self) -> Tuple[List[Scatter], List[Dict[str, Any]]]:
        """
        "Лінивий" метод малювання об'єктів шару. Створює множину полігонів відповідно до
        координат кілець й додає текстові анотації над сутностями, наприклад, містами.
        """
        if not self._is_visible:
            return [], []
        with open(self._path) as stream:
            content = stream.read()
        features = loads(content)['features']
        return (
            [
                s
                for f in features
                for s in self._flatten(f['geometry'])
            ],
            []
            if not self._is_named
            else [a for a in map(self._annotate, features) if a]
        )

    def _flatten(self, geometry: Dict[str, Any]) -> Iterable[Scatter]:
        """
        Робить "розгортання" заданого геометричного об'єкта в залежності від вказаного
        типу. Polygon (багатокутник, що може містити порожнини всередині, як бублик) та
        MultiPolygon (колекція багатокутників) відповідають формам областей, міст й
        річок. Кожне замкнене кільце (матриця розмірності N+1 x 2, де N - кількість
        вершин у кільці) є самостійним графіком на загальному полотні. Таким самим
        обосібленим чартом є і довільний фрагмент дорожньої системи. В результаті,
        навіть у межах даних для лише 3 областей із суттєвим зниженням деталізації
        комп'ютеру стає складно перемальовувати карту при інтерактивній зміні - надто
        вже багато точок й окремих графіків включає в себе результуюче полотно. Основний
        удар по продуктивності наносять дороги - вони надто багаточисельні й погано
        піддаються точковому спрощенню.
        """
        if geometry['type'] == 'Polygon':
            return self._polygonize(geometry['coordinates'])
        if geometry['type'] == 'MultiPolygon':
            return (
                s
                for c in geometry['coordinates']
                for s in self._polygonize(c)
            )
        if geometry['type'] == 'LineString':
            coordinates = array(geometry['coordinates'])
            return [
                Scatter(
                    x=coordinates[:, 0],
                    y=coordinates[:, 1],
                    mode='lines',
                    hoverinfo='skip',
                    line={
                        'color': self._outer_line_color,
                        'width': self._outer_line_width
                    }
                )
            ]
        return []

    def _polygonize(
        self,
        coordinates: List[List[List[float]]]
    ) -> Iterable[Scatter]:
        """
        Даний метод здійснює "ліниву" полігонізацію заданого багатокутника, перетворюючи
        список матриць координат на графічні об'єкти. В основі лежить застосування
        специфічних об'єктів мови Python - генераторів. Якщо коротко, то це - функції,
        чиє виконання можна призупинити. Цінність таких об'єктів полягає в операціях над
        колекціями даних - застосування генераторів усуває надлишковість проміжних
        обчислень, бо результуючі списки рахуються лише в момент відкладеного виклику,
        не обтяжуючи CPU неостаточними розрахунками.
        """
        return (
            Scatter(
                x=r[:, 0],
                y=r[:, 1],
                mode='lines',
                fill='toself',
                hoverinfo='skip',
                fillcolor=(
                    self._outer_fill_color
                    if i == 0 and self._is_filled else
                    self._inner_fill_color
                ),
                line={
                    'color': (
                        self._outer_line_color
                        if i == 0 else
                        self._inner_line_color
                    ),
                    'width': (
                        self._outer_line_width
                        if i == 0 else
                        self._inner_line_width
                    )
                }
            )
            for i, r in enumerate(map(array, coordinates))
        )

    @staticmethod
    def _annotate(feature: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Даний метод обраховує позицію й стиль текстової анотації для геометричної
        фігури. Принцип обчислення дуже простий: довкола цільової геометрії будується
        уявна обмежувальна рамка, в якості Х-координати тексту береться середнє
        арифметичне західної і східної меж, в якості Y-координати - північна межа
        фрейму.
        """
        name = feature['properties'].get('name', '')
        if name == '':
            return None
        bounds = shape(feature['geometry']).bounds
        return {
            'text': name,
            'x': (bounds[0] + bounds[2]) / 2,
            'y': bounds[3],
            'showarrow': False,
            'arrowhead': 0,
            'ax': 0,
            'ay': 0,
            'font': {'size': 7}
        }


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
