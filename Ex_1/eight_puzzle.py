# matrices representing the start state of the puzzle
_first_start_state = [[4, 7, 8],
                      [6, 3, 2],
                      [0, 5, 1]]

_second_start_state = [[1, 4, 7],
                      [2, 5, 8],
                      [3, 6, 0]]

_third_start_state = [[8, 3, 5],
                      [1, 0, 2],
                      [6, 7, 4]]


_states_to_solve = [_first_start_state, _second_start_state, _third_start_state]

# A matrix representing the goal (final) state of the puzzle
_goal_state = [[1, 2, 3],
               [8, 0, 4],
               [7, 6, 5]]

# A mapping for each tile as represented in the goal state
_goal_state_mapping = {1: 0, 2: 1, 3: 2,
                       8: 3, 0: 4, 4: 5,
                       7: 6, 6: 7, 5: 8}


def get_inversions_num(state_arr):
    inversions_num = 0

    return inversions_num


def index(item, seq):
    """Helper function that returns -1 for non-found index value of a seq"""
    if item in seq:
        return seq.index(item)
    else:
        return -1


# A class representing the puzzle`s tiles state
class EightPuzzle:
    def __init__(self, start_state):
        # heuristic value
        self._h_val = 0
        # search depth of current instance
        self._depth = 0
        # parent node in search path
        self._parent = None
        self.adj_matrix = []
        for i in xrange(3):
            self.adj_matrix.append(start_state[i][:])

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.adj_matrix == other.adj_matrix

    def __str__(self):
        res = ''
        for row in xrange(3):
            res += ' '.join(map(str, self.adj_matrix[row]))
            res += '\r\n'
        return res

    def _clone(self):
        p = EightPuzzle(self.adj_matrix)
        return p

    def _get_legal_moves(self):
        """Returns list of tuples with which the free space may
        be swapped"""
        # get row and column of the empty piece
        row, col = self.find(0)
        free = []

        # find which pieces can move there
        if row > 0:
            free.append((row - 1, col))
        if col > 0:
            free.append((row, col - 1))
        if row < 2:
            free.append((row + 1, col))
        if col < 2:
            free.append((row, col + 1))

        return free

    def is_solvable(self):
        arr = []
        for row in self.adj_matrix:
            arr += row

        inversion_num = get_inversions_num(arr)

        return inversion_num % 2 == 1

    def _generate_moves(self):
        free = self._get_legal_moves()
        zero = self.find(0)

        def swap_and_clone(a, b):
            p = self._clone()
            p.swap(a, b)
            p._depth = self._depth + 1
            p._parent = self
            return p

        return map(lambda pair: swap_and_clone(zero, pair), free)

    def _generate_solution_path(self, path):
        if self._parent is None:
            return path
        else:
            path.append(self)
            return self._parent._generate_solution_path(path)

    def solve(self, h):
        """Performs A* search for goal state.
        h(puzzle) - heuristic function, returns an integer
        """

        def is_solved(puzzle):
            return puzzle.adj_matrix == _goal_state

        opened_states = [self]
        closed_states = []
        move_count = 0
        while len(opened_states) > 0:
            x = opened_states.pop(0)
            move_count += 1
            if is_solved(x):
                if len(closed_states) > 0:
                    return x._generate_solution_path([]), move_count
                else:
                    return [x]

            son_states = x._generate_moves()
            idx_open = idx_closed = -1
            for move in son_states:
                # have we already seen this node?
                idx_open = index(move, opened_states)
                idx_closed = index(move, closed_states)
                h_val = h(move)
                f_val = h_val + move._depth

                if idx_closed == -1 and idx_open == -1:
                    move._h_val = h_val
                    opened_states.append(move)
                elif idx_open > -1:
                    copy = opened_states[idx_open]
                    if f_val < copy._h_val + copy._depth:
                        # copy the move values over existing
                        copy._h_val = h_val
                        copy._parent = move._parent
                        copy._depth = move._depth
                elif idx_closed > -1:
                    copy = closed_states[idx_closed]
                    if f_val < copy._h_val + copy._depth:
                        move._h_val = h_val
                        closed_states.remove(copy)
                        opened_states.append(move)

            closed_states.append(x)
            opened_states = sorted(opened_states, key=lambda p: p._h_val + p._depth)

        # if finished state not found, return failure
        return [], 0

    def find(self, value):
        """returns the row, col coordinates of the specified value
           in the graph"""
        if value < 0 or value > 8:
            raise Exception("value out of range")

        for row in xrange(3):
            for col in xrange(3):
                if self.adj_matrix[row][col] == value:
                    return row, col

    def peek(self, row, col):
        """returns the value at the specified row and column"""
        return self.adj_matrix[row][col]

    def poke(self, row, col, value):
        """sets the value at the specified row and column"""
        self.adj_matrix[row][col] = value

    def swap(self, pos_a, pos_b):
        """swaps values at the specified coordinates"""
        temp = self.peek(*pos_a)
        self.poke(pos_a[0], pos_a[1], self.peek(*pos_b))
        self.poke(pos_b[0], pos_b[1], temp)


# Manhattan heuristic function for the 8-puzzle game
def manhattan_heuristic(puzzle_state):
    heuristic_val = 0

    for row in xrange(3):
        for col in xrange(3):
            tile_value = puzzle_state.peek(row, col)
            tile_destination = _goal_state_mapping[tile_value]
            target_col = tile_destination % 3
            target_row = tile_destination / 3

            # Calc the Manhattan Distance of current tile and add it to the h val
            heuristic_val += abs(target_row - row) + abs(target_col - col)

    return heuristic_val


def main():

    puzzles_to_solve = [EightPuzzle(start_state) for start_state in _states_to_solve]

    for eight_puzzle in puzzles_to_solve:
        print eight_puzzle

        if eight_puzzle.is_solvable():
            print "state is not solvable!"

        path, count = eight_puzzle.solve(manhattan_heuristic)
        path.reverse()

        for i in path:
            print i

        print "Solved with Manhattan distance exploring", count, "states"

if __name__ == "__main__":
    main()