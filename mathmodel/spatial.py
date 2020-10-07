from argparse import ArgumentParser
from numpy import sqrt, full, reshape, append, ndarray, hstack, vstack
from plotly.graph_objs import Scatter, Scatter3d, Mesh3d, Figure
from cv2 import (
    imread, COLOR_BGR2GRAY, RETR_TREE, CHAIN_APPROX_SIMPLE, cvtColor, threshold,
    findContours
)
from shapely.geometry import Polygon, Point
from random import uniform


def frame_plane_2d(shape: ndarray):
    figure = Figure()
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


def frame_plane_3d(shape: ndarray):
    figure = Figure()
    figure.add_trace(
        Scatter3d(
            x=shape[:, 0],
            y=shape[:, 1],
            z=full((shape.shape[0],), 20),
            mode='lines',
            hoverinfo='skip',
            line={'color': 'red'}
        )
    )
    figure.show()


def frame_sphere(shape: ndarray):
    figure = Figure()
    points = inflate(shape)
    figure.add_trace(
        Scatter3d(
            x=points[:, 0],
            y=points[:, 1],
            z=points[:, 2],
            mode='lines',
            hoverinfo='skip',
            line={'color': 'red'}
        )
    )
    figure.show()


def inflate(shape: ndarray) -> ndarray:
    r = 50
    x, y, z = shape[:, 0], shape[:, 1], full((shape.shape[0],), 20)
    k = r / sqrt(x ** 2 + y ** 2 + (z + r) ** 2)
    dimensions = (-1, 1)
    return hstack(
        (
            reshape(x * k, dimensions),
            reshape(y * k, dimensions),
            reshape(z * k, dimensions)
        )
    )


def surface_sphere(shape: ndarray):
    figure = Figure()
    polygon = Polygon(shape)
    min_x, min_y, max_x, max_y = polygon.bounds
    points = inflate(
        vstack(
            (
                shape,
                [
                    [p.x, p.y]
                    for p in (
                        Point(uniform(min_x, max_x), uniform(min_y, max_y))
                        for _ in range(1000)
                    )
                    if p.within(polygon)
                ]
            )
        )
    )
    figure.add_trace(
        Mesh3d(
            x=points[:, 0],
            y=points[:, 1],
            z=points[:, 2],
            alphahull=-1,
            opacity=0.4,
            color='red',
            hoverinfo='skip'
        )
    )
    figure.show()


def no_graph(_: ndarray):
    print(f'There\'s no graphs with such a name')


if __name__ == '__main__':
    parser = ArgumentParser(description='Renders interactive spatial graphs')
    parser.add_argument('-g', default='frame-plane-2d', help='graph name')
    args = parser.parse_args()
    graphs = {
        'frame-plane-2d': frame_plane_2d,
        'frame-plane-3d': frame_plane_3d,
        'frame-sphere': frame_sphere,
        'surface-sphere': surface_sphere
    }
    contour = max(
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
    contour = reshape(contour, (contour.shape[0], 2))
    graphs.get(args.g, no_graph)(append(contour, contour[:1], axis=0))
