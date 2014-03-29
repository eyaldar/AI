#!/usr/bin/env python

BOARD_SIZE = 8


def back(path):
    if reject(path):
        return None
    if is_solution(path):
        print path
    for brother in make_brothers(path):
        if len(path) < BOARD_SIZE:
            new_path = back(brother)
            if new_path:
                return new_path
    return None


def is_solution(path):
    return len(path) >= BOARD_SIZE


def make_brothers(path):
    path = path + [0]
    while path[len(path) - 1] < BOARD_SIZE:
        yield path
        path[len(path) - 1] += 1


def reject(path):
    t = False
    for i in range(len(path)):
        for j in range(i + 1, len(path)):
            if abs((path[j] - path[i]) * 1.0 / (j - i)) == 1 or path[j] == path[i]:
                return True

    return t


back([])