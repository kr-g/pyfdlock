import unittest

from tests.test_func import eq, list_eq

from pyfdlock.lock import *
from pyfdlock.lock import _Region


class SegmentTestCase(unittest.TestCase):
    def test_segment_new(self):
        self.assertRaises(TypeError, _Region)

    def test_segment_new_minus_pos(self):
        self.assertRaises(BadPositionException, _Region, pos=-1, length=0)

    def test_segment_new_minus_len(self):
        self.assertRaises(NegativeLengthException, _Region, pos=0, length=-1)

    def test_eq(self):
        a = _Region(1, 2)
        b = _Region(1, 2)
        self.assertTrue(a, b)

    def test_neq1(self):
        a = _Region(1, 2)
        b = _Region(1, 3)
        self.assertTrue(a, b)

    def test_neq2(self):
        a = _Region(1, 2)
        b = _Region(2, 2)
        self.assertTrue(a, b)

    def test_neq3(self):
        a = _Region(1, 2)
        b = _Region(3, 4)
        self.assertTrue(a, b)

    def test_list_eq(self):
        a = [1, 2, 3]
        b = [1, 2, 3]
        self.assertTrue(list_eq(a, b))

    def test_list_neq(self):
        a = [1, 2, 3]
        b = [11, 2, 3]
        self.assertFalse(list_eq(a, b))

    def test_segment_list_eq(self):
        a = [_Region(x, x + 1) for x in range(1, 3, 2)]
        b = [_Region(x, x + 1) for x in range(1, 3, 2)]
        self.assertTrue(list_eq(a, b))

    def test_segment_list_neq(self):
        a = [_Region(x, x + 1) for x in range(1, 3, 2)]
        b = [_Region(x, x + 1) for x in range(2, 3, 2)]
        self.assertFalse(list_eq(a, b))

    def test_segment_list_neq2(self):
        a = [_Region(x, x + 1) for x in range(1, 3, 2)]
        b = [_Region(x, x + 1) for x in range(1 + 1, 3 + 1, 2)]
        self.assertFalse(list_eq(a, b))

    def test_segment_1_2(self):
        o = _Region(1, 2)
        self.assertEqual(o.fr, 1)
        self.assertEqual(o.ln, 2)
        self.assertEqual(o.to, 2)

    def test_low_out(self):
        ref = _Region(100, 200)
        o = _Region(10, 10)
        self.assertTrue(ref.nooverlap(o))
        self.assertTrue(ref.noclash(o.fr, o.ln))
        self.assertFalse(ref.overlap(o))

    def test_low_bound(self):
        ref = _Region(100, 200)
        o = _Region(300, 10)
        self.assertTrue(ref.nooverlap(o))
        self.assertTrue(ref.noclash(o.fr, o.ln))
        self.assertFalse(ref.overlap(o))

    def test_high_out(self):
        ref = _Region(100, 200)
        o = _Region(400, 10)
        self.assertTrue(ref.nooverlap(o))
        self.assertTrue(ref.noclash(o.fr, o.ln))
        self.assertFalse(ref.overlap(o))
        self.assertFalse(ref.clash(o.fr, o.ln))

    def test_high_bound(self):
        ref = _Region(100, 200)
        o = _Region(300, 10)
        self.assertTrue(ref.nooverlap(o))
        self.assertTrue(ref.noclash(o.fr, o.ln))
        self.assertFalse(ref.overlap(o))
        self.assertFalse(ref.clash(o.fr, o.ln))

    def test_low_overlap(self):
        ref = _Region(100, 200)
        o = _Region(95, 10)
        self.assertFalse(ref.nooverlap(o))
        self.assertFalse(ref.noclash(o.fr, o.ln))
        self.assertTrue(ref.overlap(o))
        self.assertTrue(ref.clash(o.fr, o.ln))

    def test_high_overlap(self):
        ref = _Region(100, 200)
        o = _Region(295, 10)
        self.assertFalse(ref.nooverlap(o))
        self.assertFalse(ref.noclash(o.fr, o.ln))
        self.assertTrue(ref.overlap(o))
        self.assertTrue(ref.clash(o.fr, o.ln))

    def test_full_overlap(self):
        ref = _Region(100, 200)
        o = _Region(150, 10)
        self.assertFalse(ref.nooverlap(o))
        self.assertFalse(ref.noclash(o.fr, o.ln))
        self.assertTrue(ref.overlap(o))
        self.assertTrue(ref.clash(o.fr, o.ln))
