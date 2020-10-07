from argparse import ArgumentParser
from typing import Tuple
from numpy import (
    sqrt, full, reshape, ndarray, hstack, vstack, amin, amax, array, repeat, tile
)
from plotly.graph_objs import Scatter, Scatter3d, Mesh3d, Figure
from cv2 import (
    imread, COLOR_BGR2GRAY, RETR_TREE, CHAIN_APPROX_SIMPLE, cvtColor, threshold,
    findContours
)
from shapely.geometry import Polygon, Point, LineString
from random import uniform
from scipy.spatial import Delaunay


def frame_plane_2d():
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
    figure = Figure()
    shape = contour()
    figure.add_trace(
        Scatter3d(
            x=shape[:, 0],
            y=shape[:, 1],
            z=full((len(shape),), 0),
            mode='lines',
            hoverinfo='skip',
            line={'color': 'red'}
        )
    )
    figure.show()


def frame_sphere():
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


def inflate(shape: ndarray) -> Tuple[ndarray, ndarray, ndarray]:
    r = 50
    x, y, z = shape[:, 0], shape[:, 1], full((shape.shape[0],), 20)
    k = r / sqrt(x ** 2 + y ** 2 + (z + r) ** 2)
    return x * k, y * k, z * k


def surface_sphere():
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
    return all(
        polygon.contains(ls) or polygon.exterior.contains(ls)
        for ls in
        (
            LineString([triangle[i], triangle[(i + 1) % len(triangle)]])
            for i in range(len(triangle))
        )
    )


def surface_cone():
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
    print(f'There\'s no graphs with such a name')


if __name__ == '__main__':
    parser = ArgumentParser(description='Interactive spatial graphs and illustrations')
    parser.add_argument('-g', default='frame-plane-2d', help='graph name')
    args = parser.parse_args()
    graphs = {
        'frame-plane-2d': frame_plane_2d,
        'frame-plane-3d': frame_plane_3d,
        'frame-sphere': frame_sphere,
        'surface-sphere': surface_sphere,
        'surface-cone': surface_cone,
        'surface-cylinder': surface_cylinder,
        'surface-cone-dual': surface_cone_dual
    }
    graphs.get(args.g, no_graph)()
