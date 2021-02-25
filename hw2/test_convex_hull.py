from test_util import *
from cg.algo.convex_hull import *


def read_points(filename):
    with open(filename) as file:
        return read_multi_point(file)


def read_expected_convex_hull(filename):
    with open(filename) as file:
        return read_multi_point(file)


def check(case_name):
    result = graham(read_points(data(__file__, case_name + ".txt")))
    expected_result = read_expected_convex_hull(data(__file__, case_name + "_expected.txt"))
    assert sorted(result.points) == sorted(expected_result)


def test_case_1():
    check("hw2_2_1")


def test_case_2():
    check("hw2_2_2")


def test_case_3():
    check("hw2_2_3")
