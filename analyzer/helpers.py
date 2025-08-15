import datetime
import os

'''
Log function
'''
def log(s):
    print("%s ## %s"%(datetime.datetime.now().time(),s))

'''
String Compare function
'''
def cmp(a, b):
    return (a > b) - (a < b)

'''
Read file into a buffer of lines
'''
def readfile(filepath):
    lines = None
    with open(filepath) as f:
        lines = f.readlines()

    return lines

'''
Get name of the file from the filepath
'''
def getfilename(filepath):
    base=os.path.basename(filepath)
    return os.path.splitext(base)[0]
