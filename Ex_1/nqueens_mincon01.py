import random
import time


def n_queens(nr):
    print(min_conflicts(list(xrange(nr)), nr), nr)


def min_conflicts(solution, nr, max_iterations=1000):
    def random_pos(li, filter_func):
        return random.choice([i for i in xrange(nr) if filter_func(li[i])])

    for k in xrange(max_iterations):
        conflicts = find_conflicts(solution, nr)
        if sum(conflicts) == 0:
            return solution
        col = random_pos(conflicts, lambda elt: elt > 0)
        v_conflicts = [hits(solution, nr, col, row) for row in xrange(nr)]
        solution[col] = random_pos(v_conflicts, lambda elt: elt == min(v_conflicts))
    raise Exception("Incomplete solution: try more iterations.")


def find_conflicts(solution, nr):
    return [hits(solution, nr, col, solution[col]) for col in xrange(nr)]


def hits(solution, nr, col, row):
    total = 0
    for i in xrange(nr):
        if i == col:
            continue
        if solution[i] == row or abs(i - col) == abs(solution[i] - row):
            total += 1
    return total

# MAIN

for j in xrange(4, 101, 2):
    print 'N =', j
    start_time = time.time()
    n_queens(j)
    print time.time() - start_time, "seconds"
    print '----'
