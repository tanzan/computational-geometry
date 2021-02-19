from geometry import *
import os


def data(path, file):
    return os.path.dirname(path) + "/data/" + file


def read_point_seq(file):
    points = []
    coords = file.readline().strip().split()
    for i in range(0, len(coords), 2):
        points.append(Point(float(coords[i]), float(coords[i + 1])))
    return points


def read_point(file):
    return read_point_seq(file)[0]


def read_polygon(file, cls=Polygon):
    size = int(file.readline())
    shell = read_point_seq(file)
    assert size == len(shell)
    return cls(shell)


def read_multi_point(file):
    size = int(file.readline())
    points = read_point_seq(file)
    assert size == len(points)
    return points


def read_expected_polygon_pos(filename):
    with open(filename) as f:
        expected = []
        for line in f:
            expected.append(PolygonPos(line.strip()))
        return expected
