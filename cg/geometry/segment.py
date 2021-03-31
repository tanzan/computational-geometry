import numpy as np
import enum


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

    @property
    def length(self):
        return np.linalg.norm(self.vec)

    def __str__(self):
        return "SEGMENT(" + str(self._start) + "," + str(self._end) + ")"

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    @property
    def angle(self):
        v = self.vec
        a = np.arctan2(v[1], v[0])
        if a < 0:
            return a + 2 * np.pi
        return a

    def reversed(self):
        return Segment(self.end, self.start)

    def normalized(self):
        if self.start > self.end:
            return Segment(self.end, self.start)
        return Segment(self.start, self.end)

    def normalized_y(self):
        if self.end.lt_y(self.start):
            return Segment(self.end, self.start)
        return Segment(self.start, self.end)

    def relative_pos(self, point):
        c = np.cross(self.vec, point.vec - self.start.vec)
        if c == 0:
            start_x, end_x = (self.start.x, self.end.x) if self.start.x < self.end.x else (self.end.x, self.start.x)
            start_y, end_y = (self.start.y, self.end.y) if self.start.y < self.end.y else (self.end.y, self.start.y)
            if (start_x <= point.x <= end_x) and (start_y <= point.y <= end_y):
                return SegmentPos.ON_SEGMENT
            return SegmentPos.ON_LINE
        elif c > 0:
            return SegmentPos.LEFT
        else:
            return SegmentPos.RIGHT
