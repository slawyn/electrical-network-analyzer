import datetime
import os


def log(s):
    print("%s ## %s" % (datetime.datetime.now().time(), s))


def cmp(a, b):
    return (a > b) - (a < b)


def readfile(filepath):
    lines = None
    with open(filepath) as f:
        lines = f.readlines()

    return lines


def getfilename(filepath):
    base = os.path.basename(filepath)
    return os.path.splitext(base)[0]
