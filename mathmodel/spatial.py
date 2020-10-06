from argparse import ArgumentParser
from numpy import hstack, stack, sum, sqrt, full, reshape, append, ndarray
from plotly.graph_objs import Scatter, Scatter3d, Mesh3d, Figure
from cv2 import (
    imread, COLOR_BGR2GRAY, RETR_TREE, CHAIN_APPROX_SIMPLE, cvtColor, threshold,
    findContours
)


def main(graph: str):
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
    shape = append(shape, shape[:1], axis=0)
    if graph == 'framex':
        frame_2d(shape)
    else:
        print(f'There\'s no graphs with name \'{graph}\'')


def frame_2d(shape: ndarray):
    figure = make_subplots(
        rows=2,
        cols=2,
        specs=[
            [{'type': 'xy'}, {'type': 'scene'}],
            [{'type': 'scene'}, {'type': 'scene'}]
        ]
    )
    figure.append_trace(
        Scatter(
            x=frame[:, 0],
            y=frame[:, 1],
            mode='lines',
            hoverinfo='skip',
            line={'color': 'red'}
        ),
        1,
        1
    )
    z = 5
    frame3d = hstack((frame, full((frame.shape[0], 1), z)))
    figure.append_trace(
        Scatter3d(
            x=frame3d[:, 0],
            y=frame3d[:, 1],
            z=frame3d[:, 2],
            mode='lines',
            hoverinfo='skip',
            line={'color': 'red'}
        ),
        1,
        2
    )
    r = 50
    k = r / sqrt(sum(hstack((frame, full((frame.shape[0], 1), z + r))) ** 2, axis=1))
    frame_sphere = frame3d * stack((k, k, k), axis=1)
    figure.append_trace(
        Scatter3d(
            x=frame_sphere[:, 0],
            y=frame_sphere[:, 1],
            z=frame_sphere[:, 2],
            mode='lines',
            hoverinfo='skip',
            line={'color': 'red'}
        ),
        2,
        1
    )
    figure.append_trace(
        Mesh3d(
            x=frame_sphere[:, 0],
            y=frame_sphere[:, 1],
            z=frame_sphere[:, 2],
            alphahull=1
        ),
        2,
        2
    )
    figure.update_layout(showlegend=False)
    figure.show()


if __name__ == '__main__':
    parser = ArgumentParser(description='Renders interactive spatial graphs')
    parser.add_argument('-g', default='frame-2d', help='graph name')
    args = parser.parse_args()
    main(args.g)
