from numpy import hstack, stack, sum, sqrt, full, reshape, append
from plotly.graph_objs import Scatter, Scatter3d
from plotly.subplots import make_subplots
from cv2 import (
    imread, COLOR_BGR2GRAY, RETR_TREE, CHAIN_APPROX_SIMPLE, cvtColor, threshold,
    findContours
)


def main():
    frame = max(
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
    frame = reshape(frame, (frame.shape[0], 2))
    frame = append(frame, frame[:1], axis=0)
    figure = make_subplots(
        rows=1,
        cols=3,
        specs=[[{'type': 'xy'}, {'type': 'scene'}, {'type': 'scene'}]]
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
        1,
        3
    )
    figure.update_layout(showlegend=False)
    figure.show()


if __name__ == '__main__':
    main()
