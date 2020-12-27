import numpy as np


class Point:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def vec(self):
        return np.array([self.x, self.y])

    def __str__(self):
        return str(self._x) + " " + str(self._y)
