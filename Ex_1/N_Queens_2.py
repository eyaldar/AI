def under_attack(row, column, existing_queens):
    if not len(existing_queens): return False # if no queens - not under attack
    for queen in existing_queens:
        if not len(queen):
            continue
        r,c = queen
        if r == row: return True # Check row
        if c == column: return True # Check column
        if (column-c) == (row-r): return True # Check left diagonal
        if (column-c) == -(row-r): return True # Check right diagonal
    return False # not under attack

def iter_solve(n):
    solutions = None
    for row in range(1, n+1):
        # for each row, check all valid column
        solutions = check(solutions, row, n)
    return solutions

def check(solutions, row, n):
    new_solutions = []
    for column in range(1, n+1):
        if not solutions or not len(solutions): # if null or empty
            new_solutions.append([(row, column)])
            # new_solutions.append([] + [(row, column)])
        else:
            for solution in solutions:
                if not under_attack(row, column, solution):
                    new_solutions.append(solution + [(row, column)])
    return new_solutions

BOARD_SIZE = 8
# print the first solution
print(iter_solve(BOARD_SIZE)[0])