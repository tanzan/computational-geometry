from geometry import *
from collections import namedtuple
from test_util import *

Input = namedtuple('Input', 'segment points')


def read_input(filename):
    with open(filename) as f:
        segment = read_point_seq(f.readline())
        n = float(f.readline())
        points = []
        for line in f:
            points.append(read_point(line))
        assert (n == len(points))
        return Input(Segment(segment[0], segment[1]), points)


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
