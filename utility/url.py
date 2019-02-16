import os
import re

def get_relative_steps(targetDirName, path):
    """Returns the number of steps back up the given path it takes to get to the given target directory name"""
    steps = re.split('/|\\\\', os.path.normpath(path))
    stepCount = 0;
    count = len(steps) - 1

    for step in steps:
        if step == targetDirName:
            return count - stepCount
        stepCount += 1
    return -1

def get_relative_url_stepped(steps):
    """Returns the 'move up' segment for a url for the given number of times"""
    url = ''
    for step in range(0,steps):
        url = '../' + url
    return url
