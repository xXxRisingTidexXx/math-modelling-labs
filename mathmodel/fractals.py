from plotly.graph_objects import Figure, Heatmap


def main():
    """
    TODO
    """
    figure = Figure()
    width, height = 400, 200
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
        paper_bgcolor='black',
        plot_bgcolor='black',
        margin={'t': 0, 'r': 0, 'b': 0, 'l': 0}
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


def paint(x: float, y: float, stop: int = 1000) -> float:
    """
    TODO
    """
    z = complex(x * 3 - 1.5, y * 3 - 1.5)
    n = 0
    while abs(z) <= 10 and n < stop:
        z = z ** 2 - 0.1 + 0.65j
        n += 1
    return n / stop


if __name__ == '__main__':
    main()
