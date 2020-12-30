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

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        if self.x == other.x:
            return self.y < other.y

        return self.x < other.x

    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)

    def lt_y(self, other):
        if self.y == other.y:
            return self.x < other.x

        return self.y < other.y