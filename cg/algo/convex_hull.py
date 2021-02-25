from ..geometry import Segment, SegmentPos, ConvexPolygon


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
