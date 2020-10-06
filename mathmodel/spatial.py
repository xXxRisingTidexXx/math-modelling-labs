from numpy import array, hstack, stack, sum, sqrt, full, reshape
from plotly.graph_objs import Scatter, Scatter3d
from plotly.subplots import make_subplots
from cv2 import (
    imread, COLOR_BGR2GRAY, RETR_TREE, CHAIN_APPROX_SIMPLE, cvtColor, threshold,
    findContours
)


def main():
    contours = findContours(
        threshold(cvtColor(imread('images/shape.png'), COLOR_BGR2GRAY), 127, 255, 0)[1],
        RETR_TREE,
        CHAIN_APPROX_SIMPLE
    )[0]
    figure = make_subplots(
        rows=1,
        cols=3,
        specs=[[{'type': 'xy'}, {'type': 'scene'}, {'type': 'scene'}]]
    )
    # frame = array(
    #     [
    #         [4.79421615600582, 6.01198612991254],
    #         [4.8328399658203, 6.02756149992565],
    #         [4.8809051513672, 6.0158800190595],
    #         [4.91781234741214, 6.0125424016945],
    #         [4.9324035644531, 5.9969665519166],
    #         [4.95386123657223, 5.9736018443636],
    #         [4.9418449401855, 6.0181050846108],
    #         [4.96931076049805, 6.02700524527826],
    #         [4.99334335327145, 6.0403551816698],
    #         [5.0165176391602, 6.0103173107591],
    #         [5.0053596496582, 6.05147984943855],
    #         [5.0165176391602, 6.08040279767906],
    #         [5.05256652832035, 6.08874563694535],
    #         [5.0165176391602, 6.0870770805144],
    #         [4.9856185913086, 6.10487472132995],
    #         [4.94871139526364, 6.11766637429625],
    #         [4.9160957336426, 6.1254524334865],
    #         [4.93583679199222, 6.1421364272228],
    #         [4.95729446411136, 6.15603931907366],
    #         [4.92897033691403, 6.145473157437],
    #         [4.90407943725582, 6.1260085758122],
    #         [4.86030578613285, 6.1299015543247],
    #         [4.8431396484375, 6.1660491556325],
    #         [4.8508644104004, 6.12712085855996],
    #         [4.83541488647457, 6.1243401469312],
    #         [4.77790832519528, 6.1393558012603],
    #         [4.81395721435543, 6.1154417631114],
    #         [4.78992462158203, 6.0831837599658],
    #         [4.71782684326172, 6.06872258283346],
    #         [4.78219985961914, 6.0626042633693],
    #         [4.78992462158203, 6.048142475761],
    #         [4.8122406005859, 6.0347927525954],
    #         [4.79421615600582, 6.01198612991254]
    #     ]
    # )
    frame = array([[1, 2.5], [5, 7], [4, 8.3], [2, 4.1], [1, 2.5]])
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
