from test_util import *
from cg.algo.convex_hull import *


def read_points(filename):
    with open(filename) as file:
        return read_multi_point(file)


def read_expected_convex_hull(filename):
    with open(filename) as file:
        return read_multi_point(file)


def check(case_name):
    points = read_points(data(__file__, case_name + ".txt"))
    expected_result = sorted(read_expected_convex_hull(data(__file__, case_name + "_expected.txt")))

    assert sorted(graham(points).points) == expected_result
    assert sorted(jarvis(points).points) == expected_result


def test_case_1():
    check("hw2_2_1")


def test_case_2():
    check("hw2_2_2")


def test_case_3():
    check("hw2_2_3")
