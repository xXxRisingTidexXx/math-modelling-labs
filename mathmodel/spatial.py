from argparse import ArgumentParser
from numpy import (
    full, reshape, ndarray, hstack, vstack, amin, amax, array, repeat, tile, zeros
)
from plotly.graph_objs import Scatter, Scatter3d, Mesh3d, Figure
from cv2 import (
    imread, COLOR_BGR2GRAY, RETR_TREE, CHAIN_APPROX_SIMPLE, cvtColor, threshold,
    findContours
)
from shapely.geometry import Polygon, Point, LineString
from random import uniform
from scipy.spatial import Delaunay

from mathmodel.utils import inflate


def frame_plane_2d():
    """
    Примітивний графік 2D-фігури.
    """
    figure = Figure()
    shape = contour()
    figure.add_trace(
        Scatter(
            x=shape[:, 0],
            y=shape[:, 1],
            mode='lines',
            hoverinfo='skip',
            line={'color': 'red'}
        )
    )
    figure.update_yaxes(scaleanchor='x', scaleratio=1)
    figure.show()


def contour(is_closed=True) -> ndarray:
    """
    Функція читання контуру необхідного зображення з картинки, аналог ginput в Matlab.
    Бібліотечні алгоритми "комп'ютерного зору" переводять картинку в чорно-білу шкалу й
    відокремлюють найбільший із контурів, який відповідає зовнішньому кільцю. При
    потребі масив 2D-точок можна закільцювати, це необхідно лінійним графікам.
    """
    shape = max(
        findContours(
            threshold(
                cvtColor(imread('images/shape.png'), COLOR_BGR2GRAY),
                200,
                255,
                0
            )[1],
            RETR_TREE,
            CHAIN_APPROX_SIMPLE
        )[0],
        key=len
    )
    shape = reshape(shape, (shape.shape[0], 2))
    return vstack((shape, shape[:1])) if is_closed else shape


def frame_plane_3d():
    """
    Функція побудови 3D-рамки контуру. Тепер вже додається z-координата.
    """
    figure = Figure()
    shape = contour()
    figure.add_trace(
        Scatter3d(
            x=shape[:, 0],
            y=shape[:, 1],
            z=zeros((len(shape),)),
            mode='lines',
            hoverinfo='skip',
            line={'color': 'red'}
        )
    )
    figure.show()


def frame_sphere():
    """
    Графік, що проектує зчитану фігуру на сферу. Основна логіка перетворення прописана у
    функції нижче, тут присутня лише візуалізація.
    """
    figure = Figure()
    x, y, z = inflate(contour())
    figure.add_trace(
        Scatter3d(
            x=x,
            y=y,
            z=z,
            mode='lines',
            hoverinfo='skip',
            line={'color': 'red'}
        )
    )
    figure.show()


def surface_sphere():
    """
    З потребою зображення поверхонь малювання ускладнюється. Тепер необхідно
    використовувати можливості об'єкта mesh графічної бібліотеки. По суті, це сховище
    двох матриць - таблиці 3D-точок й преліку трикутників. Кожен трикутник - це реляція,
    котра містить неповторювані індекси трьох довільних точок із попереднього переліку.
    Задача малювання на сфері ускладнена й тим, що для набухання необхідно рівномірно-
    випадковим чином наповнити простір усередині базового полігона, аби в результаті
    побачити опуклу поверхню. У візуалізації також використовується триангуляція Делоне
    (https://en.wikipedia.org/wiki/Delaunay_triangulation) для розбиття полігона й
    внутрішніх опорних точок на мінімальні трикутники без взаємних накладнь.
    Ускладнюється обчислення й тим, що після обрахунку теселяції необхідно відкинути ті
    трикутники, чиє хоча б одне ребро лежить за межами початкового (швидше за все,
    неопуклого) багатокутника. А вже результуючі точки мають бути "надутими", аби
    сформувати каркас фрагменту поверхні сфери. Якщо точок буде достатньо багато,
    кутуватість обгортки буде згладженою і непомітною.
    """
    figure = Figure()
    shape = contour()
    polygon = Polygon(shape)
    min_x, min_y, max_x, max_y = polygon.bounds
    delaunay = Delaunay(
        vstack(
            (
                shape,
                [
                    [p.x, p.y]
                    for p in
                    (
                        Point(uniform(min_x, max_x), uniform(min_y, max_y))
                        for _ in range(1000)
                    )
                    if p.within(polygon)
                ]
            )
        )
    )
    x, y, z = inflate(delaunay.points)
    ijk = array(
        [
            t for t in delaunay.simplices if is_included(delaunay.points[t], polygon)  # noqa
        ]
    )
    figure.add_trace(
        Mesh3d(
            x=x,
            y=y,
            z=z,
            i=ijk[:, 0],
            j=ijk[:, 1],
            k=ijk[:, 2],
            opacity=0.4,
            color='red',
            hoverinfo='skip'
        )
    )
    figure.show()


