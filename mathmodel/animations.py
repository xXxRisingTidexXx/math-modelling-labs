from typing import Tuple
from PIL.Image import fromarray, Image
from numpy import linspace, pi, uint8
from cmath import exp
from multiprocessing import Pool, cpu_count


def main():
    pool = Pool(cpu_count())
    pairs = pool.map(draw, enumerate(linspace(0, 2 * pi, 250)))
    pool.close()
    images = [p[1] for p in sorted(pairs, key=lambda p: p[0])]
    images[0].save(
        'images/julia.gif',
        save_all=True,
        append_images=images[1:],
        optimize=True,
        duration=65,
        loop=0
    )


def draw(ia: Tuple[int, float]) -> Tuple[int, Image]:
    return (
        ia[0],
        fromarray(
            uint8(
                [
                    [paint(x, y, ia[1]) for x in linspace(3.5, -3.5, 200)]
                    for y in linspace(3.5, -3.5, 200)
                ]
            )
        )
    )


def paint(x: float, y: float, a: float) -> float:
    z, c = x + y * 1j, 0.7885 * exp(a * 1j)
    n, stop = 0, 50
    while abs(z) <= 10 and n < stop:
        z = z ** 2 + c
        n += 1
    return n / stop * 255


if __name__ == '__main__':
    main()
