#!/usr/bin/env python

def back(path, n):
    if reject(path):
        return None
    if is_solution(path, n):
        return path
    for brother in make_brothers(path, n):
        if len(path) < n:
            new_path = back(brother, n)
            if new_path:
                return new_path
    return None


def is_solution(path, n):
    return len(path) >= n


def make_brothers(path, n):
    path = path + [0]
    while path[len(path) - 1] < n:
        yield path
        path[len(path) - 1] += 1


def reject(path):
    t = False
    for i in range(len(path)):
        for j in range(i + 1, len(path)):
            # checks if any two queens are on the same diagonal or same row
            if abs((path[j] - path[i]) * 1.0 / (j - i)) == 1 or path[j] == path[i]:
                return True

    return t


# MAIN
import time

for i in range(4, 31, 2):
    start_time = time.time()
    print 'N =', i
    print 'solution: ', back([], i)
    print time.time() - start_time, "seconds"
    print '----'