def is_included(triangle: ndarray, polygon: Polygon) -> bool:
    """
    Ця невеличка утилітна функція необхідна для визначення того, чиварто включати даний
    трикутник у базовий полігон і результуючу теселяцію.
    """
    return all(
        polygon.contains(ls) or polygon.exterior.contains(ls)
        for ls in
        (
            LineString([triangle[i], triangle[(i + 1) % len(triangle)]])
            for i in range(len(triangle))
        )
    )


def surface_cone():
    """
    Візуалізація конуса, в основі якого лежить базовий 2D-полігон. Цікавим є принцип
    формування граней меша - це послідовні вершини основоположної фігури, чиї перші
    дві координати належать площині основи, а третя - усезагальна вершина конуса.
    """
    figure = Figure()
    shape = contour(False)
    x, y = shape[:, 0], shape[:, 1]
    ijk = array([[i, (i + 1) % len(shape), len(shape)] for i in range(len(shape))])
    figure.add_trace(
        Mesh3d(
            x=hstack((x, [(amin(x) + amax(x)) / 2])),
            y=hstack((y, [(amin(y) + amax(y)) / 2])),
            z=hstack((full((len(shape),), 0), [30])),
            i=ijk[:, 0],
            j=ijk[:, 1],
            k=ijk[:, 2],
            opacity=0.4,
            color='red',
            hoverinfo='skip'
        )
    )
    figure.show()


def surface_cylinder():
    """
    Аналогічна попередній візуалізація тривимірного циліндра. Кожна вертикальна грань
    меша - два суміжних прямокутних трикутника. Ми просто подвоюємо 3D-точки в порядку
    "нижня точка ребра - верхня точка" й нехитрим послідовним ходом встановлюємо
    відношення вершин трикутників.
    """
    figure = Figure()
    shape = repeat(contour(False), 2, 0)
    ijk = array(
        [[i, (i + 1) % len(shape), (i + 2) % len(shape)] for i in range(len(shape))]
    )
    figure.add_trace(
        Mesh3d(
            x=shape[:, 0],
            y=shape[:, 1],
            z=tile([0, 10], len(shape) // 2),
            i=ijk[:, 0],
            j=ijk[:, 1],
            k=ijk[:, 2],
            color='red',
            opacity=0.4,
            hoverinfo='skip'
        )
    )
    figure.show()


def surface_cone_dual():
    """
    Подвоєний / відображений 3D-конус. Майже нічого нового відносно одиничного піка,
    лише подвоєні й перевернуті координати кілець основ.
    """
    figure = Figure()
    shape = contour(False)
    x, y = shape[:, 0], shape[:, 1]
    ijk = array(
        [
            [j + i * len(shape), (j + 1) % len(shape) + i * len(shape), 2 * len(shape)]
            for i in range(2) for j in range(len(shape))
        ]
    )
    figure.add_trace(
        Mesh3d(
            x=hstack((x, x, [(amin(x) + amax(x)) / 2])),
            y=hstack((y, y, [(amin(y) + amax(y)) / 2])),
            z=hstack((full((len(shape),), 30), full((len(shape),), -30), [0])),
            i=ijk[:, 0],
            j=ijk[:, 1],
            k=ijk[:, 2],
            opacity=0.4,
            color='red',
            hoverinfo='skip'
        )
    )
    figure.show()


def no_graph():
    """
    "Порожній граф", чиє повідомлення виводиться на stdout.
    """
    print(f'There\'s no graphs with such a name')


if __name__ == '__main__':
    # Фігури до відображення проіндексовані за іменами.
    graphs = {
        'frame-plane-2d': frame_plane_2d,
        'frame-plane-3d': frame_plane_3d,
        'frame-sphere': frame_sphere,
        'surface-sphere': surface_sphere,
        'surface-cone': surface_cone,
        'surface-cylinder': surface_cylinder,
        'surface-cone-dual': surface_cone_dual
    }
    parser = ArgumentParser(description='Interactive spatial graphs and illustrations')
    # Аргумент командного рядка для ідентифікації обраного графіка.
    parser.add_argument(
        '-g',
        default='frame-plane-2d',
        help=f'graph name (available ones: {", ".join(graphs.keys())})'
    )
    args = parser.parse_args()
    graphs.get(args.g, no_graph)()
