from geometry import *
from test_util import *
from collections import namedtuple

Input = namedtuple('Input', 'triangle points')


def read_input(filename):
    with open(filename) as f:
        triangle = read_point_seq(f.readline())
        n = int(f.readline())
        points = []
        for line in f:
            points.append(read_point(line))
        assert (n == len(points))
        return Input(Triangle(triangle[0], triangle[1], triangle[2]).normalized(), points)

def calc_positions(inputs):
    positions = []
    for point in inputs.points:
        positions.append(inputs.triangle.relative_pos(point))
    return positions


if __name__ == '__main__':
    assert calc_positions(read_input('data/hw1_2_1.txt')) == read_expected_polygon_pos('data/hw1_2_1_expected.txt')
    assert calc_positions(read_input('data/hw1_2_2.txt')) == read_expected_polygon_pos('data/hw1_2_2_expected.txt')
