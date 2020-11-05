from plotly.graph_objects import Figure, Heatmap


def main():
    """
    TODO
    """
    figure = Figure()
    width, height = 1000, 500
    figure.add_trace(
        Heatmap(
            z=[
                [paint(j / width, i / height) for j in range(width)]
                for i in range(height)
            ],
            zmin=0,
            zmax=1,
            hoverinfo='skip',
            colorscale='inferno',
            showscale=False
        )
    )
    figure.update_layout(
        showlegend=False,
        plot_bgcolor='black',
        margin={'t': 30, 'r': 20, 'b': 30, 'l': 20}
    )
    figure.update_xaxes(
        showticklabels=False,
        showgrid=False,
        showline=False,
        zeroline=False
    )
    figure.update_yaxes(
        scaleanchor='x',
        scaleratio=1,
        showticklabels=False,
        showgrid=False,
        showline=False,
        zeroline=False
    )
    figure.show()


def paint(x: float, y: float, stop: int = 100) -> float:
    """
    TODO
    """
    z = complex(x * 3 - 1.5, y * 3 - 1.5)
    n = 0
    while abs(z) <= 10 and n < stop:
        z = z ** 2 - 0.7269 + 0.1889j
        n += 1
    return n / stop


if __name__ == '__main__':
    main()
