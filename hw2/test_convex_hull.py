from algo.convex_hull import *
from test_util import *


def read_points(filename):
    with open(filename) as file:
        return read_multi_point(file)


def read_expected_convex_hull(filename):
    with open(filename) as file:
        return read_polygon(file)


def test_case_1():
    assert graham(read_points(data(__file__, "hw2_2_1.txt"))) == read_expected_convex_hull(
        data(__file__, "hw2_2_1_expected.txt"))


def test_case_2():
    assert graham(read_points(data(__file__, "hw2_2_2.txt"))) == read_expected_convex_hull(
        data(__file__, "hw2_2_2_expected.txt"))


def test_case_3():
    assert graham(read_points(data(__file__, "hw2_2_3.txt"))) == read_expected_convex_hull(
        data(__file__, "hw2_2_3_expected.txt"))
