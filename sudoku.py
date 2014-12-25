def make_assert(assertion):
    return "ASSERT(" + assertion + ");"


def make_booleans(bools):
    return ", ".join([bool for bool in bools]) + " : BOOLEAN;"


class SudokuBoard:
    def __init__(self):
        # initialize each grid to given values; 0 represents empty
        self.grids = [SudokuGrid([0] * 8 + [1],                 (0, 0)),
                      SudokuGrid([0] * 5 + [3, 0, 2, 0],        (1, 0)),
                      SudokuGrid([0] * 4 + [8, 5] + [0] * 3,    (2, 0)),
                      SudokuGrid([0] * 5 + [4, 0, 9, 0],        (0, 1)),
                      SudokuGrid([5, 0, 7] + [0] * 6,           (1, 1)),
                      SudokuGrid([0] * 3 + [1] + [0] * 5,       (2, 1)),
                      SudokuGrid([5] + [0] * 4 + [2] + [0] * 3, (0, 2)),
                      SudokuGrid([0] * 4 + [1, 0, 0, 4, 0],     (1, 2)),
                      SudokuGrid([0, 7, 3] + [0] * 5 + [9],     (2, 2))]


class SudokuGrid:
    def __init__(self, cells=[0]*9, coords=(0, 0)):
        self.cells = cells
        self.offset_x = coords[0] * 3
        self.offset_y = coords[1] * 3

    # prints assert statements given the properties of numbers in each grid
    def make_asserts(self):
        for cell in self.get_bools():
            for cell_bool in cell:
                print make_assert(
                    cell_bool + " <=> (" +
                    " AND ".join(["NOT(" + other_bool + ")"
                    for other_bool in cell if other_bool != cell_bool]) + ")")
                num = int(cell_bool[-1])
                same_num_grid_bools = self.get_bools(num)
                print make_assert(
                    cell_bool + " <=> (" +
                    " AND ".join(["NOT(" + other_bool + ")"
                    for other_bool in same_num_grid_bools if other_bool != cell_bool]) + ")")

        # assert given values
        for i, cell in enumerate(self.cells):
            if cell != 0:
                x = self.offset_x + (i % 3)
                y = self.offset_y + (i / 3)
                print make_assert(get_cell_bool(x, y, cell))

    # returns a list of 9 boolean variables for each of the 9 cells in the grid
    def get_bools(self, specific_num=0):
        for x in range(3):
            for y in range(3):
                actual_x = x + self.offset_x
                actual_y = y + self.offset_y
                if specific_num > 0:
                    yield get_cell_bool(actual_x, actual_y, specific_num)
                else:
                    yield([get_cell_bool(actual_x, actual_y, n)for n in range(1, 10)])


# gives the string encoding for the boolean variable representing a number at a given cell
def get_cell_bool(x, y, n):
    return 'x' + str(x) + 'y' + str(y) + 'n' + str(n)


# booleans for each possible value 1-9 for each cell x{1-9}y{1-9}
for x in range(9):
    for y in range(9):
        x_y_booleans = []
        for n in range(1, 10):
            x_y_booleans.append(get_cell_bool(x, y, n))
        print make_booleans(x_y_booleans)

# constraints of each grid, i.e., 1) each cell can only have one value, and 2) no two cells can have the same value
board = SudokuBoard()
for grid in board.grids:
    grid.make_asserts()

for x in range(9):
    for y in range(9):
        for n in range(1, 10):
            x_y_n = get_cell_bool(x, y, n)
            print make_assert(x_y_n + " <=> (" + " AND ".join(["NOT(" + get_cell_bool(x1, y, n) + ")"
                                                               for x1 in range(9) if x1 != x]) + ")")
            print make_assert(x_y_n + " <=> (" + " AND ".join(["NOT(" + get_cell_bool(x, y1, n) + ")"
                                                               for y1 in range(9) if y1 != y]) + ")")
