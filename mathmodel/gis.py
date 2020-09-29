from json import loads
from pathlib import Path
from typing import Any, Dict, List, Iterable
from plotly.graph_objs import Figure, Scatter
from numpy import array


def main():
    layers = [
        Layer(
            'oblasts',
            outer_fill_color='#ebf2e7',
            outer_line_color='#b46198',
            outer_line_width=2
        ),
        Layer(
            'cities',
            is_named=True,
            outer_fill_color='#a1a0a0',
            outer_line_color='#656464',
            outer_line_width=1,
            inner_fill_color='#ebf2e7',
            inner_line_color='#ebf2e7'
        ),
        Layer(
            'rivers',
            outer_fill_color='#9fcee5',
            outer_line_color='#2a5eea',
            outer_line_width=1,
            inner_fill_color='#ebf2e7',
            inner_line_color='#2a5eea',
            inner_line_width=1
        ),
        Layer('roads', outer_line_color='#ffb732', outer_line_width=2)
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
    __slots__ = [
        '_path',
        '_is_named',
        '_outer_fill_color',
        '_outer_line_color',
        '_outer_line_width',
        '_inner_fill_color',
        '_inner_line_color',
        '_inner_line_width'
    ]
    _root_dir = Path(__file__).parent.parent

    def __init__(
        self,
        name: str,
        is_named: bool = False,
        outer_fill_color: str = '#fff',
        outer_line_color: str = '#fff',
        outer_line_width: int = 0,
        inner_fill_color: str = '#fff',
        inner_line_color: str = '#fff',
        inner_line_width: int = 0
    ):
        self._path = self._root_dir / f'layers/{name}.geojson'
        self._is_named = is_named
        self._outer_fill_color = outer_fill_color
        self._outer_line_color = outer_line_color
        self._outer_line_width = outer_line_width
        self._inner_fill_color = inner_fill_color
        self._inner_line_color = inner_line_color
        self._inner_line_width = inner_line_width

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
            return self._polygonize(geometry['coordinates'])
        if geometry['type'] == 'MultiPolygon':
            return (
                s
                for c in geometry['coordinates']
                for s in self._polygonize(c)
            )
        if geometry['type'] == 'LineString':
            coordinates = array(geometry['coordinates'])
            return [
                Scatter(
                    x=coordinates[:, 0],
                    y=coordinates[:, 1],
                    mode='lines',
                    hoverinfo='skip',
                    line={
                        'color': self._outer_line_color,
                        'width': self._outer_line_width
                    }
                )
            ]
        return []

    def _polygonize(
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
                fillcolor=(
                    self._outer_fill_color
                    if i == 0 else
                    self._inner_fill_color
                ),
                line={
                    'color': (
                        self._outer_line_color
                        if i == 0 else
                        self._inner_line_color
                    ),
                    'width': (
                        self._outer_line_width
                        if i == 0 else
                        self._inner_line_width
                    )
                }
            )
            for i, r in enumerate(map(array, coordinates))
        )


if __name__ == '__main__':
    main()
