
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


# pyfdlock - python file lock

secure and comfortable locking file regions

features:
    
- tracks already locked regions
  - checks overlapping regions
- with context manager included
  - automatic unlocking
- custom locking backends (currently Linux only)
- 


# how to use

refer to [`sample.py`](https://github.com/kr-g/pyfdlock/blob/main/sample.py)


# Platform

Tested on Python3, and Linux.


# Development status

alpha state.
the API or logical call flow might change without prior notice.

read [`CHANGELOG`](https://github.com/kr-g/pyfdlock/blob/master/CHANGELOG.MD)
for latest, or upcoming news.


# installation
    
available on pypi. install with:

    python3 -m pip install pyfdlock
    
