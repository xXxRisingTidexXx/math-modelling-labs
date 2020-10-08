from cv2 import (
    CHAIN_APPROX_SIMPLE, RETR_TREE, COLOR_BGR2GRAY, imread, cvtColor, threshold,
    findContours
)
from numpy import reshape, vstack
from plotly.graph_objs import Figure, Scatter3d
from mathmodel.utils import inflate


def main():
    figure = Figure()
    shape = max(
        findContours(
            threshold(
                cvtColor(imread('images/oblast.jpg'), COLOR_BGR2GRAY),
                127,
                255,
                0
            )[1],
            RETR_TREE,
            CHAIN_APPROX_SIMPLE
        )[0],
        key=len
    )
    shape = reshape(shape, (shape.shape[0], 2))
    shape = vstack((shape, shape[:1]))
    x, y, z = inflate(shape)
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


if __name__ == '__main__':
    main()
