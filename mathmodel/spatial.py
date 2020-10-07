from argparse import ArgumentParser
from numpy import sqrt, full, reshape, ndarray, hstack, vstack
from plotly.graph_objs import Scatter, Scatter3d, Mesh3d, Figure
from cv2 import (
    imread, COLOR_BGR2GRAY, RETR_TREE, CHAIN_APPROX_SIMPLE, cvtColor, threshold,
    findContours
)
from shapely.geometry import Polygon, Point
from random import uniform


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
            z=full((shape.shape[0],), 20),
            mode='lines',
            hoverinfo='skip',
            line={'color': 'red'}
        )
    )
    figure.show()


def frame_sphere():
    figure = Figure()
    shape = inflate(contour())
    figure.add_trace(
        Scatter3d(
            x=shape[:, 0],
            y=shape[:, 1],
            z=shape[:, 2],
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


def surface_sphere():
    figure = Figure()
    shape = contour()
    polygon = Polygon(shape)
    min_x, min_y, max_x, max_y = polygon.bounds
    shape = inflate(
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
            x=shape[:, 0],
            y=shape[:, 1],
            z=shape[:, 2],
            alphahull=-1,
            opacity=0.4,
            color='red',
            hoverinfo='skip'
        )
    )
    figure.show()


def surface_cone():
    figure = Figure()

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
        'surface-cone': no_graph,
        'surface-cylinder': no_graph,
        'surface-cone-dual': no_graph
    }
    graphs.get(args.g, no_graph)()
