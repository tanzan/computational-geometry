import enum
from typing import Dict

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


class SegmentPos(enum.Enum):
    ON_SEGMENT = 1
    ON_LINE = 2
    LEFT = 3
    RIGHT = 4

    def __str__(self):
        return SegmentPos._value_to_str.get(self)


SegmentPos.__new__ = lambda cls, value: (cls._str_to_value[value]
                                         if isinstance(value, str) else
                                         super(SegmentPos, cls).__new__(cls, value))

SegmentPos._str_to_value = {'ON_SEGMENT': SegmentPos.ON_SEGMENT,
                            'ON_LINE': SegmentPos.ON_LINE,
                            'LEFT': SegmentPos.LEFT,
                            'RIGHT': SegmentPos.RIGHT}

SegmentPos._value_to_str = {val: key for key, val in SegmentPos._str_to_value.items()}


class Segment:
    def __init__(self, start, end):
        self._start = start
        self._end = end

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def vec(self):
        return self.end.vec - self.start.vec

    def __str__(self):
        return "SEGMENT(" + str(self._start) + "," + str(self._end) + ")"

    def relative_pos(self, point):
        c = np.cross(self.vec, point.vec - self.start.vec)
        if c == 0:
            if (self.start.x <= point.x <= self.end.x) or (
                    self.end.x <= point.x <= self.start.x):
                return SegmentPos.ON_SEGMENT
            return SegmentPos.ON_LINE
        elif c > 0:
            return SegmentPos.LEFT
        else:
            return SegmentPos.RIGHT


class PolygonPos(enum.Enum):
    BORDER = 1
    OUTSIDE = 2
    INSIDE = 3

    def __str__(self):
        return PolygonPos._value_to_str.get(self)


PolygonPos.__new__ = lambda cls, value: (cls._str_to_value[value]
                                         if isinstance(value, str) else
                                         super(PolygonPos, cls).__new__(cls, value))

PolygonPos._str_to_value = {'BORDER': PolygonPos.BORDER,
                            'OUTSIDE': PolygonPos.OUTSIDE,
                            'INSIDE': PolygonPos.INSIDE}

PolygonPos._value_to_str = {val: key for key, val in PolygonPos._str_to_value.items()}


class Triangle:
    def __init__(self, a, b, c):
        self._points = []
        self._points.append(a)
        self._points.append(b)
        self._points.append(c)

    @property
    def a(self):
        return self._points[0]

    @property
    def b(self):
        return self._points[1]

    @property
    def c(self):
        return self._points[2]

    def __str__(self):
        return 'TRIANGLE(' + str(self.a) + ',' + str(self.b) + ',' + str(self.c) + ')'

    def normalized(self):
        def less(p1, p2):
            if p1.x == p2.x:
                return p1.y < p2.y
            else:
                return p1.x < p2.x

        n = len(self._points)

        min_i = 0
        for i in range(1, n):
            if less(self._points[i], self._points[min_i]):
                min_i = i

        normalized_points = []
        for i in range(0, n):
            normalized_points.append(self._points[(i + min_i) % n])

        hi_i = 0
        for i in range(1, n):
            if self._points[hi_i].y < self._points[i].y:
                hi_i = i

        c = Segment(self._points[(hi_i - 1) % n], self._points[hi_i]).relative_pos(self._points[(hi_i + 1) % n])

        if c == SegmentPos.ON_SEGMENT or c == SegmentPos.ON_LINE:
            is_ccv = self._points[(hi_i - 1) % n].x < self._points[(hi_i + 1) % n].x
        else:
            is_ccv = c == SegmentPos.LEFT

        if is_ccv:
            normalized_points.reverse()

        return Triangle(normalized_points[0], normalized_points[1], normalized_points[2])

    @property
    def segments(self):
        segs = []
        for i in range(len(self._points)):
            segs.append(Segment(self._points[i], self._points[(i + 1) % len(self._points)]))
        return segs

    def relative_pos(self, point):
        segs = self.segments
        for seg in segs:
            pos = seg.relative_pos(point)
            if pos == SegmentPos.ON_SEGMENT:
                return PolygonPos.BORDER
            if pos != SegmentPos.RIGHT:
                return PolygonPos.OUTSIDE
        return PolygonPos.INSIDE
