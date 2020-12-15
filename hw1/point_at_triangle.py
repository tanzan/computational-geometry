from geometry import *
from collections import namedtuple

Input = namedtuple('Input', 'triangle points')


def read_input(filename):
    with open(filename) as f:
        triangle = f.readline().split()
        n = int(f.readline())
        p1 = Point(float(triangle[0]), float(triangle[1]))
        p2 = Point(float(triangle[2]), float(triangle[3]))
        p3 = Point(float(triangle[4]), float(triangle[5]))
        points = []
        for line in f:
            point = line.split()
            points.append(Point(float(point[0]), float(point[1])))
        assert (n == len(points))
        return Input(Triangle(p1, p2, p3).normalized(), points)


def read_expected(filename):
    with open(filename) as f:
        expected = []
        for line in f.readlines():
            expected.append(PolygonPos(line.strip()))
        return expected


def calc_positions(inputs):
    positions = []
    for point in inputs.points:
        positions.append(inputs.triangle.relative_pos(point))
    return positions


if __name__ == '__main__':
    assert calc_positions(read_input('data/hw1_2_1.txt')) == read_expected('data/hw1_2_1_expected.txt')
    assert calc_positions(read_input('data/hw1_2_2.txt')) == read_expected('data/hw1_2_2_expected.txt')
