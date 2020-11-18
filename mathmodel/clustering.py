from typing import Optional
from numpy import linspace, sum, ndarray, max, argmin, array, append
from plotly.figure_factory import create_dendrogram
from plotly.graph_objects import Bar, Figure
from sklearn.preprocessing import scale


def main():
    """
    Тут відбувається обчислення всіх масивів й побудова графіків.
    """
    names = ['alpha', 'beta', 'gamma', 'delta']
    companies = array(
        [
            [67, 57, 49, 81, 63],
            [73, 59, 41, 87, 59],
            [65, 57, 43, 77, 63],
            [67, 55, 87, 73, 63]
        ]
    )
    z = scale(companies)
    weights = linspace(1, 5, 5)
    unweighted = score(z)
    non_normalized = score(z, weights)
    normalized = score(z, weights / sum(weights))
    figure = Figure()  # Графік оцінок кожної з варіацій таксонометричного методу.
    figure.add_trace(Bar(name='Незважені', x=names, y=unweighted))
    figure.add_trace(Bar(name='Зважені ненормалізовані', x=names, y=non_normalized))
    figure.add_trace(Bar(name='Зважені нормалізовані', x=names, y=normalized))
    figure.update_layout(margin={'t': 20, 'r': 20, 'b': 20, 'l': 20})
    figure.write_image('images/scores.png', width=1200, height=600)
    features = ['досвід', 'фінанси', 'іновації', 'динаміка', 'стабільність']
    standard = max(companies, 0)
    figure = Figure()  # Графік профілів таксонометричного методу й еталону.
    figure.add_trace(Bar(name='Незважені', x=features, y=companies[argmin(unweighted)]))
    figure.add_trace(
        Bar(
            name='Зважені ненормалізовані',
            x=features,
            y=companies[argmin(non_normalized)]
        )
    )
    figure.add_trace(
        Bar(name='Зважені нормалізовані', x=features, y=companies[argmin(normalized)])
    )
    figure.add_trace(Bar(name='Еталон', x=features, y=standard))
    figure.update_layout(margin={'t': 20, 'r': 20, 'b': 20, 'l': 20})
    figure.write_image('images/profiles.png', width=1200, height=600)
    figure = create_dendrogram(  # Дендрограма відносно еталонного рішення.
        append(companies, [standard], 0),
        orientation='left',
        labels=names + ['standard']
    )
    figure.update_layout(margin={'t': 20, 'r': 20, 'b': 20, 'l': 20})
    figure.write_image('images/dendrogram.png', width=1200, height=600)


def score(z: ndarray, weights: Optional[ndarray] = None) -> ndarray:
    """
    Обрахунок квазівідстаней для таксонометричного методу.
    """
    squares = (z - max(z, 0)) ** 2
    if weights is not None:
        squares = squares * weights
    return sum(squares, 1)


if __name__ == '__main__':
    main()
