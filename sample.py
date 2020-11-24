import os
import tempfile

from pyfdlock.lock import FileLock


fd = tempfile.TemporaryFile()
teststr = "some-test-stuff".encode()
fd.write(teststr)
fd.seek(0)

with FileLock(fd) as fdl:

    # lock one region
    fdl.flock(1, 10)
    print("after 1 region", fdl)

    # release the region above
    fdl.flock(1, 10, False)
    print("after 1 region unlock", fdl)

    pid = os.getpid()
    print("pid", pid)

    fdl.pid()
    print("lock pid", fdl)
    fdl.pid(False)
    print("unlock pid", fdl)

    # block the whole file
    fdl.block()
    print("all blocked", fdl)

# here all locks are released
print("end state", fdl)
