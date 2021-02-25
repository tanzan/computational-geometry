import enum
from .segment import Segment, SegmentPos
from .point import Point
import numpy as np
import bisect as bs
from . import angle


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


class Polygon:
    def __init__(self, points):
        if len(points) < 3:
            raise ValueError("Polygon cannot contain less than 3 points")
        self._points = points

    @property
    def points(self):
        return self._points

    def __str__(self):
        return f"POLYGON(({', '.join(str(p) for p in self.points)}, {str(self.points[0])}))"

    def __eq__(self, other):
        return self.points == other.points

    @property
    def segments(self):
        segs = []
        for i in range(len(self.points)):
            segs.append(Segment(self.points[i], self.points[(i + 1) % len(self.points)]))
        return segs

    def prepared(self):
        return self

    def normalized(self):
        n = len(self.points)

        min_i = 0
        for i in range(1, n):
            if self.points[i] < self.points[min_i]:
                min_i = i

        normalized_points = []
        for i in range(0, n):
            normalized_points.append(self.points[(i + min_i) % n])

        hi_i = 0
        for i in range(1, n):
            if self.points[hi_i].y < self.points[i].y:
                hi_i = i

        c = Segment(self.points[(hi_i - 1) % n], self.points[hi_i]).relative_pos(self.points[(hi_i + 1) % n])

        if c == SegmentPos.ON_SEGMENT or c == SegmentPos.ON_LINE:
            is_ccv = self.points[(hi_i - 1) % n].x < self.points[(hi_i + 1) % n].x
        else:
            is_ccv = c == SegmentPos.LEFT

        if is_ccv:
            normalized_points.reverse()

        return type(self)(normalized_points)

    def relative_pos(self, point):

        def ray_position(s):
            s_norm = s.normalized_y()
            ray_pos = s_norm.relative_pos(point)
            if ray_pos == SegmentPos.RIGHT:
                if s_norm.start.y <= point.y <= s_norm.end.y:
                    if point.y == s_norm.start.y:
                        # Ignore bottom point intersection
                        return SegmentPos.LEFT
                    else:
                        return SegmentPos.RIGHT
                else:
                    return SegmentPos.LEFT
            return ray_pos

        n_cross = 0

        for seg in self.segments:
            pos = ray_position(seg)
            if pos == SegmentPos.ON_SEGMENT:
                return PolygonPos.BORDER
            elif pos == SegmentPos.RIGHT:
                n_cross += 1

        if n_cross % 2 == 1:
            return PolygonPos.INSIDE

        return PolygonPos.OUTSIDE

    def is_convex(self):

        norm = self.normalized()
        segs = norm.segments

        for i in range(len(segs)):
            if angle.oriented(segs[i].reversed(), segs[(i + 1) % len(segs)]) <= 0:
                return False

        return True


class Triangle(Polygon):
    def __init__(self, a, b, c):
        super().__init__([a, b, c])

    @property
    def a(self):
        return self.points[0]

    @property
    def b(self):
        return self.points[1]

    @property
    def c(self):
        return self.points[2]

    def __str__(self):
        return f'TRIANGLE({self.a} , {self.b}, {self.c})'

    def normalized(self):
        normalized = Polygon(self.points).normalized()
        return Triangle(normalized.points[0], normalized.points[1], normalized.points[2])

    def relative_pos(self, point):
        segs = self.segments
        for seg in segs:
            pos = seg.relative_pos(point)
            if pos == SegmentPos.ON_SEGMENT:
                return PolygonPos.BORDER
            if pos != SegmentPos.RIGHT:
                return PolygonPos.OUTSIDE
        return PolygonPos.INSIDE

    def centroid(self):
        return Point((self.points[0].x + self.points[1].x + self.points[2].x) / 3,
                     (self.points[0].y + self.points[1].y + self.points[2].y) / 3)


class ConvexPolygon(Polygon):

    def __init__(self, points):
        super().__init__(points)
        self._index = None
        self._index_center = None

    def _index_key(self, point):
        centered_point = Point(point.x - self._index_center.x, point.y - self._index_center.y)
        tan = np.abs(centered_point.y / centered_point.x)
        if centered_point.x <= 0 < centered_point.y:
            return 1, tan
        elif centered_point.x > 0 and centered_point.y >= 0:
            return 2, -tan
        elif centered_point.x >= 0 > centered_point.y:
            return 3, tan
        elif centered_point.x < 0 and centered_point.y <= 0:
            return 4, -tan
        else:
            raise ValueError()

    def _indexed(self):
        if len(self.points) < 5:
            center_triangle = Triangle(self.points[0], self.points[1], self.points[2])
        else:
            center_triangle = Triangle(self.points[0], self.points[2], self.points[3])

        self._index_center = center_triangle.centroid()

        self._index = sorted([(self._index_key(point), i) for i, point in enumerate(self.points)], key=lambda x: x[0])
        self._index_keys = [key[0] for key in self._index]

        return self

    def prepared(self):
        if self._index is None:
            return self._indexed()
        return self

    def relative_pos(self, point):
        if self._index is None:
            return super().relative_pos(point)

        if point == self._index_center:
            return PolygonPos.INSIDE

        i = bs.bisect_left(self._index_keys, self._index_key(point))

        point_index = self._index[i][1]

        pos = Segment(self.points[(point_index - 1) % len(self.points)], self.points[point_index]).relative_pos(point)

        if pos == SegmentPos.ON_SEGMENT:
            return PolygonPos.BORDER
        elif pos == SegmentPos.RIGHT:
            return PolygonPos.INSIDE

        return PolygonPos.OUTSIDE
