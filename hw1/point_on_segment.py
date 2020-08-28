from geometry import *
from collections import namedtuple

Input = namedtuple('Input', 'segment points')


def read_input(filename):
    with open(filename) as f:
        segment = f.readline().split()
        n = float(f.readline())
        p1 = Point(float(segment[0]), float(segment[1]))
        p2 = Point(float(segment[2]), float(segment[3]))
        points = []
        for line in f:
            point = line.split()
            points.append(Point(float(point[0]), float(point[1])))
        assert (n == len(points))
        return Input(Segment(p1, p2), points)


def read_expected(filename):
    with open(filename) as f:
        expected = []
        for line in f.readlines():
            expected.append(SegmentPos(line.strip()))
        return expected


def calc_positions(inputs):
    positions = []
    for point in inputs.points:
        positions.append(inputs.segment.relative_pos(point))
    return positions


if __name__ == '__main__':
    assert calc_positions(read_input('data/hw1_1_1.txt')) == read_expected('data/hw1_1_1_expected.txt')
    assert calc_positions(read_input('data/hw1_1_2.txt')) == read_expected('data/hw1_1_2_expected.txt')
