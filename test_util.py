from geometry import *

def read_point_seq(line):
    points = []
    coords = line.strip().split()
    for i in range(0, len(coords), 2):
        points.append(Point(float(coords[i]), float(coords[i + 1])))
    return points


def read_point(line):
    return read_point_seq(line)[0]


def read_expected_polygon_pos(filename):
    with open(filename) as f:
        expected = []
        for line in f.readlines():
            expected.append(PolygonPos(line.strip()))
        return expected
