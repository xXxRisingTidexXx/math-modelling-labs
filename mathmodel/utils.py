from random import uniform
from typing import Tuple
from numpy import full, sqrt, ndarray, vstack, array
from scipy.spatial import Delaunay
from shapely.geometry import Polygon, Point, LineString


def inflate(
    shape: ndarray,
    r: float = 50,
    z: float = 20
) -> Tuple[ndarray, ndarray, ndarray]:
    """
    Логіка "набухання" отриманої 2D-фігури.
    """
    x, y, z = shape[:, 0], shape[:, 1], full((shape.shape[0],), z)
    k = r / sqrt(x ** 2 + y ** 2 + (z + r) ** 2)
    return x * k, y * k, z * k


def mesh(
    shape: ndarray,
    r: float = 50,
    z: float = 20
) -> Tuple[ndarray, ndarray, ndarray, ndarray, ndarray, ndarray]:
    """
    TODO
    """
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
    x, y, z = inflate(delaunay.points, r=r, z=z)
    ijk = array(
        [
            t for t in delaunay.simplices if _is_included(delaunay.points[t], polygon)  # noqa
        ]
    )
    return x, y, z, ijk[:, 0], ijk[:, 1], ijk[:, 2]


def _is_included(triangle: ndarray, polygon: Polygon) -> bool:
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
