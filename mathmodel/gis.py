from json import loads
from typing import List
from plotly.graph_objects import Figure
from plotly.graph_objs import Scatter
from numpy import array


def main():
    figure = Figure()
    figure.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    figure.update_xaxes(showline=True, linewidth=2, linecolor='#8b8b8b', mirror=True)
    figure.update_yaxes(
        scaleanchor='x',
        scaleratio=1.5,
        showline=True,
        linewidth=2,
        linecolor='#8b8b8b',
        mirror=True
    )
    figure.show()


def load_oblast() -> Scatter:
    with open('geodata/dnipropetrovska_oblast.geojson') as stream:
        content = stream.read()
    bounds = array(loads(content)['features'][0]['geometry']['coordinates'][0])
    return Scatter(
        x=bounds[:, 0],
        y=bounds[:, 1],
        mode='lines',
        fill='toself',
        fillcolor='#deeed5',
        hoverinfo='skip',
        line={'color': '#b46198', 'width': 2}
    )


def load_scatters() -> List[Scatter]:
    pass


def load_rivers() -> List[Scatter]:
    with open('geodata/rivers.geojson') as stream:
        content = stream.read()
    return [Scatter() for f in loads(content)['features']]


if __name__ == '__main__':
    main()
