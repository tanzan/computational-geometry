from ..geometry import Segment, SegmentPos, ConvexPolygon, Point, angle
import numpy as np


def graham(points):
    sorted_points = sorted(points)

    def semi_hull(pos):
        hull = sorted_points[:2]

        for point in sorted_points[2:]:
            hull.append(point)
            while len(hull) > 2 and pos != Segment(hull[-3], hull[-2]).relative_pos(hull[-1]):
                del hull[-2]
        return hull

    upper_hull = semi_hull(SegmentPos.RIGHT)

    lower_hull = semi_hull(SegmentPos.LEFT)

    return ConvexPolygon(upper_hull + list(reversed(lower_hull[1:-1])))


def jarvis(points):
    point_set = set(points)
    hull = []

    hull_point = min(points, key=lambda p: Point(p.y, p.x))
    hull.append(hull_point)
    point_set.remove(hull_point)

    prev_hull_point = Point(hull_point.x - 1, hull_point.y)

    start_hull_point = hull_point

    while True:

        alpha = 0
        seg_len = 0
        prev_seg = Segment(hull_point, prev_hull_point)
        next_hull_point = None

        for point in point_set:
            seg = Segment(hull_point, point)
            a = angle.oriented(prev_seg, seg)
            if a == np.pi:
                a = -a
            if a < alpha or (a == alpha and seg.length > seg_len):
                alpha = a
                seg_len = seg.length
                next_hull_point = point

        hull_point = next_hull_point

        if len(hull) == 1:
            point_set.add(start_hull_point)

        if hull_point == start_hull_point:
            break

        prev_hull_point = hull[-1]
        hull.append(hull_point)
        point_set.remove(hull_point)

    return ConvexPolygon(hull)
