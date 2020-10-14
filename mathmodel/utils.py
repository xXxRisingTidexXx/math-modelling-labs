from typing import Tuple
from numpy import full, sqrt, ndarray


def inflate(
    shape: ndarray,
    r: float = 50,
    z: float = 20
) -> Tuple[ndarray, ndarray, ndarray]:
    """
    Логіка "набухання" отриманої 2D-фігури.
    """
    x, y, z = shape[:, 0], shape[:, 1], full((shape.shape[0],), z)
    k = r / sqrt(x ** 2 + y ** 2 + (z + r) ** 2)
    return x * k, y * k, z * k
