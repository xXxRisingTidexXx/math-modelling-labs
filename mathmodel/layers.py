from json import loads
from pathlib import Path
from typing import Any, Dict, List, Iterable, Tuple, Optional, Union
from plotly.graph_objs import Scatter, Mesh3d, Scatter3d
from numpy import array, ndarray
from shapely.geometry import shape
from mathmodel.utils import inflate, mesh


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
        '_inner_line_width',
        '_dx',
        '_dy',
        '_r',
        '_z'
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
        inner_line_width: int = 0,
        dx: float = 36.8,
        dy: float = 48.1,
        r: float = 100,
        z: float = 1
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
        self._dx = dx
        self._dy = dy
        self._r = r
        self._z = z

    def render2d(self) -> Tuple[List[Scatter], List[Dict[str, Any]]]:
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
                for s in self._flatten2d(f['geometry'])
            ],
            []
            if not self._is_named
            else [a for a in map(self._annotate, features) if a]
        )

    def _flatten2d(self, geometry: Dict[str, Any]) -> Iterable[Scatter]:
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
            return self._polygon2d(geometry['coordinates'])
        if geometry['type'] == 'MultiPolygon':
            return (
                s
                for c in geometry['coordinates']
                for s in self._polygon2d(c)
            )
        if geometry['type'] == 'LineString':
            return [self._line2d(geometry['coordinates'])]
        return []

    def _polygon2d(self, coordinates: List[List[List[float]]]) -> Iterable[Scatter]:
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

    def _line2d(self, coordinates: List[List[float]]) -> Scatter:
        """
        TODO
        """
        points = array(coordinates)
        return Scatter(
            x=points[:, 0],
            y=points[:, 1],
            mode='lines',
            hoverinfo='skip',
            line={'color': self._outer_line_color, 'width': self._outer_line_width}
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

    def render3d(self) -> List[Union[Mesh3d, Scatter3d]]:
        """
        TODO
        """
        if not self._is_visible:
            return []
        with open(self._path) as stream:
            content = stream.read()
        features = loads(content)['features']
        return [
            s
            for f in features
            for s in self._flatten3d(f['geometry'])
        ]

    def _flatten3d(self, geometry: Dict[str, Any]) -> Iterable[Union[Mesh3d, Scatter3d]]:
        """
        TODO
        """
        if geometry['type'] == 'Polygon':
            return self._polygon3d(geometry['coordinates'][0])
        if geometry['type'] == 'MultiPolygon':
            return (
                s
                for c in geometry['coordinates']
                for s in self._polygon3d(c[0])
            )
        if geometry['type'] == 'LineString':
            return [self._line3d(self._array(geometry['coordinates']))]
        return []

    def _polygon3d(self, coordinates: List[List[float]]) -> Tuple[Mesh3d, Scatter3d]:
        """
        TODO
        """
        points = self._array(coordinates)
        x, y, z, i, j, k = mesh(points, r=self._r, z=self._z)
        return (
            Mesh3d(
                x=x,
                y=y,
                z=z,
                i=i,
                j=j,
                k=k,
                color=self._outer_fill_color,
                hoverinfo='skip'
            ),
            self._line3d(points)
        )

    def _array(self, coordinates: List[List[float]]) -> ndarray:
        """
        TODO
        """
        points = array(coordinates)
        points[:, 0] -= self._dx
        points[:, 1] -= self._dy
        return points

    def _line3d(self, points: ndarray) -> Scatter3d:
        """
        TODO
        """
        x, y, z = inflate(points, r=self._r, z=self._z)
        return Scatter3d(
            x=x,
            y=y,
            z=z,
            mode='lines',
            hoverinfo='skip',
            line={'color': self._outer_line_color, 'width': self._outer_line_width}
        )
