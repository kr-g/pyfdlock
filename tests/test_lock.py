import os

import unittest
import tempfile

from tests.test_func import eq, list_eq

from pyfdlock.lock import *
from pyfdlock.lock import _Region


class LockTestCase(unittest.TestCase):
    def setUp(self):
        self.fd = tempfile.TemporaryFile()
        self.teststr = "some-test-stuff".encode()
        self.fd.write(self.teststr)
        self.fd.seek(0)

    def tearDown(self):
        self.fd.seek(0)
        readstr = self.fd.read()
        self.assertTrue(self.teststr == readstr)
        self.fd.close()

    def test_setup(self):
        self.assertTrue(True)

    def test_no_locks(self):
        with FileLock(self.fd) as fdl:
            self.assertTrue(list_eq([], fdl._regions))

    def test_block(self):
        with FileLock(self.fd) as fdl:
            fdl.block()
            self.assertTrue(len(fdl._regions) == 1)
            self.assertTrue(list_eq([_Region(0, 0)], fdl._regions))

    def test_unblock(self):
        with FileLock(self.fd) as fdl:
            fdl.block()
            fdl.block(False)
            self.assertTrue(len(fdl._regions) == 0)
            self.assertTrue(list_eq([], fdl._regions))

    def test_rollb(self):
        with FileLock(self.fd) as fdl:
            fdl.block()
            fdl.rollb()
            self.assertTrue(len(fdl._regions) == 0)

    def test_auto_rollb(self):
        with FileLock(self.fd) as fdl:
            fdl.block()
        self.assertTrue(len(fdl._regions) == 0)

    def test_pid(self):
        with FileLock(self.fd) as fdl:
            pid = os.getpid()
            fdl.pid()
            self.assertTrue(len(fdl._regions) == 1)
            self.assertTrue(list_eq([_Region(pid, 1)], fdl._regions))
            fdl.pid(False)
            self.assertTrue(list_eq([], fdl._regions))

    def test_regions_insize(self):
        with FileLock(self.fd) as fdl:
            fdl.flock(0, 2)
            self.assertTrue(len(fdl._regions) == 1)

    def test_regions_outsize(self):
        with FileLock(self.fd) as fdl:
            fdl.flock(100, 2)
            self.assertTrue(len(fdl._regions) == 1)

    def test_2_regions(self):
        with FileLock(self.fd) as fdl:
            fdl.flock(2, 2)
            fdl.flock(4, 2)
            self.assertTrue(len(fdl._regions) == 2)
            self.assertTrue(list_eq([_Region(2, 2), _Region(4, 2)], fdl._regions))

    def test_no_regions(self):
        with FileLock(self.fd) as fdl:
            self.assertRaises(
                NotLockedException, fdl.flock, pos=2, length=2, lock=False
            )

    def test_wrong_len_regions(self):
        with FileLock(self.fd) as fdl:
            fdl.flock(pos=2, length=2, lock=True)
            self.assertRaises(
                SegmentLengthException, fdl.flock, pos=2, length=1, lock=False
            )

    def test_overlap_regions(self):
        with FileLock(self.fd) as fdl:
            fdl.flock(pos=100, length=100, lock=True)
            self.assertRaises(OverlapException, fdl.flock, pos=50, length=100)
            self.assertRaises(OverlapException, fdl.flock, pos=110, length=10)
            self.assertRaises(OverlapException, fdl.flock, pos=150, length=100)
