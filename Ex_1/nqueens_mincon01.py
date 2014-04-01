import random


def n_queens(nr):
    show(min_conflicts(list(range(nr)), nr), nr)


def show(solution, nr):
    for i in range(nr):
        row = ['~'] * nr
        for col in range(nr):
            if solution[col] == nr - 1 - i:
                row[col] = 'Q'
        print(''.join(row))


def min_conflicts(solution, nr, max_iterations=1000):
    def random_pos(li, filter_func):
        return random.choice([i for i in range(nr) if filter_func(li[i])])

    for k in range(max_iterations):
        conflicts = find_conflicts(solution, nr)
        if sum(conflicts) == 0:
            return solution
        col = random_pos(conflicts, lambda elt: elt > 0)
        v_conflicts = [hits(solution, nr, col, row) for row in range(nr)]
        solution[col] = random_pos(v_conflicts, lambda elt: elt == min(v_conflicts))
    raise Exception("Incomplete solution: try more iterations.")


def find_conflicts(solution, nr):
    return [hits(solution, nr, col, solution[col]) for col in range(nr)]


def hits(solution, nr, col, row):
    total = 0
    for i in range(nr):
        if i == col:
            continue
        if solution[i] == row or abs(i - col) == abs(solution[i] - row):
            total += 1
    return total


n_queens(100)