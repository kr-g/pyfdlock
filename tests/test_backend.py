import os

import unittest
import tempfile

from tests.test_func import eq, list_eq

from pyfdlock.lock import *
from pyfdlock.lock import _Region

from pyfdlock.backend import fnctlBackend, VirtualBackend


class MockRecorderBackend(VirtualBackend):
    def __init__(self):
        self.testing_data = []

    def lockf(self, fd, pos, length):
        self.testing_data.append((fd, pos, length))

    def unlockf(self, fd, pos, length):
        self.testing_data.remove((fd, pos, length))


class BackEndTestCase(unittest.TestCase):
    def setUp(self):
        self.fd = tempfile.TemporaryFile()
        self.teststr = "some-test-stuff".encode()
        self.fd.write(self.teststr)
        self.fd.seek(0)
        self.fileno = self.fd.fileno()
        self.mockbe = MockRecorderBackend()

    def tearDown(self):
        self.fd.seek(0)
        readstr = self.fd.read()
        self.assertTrue(self.teststr == readstr)
        self.fd.close()

    def test_block(self):

        with FileLock(self.fd, backend=self.mockbe) as fdl:
            fdl.block()

            self.assertTrue(len(fdl._regions) == 1)
            self.assertTrue(list_eq([_Region(0, 0)], fdl._regions))

            self.assertTrue(len(self.mockbe.testing_data) == 1)
            self.assertEqual(self.mockbe.testing_data, [(self.fileno, 0, 0)])

        self.assertTrue(len(self.mockbe.testing_data) == 0)

    def test_2_regions(self):
        with FileLock(self.fd, backend=self.mockbe) as fdl:
            fdl.flock(2, 2)
            fdl.flock(4, 2)
            self.assertTrue(len(fdl._regions) == 2)
            self.assertTrue(list_eq([_Region(2, 2), _Region(4, 2)], fdl._regions))

            self.assertTrue(len(self.mockbe.testing_data) == 2)
            self.assertEqual(
                self.mockbe.testing_data, [(self.fileno, 2, 2), (self.fileno, 4, 2)]
            )

        self.assertTrue(len(self.mockbe.testing_data) == 0)
