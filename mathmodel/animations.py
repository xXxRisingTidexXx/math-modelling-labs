from PIL.Image import fromarray
from numpy import linspace, pi, uint8
from cmath import exp


def main():
    images = [
        fromarray(
            uint8(
                [
                    [pixel(x, y, a) for x in linspace(3.4, -3.4, 1600)]
                    for y in linspace(1.7, -1.7, 800)
                ]
            )
        )
        for a in linspace(0, 2 * pi, 100)
    ]

    # width = 200
    # center = width // 2
    # color_1 = (0, 0, 0)
    # color_2 = (255, 255, 255)
    # max_radius = int(center * 1.5)
    # step = 8
    # for i in range(0, max_radius, step):
    #     im = Image.new('RGB', (width, width), color_1)
    #     draw = ImageDraw.Draw(im)
    #     draw.ellipse((center - i, center - i, center + i, center + i), fill=color_2)
    #     images.append(im)
    # for i in range(0, max_radius, step):
    #     im = Image.new('RGB', (width, width), color_2)
    #     draw = ImageDraw.Draw(im)
    #     draw.ellipse((center - i, center - i, center + i, center + i), fill=color_1)
    #     images.append(im)
    # images[0].save(
    #     'images/pillow.gif',
    #     save_all=True,
    #     append_images=images[1:],
    #     optimize=False,
    #     duration=40,
    #     loop=0
    # )


def pixel(x: float, y: float, a: float) -> float:
    z, c = x + y * 1j, 0.7885 * exp(a * 1j)
    n, stop = 0, 50
    while abs(z) <= 10 and n < stop:
        z = z ** 2 + c
        n += 1
    return n / stop * 255


if __name__ == '__main__':
    main()
