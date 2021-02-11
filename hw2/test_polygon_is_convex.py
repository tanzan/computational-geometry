from test_util import *


def read_input_polygon(filename):
    with open(filename) as f:
        return read_polygon(f).normalized()


def read_expected(filename):
    with open(filename) as f:
        expected = f.read().strip().upper()
        if expected == 'CONVEX':
            return True
        elif expected == 'NOT_CONVEX':
            return False
        else:
            raise ValueError(expected[0:20])


def test_case_1():
    assert read_input_polygon(data(__file__, 'hw2_1_1.txt')).is_convex() == read_expected(
        data(__file__, 'hw2_1_1_expected.txt'))


def test_case_2():
    assert read_input_polygon(data(__file__, 'hw2_1_2.txt')).is_convex() == read_expected(
        data(__file__, 'hw2_1_2_expected.txt'))
