from geometry import *
import numpy as np


def test_oriented_сw():
    assert angle.oriented(Segment(Point(0, 0), Point(2, 2)), Segment(Point(0, 0), Point(-3, 3))) == np.radians(90)
    assert angle.oriented(Segment(Point(0, 0), Point(-3, -3)), Segment(Point(0, 0), Point(2, -2))) == np.radians(90)
    assert angle.oriented(Segment(Point(0, 0), Point(2, 2)), Segment(Point(0, 0), Point(-3, 0))) == np.radians(135)
    assert angle.oriented(Segment(Point(0, 0), Point(-3, -3)), Segment(Point(0, 0), Point(2, 0))) == np.radians(135)


def test_oriented_ccw():
    assert angle.oriented(Segment(Point(0, 0), Point(-3, 3)), Segment(Point(0, 0), Point(2, 2))) == -np.radians(90)
    assert angle.oriented(Segment(Point(0, 0), Point(2, -2)), Segment(Point(0, 0), Point(-3, -3))) == -np.radians(90)
    assert angle.oriented(Segment(Point(0, 0), Point(-3, 0)), Segment(Point(0, 0), Point(2, 2))) == -np.radians(135)
    assert angle.oriented(Segment(Point(0, 0), Point(2, 0)), Segment(Point(0, 0), Point(-3, -3))) == -np.radians(135)


def test_pi():
    assert angle.oriented(Segment(Point(0, 0), Point(-3, -3)), Segment(Point(0, 0), Point(2, 2))) == np.pi
    assert angle.oriented(Segment(Point(0, 0), Point(2, 2)), Segment(Point(0, 0), Point(-3, -3))) == np.pi


def test_zero():
    assert angle.oriented(Segment(Point(0, 0), Point(2, 2)), Segment(Point(0, 0), Point(3, 3))) == 0
    assert angle.oriented(Segment(Point(0, 0), Point(3, 3)), Segment(Point(0, 0), Point(2, 2))) == 0

