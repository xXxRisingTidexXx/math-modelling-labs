from plotly.graph_objs import Figure
from mathmodel.layers import Layer


def main():
    layers = [
        Layer(
            'oblasts',
            is_filled=True,
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
        )
    ]
    figure = Figure()
    for layer in layers:
        figure.add_traces(layer.render3d())
    figure.update_layout(showlegend=False)
    figure.update_yaxes(scaleanchor='x', scaleratio=1.5)
    figure.show()


if __name__ == '__main__':
    main()
