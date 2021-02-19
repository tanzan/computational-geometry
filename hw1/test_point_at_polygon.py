from test_util import *
from collections import namedtuple

Input = namedtuple('Input', 'polygon points')


def read_input_triangle(filename):
    with open(filename) as f:
        triangle = read_point_seq(f)
        n = int(f.readline())
        points = []
        for _ in range(n):
            points.append(read_point(f))
        return Input(Triangle(triangle[0], triangle[1], triangle[2]).normalized(), points)


def read_input_polygon(filename, cls=Polygon):
    with open(filename) as f:
        polygon = read_polygon(f, cls).normalized()
        n = int(f.readline())
        points = []
        for _ in range(n):
            points.append(read_point(f))
        return Input(polygon.prepared(), points)


def calc_positions(inputs):
    positions = []
    for point in inputs.points:
        positions.append(inputs.polygon.relative_pos(point))
    return positions


def test_triangle_case_1():
    assert calc_positions(read_input_triangle(data(__file__, 'hw1_2_1.txt'))) == read_expected_polygon_pos(
        data(__file__, 'hw1_2_1_expected.txt'))


def test_triangle_case_2():
    assert calc_positions(read_input_triangle(data(__file__, 'hw1_2_2.txt'))) == read_expected_polygon_pos(
        data(__file__, 'hw1_2_2_expected.txt'))


def test_polygon_case_1():
    assert calc_positions(read_input_polygon(data(__file__, 'hw1_3_1.txt'))) == read_expected_polygon_pos(
        data(__file__, 'hw1_3_1_expected.txt'))


def test_polygon_case_2():
    assert calc_positions(read_input_polygon(data(__file__, 'hw1_3_2.txt'))) == read_expected_polygon_pos(
        data(__file__, 'hw1_3_2_expected.txt'))


def test_convex_polygon_case_1():
    assert calc_positions(read_input_polygon(data(__file__, 'hw1_4_1.txt'), ConvexPolygon)) == read_expected_polygon_pos(
        data(__file__, 'hw1_4_expected.txt'))
