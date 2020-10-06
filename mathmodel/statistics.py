from numpy import array, arange, cov, corrcoef
from plotly.graph_objs import Figure, Scatter
from tabulate import tabulate


def main():
    # Ініціалізуємо вибірки й масив індексів.
    x0 = array([95, 116, 150, 87, 52, 156, 173, 41, 54, 197, 149, 16, 92, 198, 108, 39, 124])
    x1 = array([114, 110, 99, 109, 128, 112, 85, 107, 142, 114, 71, 104, 155, 118, 58, 99, 167])
    ix = arange(0, len(x0))

    # Виведення статистичних показників x0 і x1 у stdout.
    print(
        tabulate(
            [
                ['x0', 'x1'],
                ['mean', x0.mean(), x1.mean()],
                ['var', x0.var(), x1.var()],
                ['std', x0.std(), x1.std()],
            ],
            headers='firstrow',
            tablefmt='psql',
            numalign='right'
        )
    )

    # Візуалізуємо вибірки через браузер.
    figure = Figure()
    figure.add_trace(Scatter(x=ix, y=x0, mode='lines+markers', name='x0'))
    figure.add_trace(Scatter(x=ix, y=x1, mode='lines+markers', name='x1'))
    figure.update_layout(title=f'cov = {cov(x0, x1)[0][1]:.4f}, cor = {corrcoef(x0, x1)[0][1]:.4f}')
    figure.show()


if __name__ == '__main__':
    main()
