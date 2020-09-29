from json import loads
from pathlib import Path
from typing import Any, Dict, List, Iterable
from plotly.graph_objs import Figure, Scatter
from numpy import array


def main():
    layers = [
        Layer(
            'oblasts',
            Style('#deeed5', '#b46198', 2),
            Style('#fff', '#fff', 0)
        ),
        Layer(
            'rivers',
            Style('#9fcee5', '#2a5eea', 1),
            Style('#deeed5', '#2a5eea', 1)
        )
    ]
    figure = Figure()
    for layer in layers:
        figure.add_traces(layer.scatters())
    figure.update_layout(plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
    figure.update_xaxes(
        showline=True,
        linewidth=2,
        linecolor='#8b8b8b',
        mirror=True
    )
    figure.update_yaxes(
        scaleanchor='x',
        scaleratio=1.5,
        showline=True,
        linewidth=2,
        linecolor='#8b8b8b',
        mirror=True
    )
    figure.show()


class Layer:
    __slots__ = ['_path', '_outer_style', '_inner_style']
    _root_dir = Path(__file__).parent.parent

    def __init__(self, name: str, outer_style: 'Style', inner_style: 'Style'):
        self._path = self._root_dir / f'layers/{name}.geojson'
        self._outer_style = outer_style
        self._inner_style = inner_style

    def scatters(self) -> List[Scatter]:
        with open(self._path) as stream:
            content = stream.read()
        return [
            s
            for f in loads(content)['features']
            for s in self._flatten(f['geometry'])
        ]

    def _flatten(self, geometry: Dict[str, Any]) -> Iterable[Scatter]:
        if geometry['type'] == 'Polygon':
            return self._scatter(geometry['coordinates'])
        if geometry['type'] == 'MultiPolygon':
            return (
                s
                for c in geometry['coordinates']
                for s in self._scatter(c)
            )
        return []

    def _scatter(
        self,
        coordinates: List[List[List[float]]]
    ) -> Iterable[Scatter]:
        return (
            Scatter(
                x=r[:, 0],
                y=r[:, 1],
                mode='lines',
                fill='toself',
                hoverinfo='skip',
                fillcolor=self._style(i).fill_color,
                line={
                    'color': self._style(i).line_color,
                    'width': self._style(i).line_width
                }
            )
            for i, r in enumerate(map(array, coordinates))
        )

    def _style(self, i: int) -> 'Style':
        return self._outer_style if i == 0 else self._inner_style


class Style:
    __slots__ = ['fill_color', 'line_color', 'line_width']

    def __init__(
        self,
        fill_color: str,
        line_color: str,
        line_width: int
    ):
        self.fill_color = fill_color
        self.line_color = line_color
        self.line_width = line_width


if __name__ == '__main__':
    main()
