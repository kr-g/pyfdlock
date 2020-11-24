import os
import tempfile

import traceback

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

    reg = [(10, 2), (20, 5), (30, 4)]
    fdl.regions(reg)
    print("lock regions", fdl)

    try:
        # locking the last will fail
        fdl.regions([(0, 1), (27, 2), (24, 1)])
        print("additional regions", fdl)
    except:
        print("ERR: rolled back", fdl)

    fdl.regions(reg, False)
    print("unlock regions", fdl)

    # rollback all until now locked regions
    fdl.rollb()
    print("after rollb", fdl)

    # block the whole file
    fdl.block()
    print("all blocked", fdl)

    try:
        fdl.pid()
    except Exception as ex:
        print("ERR: pid lock not possible")
        # traceback.print_exc()

# here all locks are released
print("end state", fdl)
