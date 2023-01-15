import argparse
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument('start', type=str,
                    help="file containing the starting state of the sudoku.")


def parse_file_element(val: str):
    if val.isdigit():
        return int(val)
    else:
        return 0


def parse_sudoku_file(file_path: str, divider: str = ' '):
    board = []
    with open(file_path, 'r') as f:
        for line in f:
            if len(line) < 9:
                continue
            row = [parse_file_element(val) for val in line.strip().split(divider)]
            assert len(row) == 9, 'Every row on the sudoku should have 9 elements.'
            board.append(row)
    return board


class Cell():

    def __init__(self, value: int, row: int, col: int) -> None:
        assert value >= 0 and value <= 9, "Value must be between 0 and 9. 0 represents empty."
        self.value = value
        self.row = row
        self.col = col
        if self.value == 0:
            self.possible_values = set(range(1, 10))
        self.groups = {}

    @property
    def is_set(self):
        """ Whether the value is known or not. """
        return self.value > 0

    def set(self, value):
        self.value = value
        self.update_groups()

    def add_group(self, group):
        self.groups[group.kind] = group

    def update_groups(self):
        for group in self.groups.values():
            group.update(self)

    def remove_option(self, option):
        # Only update if 
        if self.value == 0:
            self.possible_values.discard(option)
            # If there is only one option left, set the cell to the remaining number.
            if len(self.possible_values) == 1:
                self.set(list(self.possible_values)[0])

    def remove_group_known(self, values):
        if self.value == 0:
            self.possible_values.difference_update(values)
            # If there is only one option left, set the cell to the remaining number.
            if len(self.possible_values) == 1:
                self.set(list(self.possible_values)[0])
    
    def __str__(self) -> str:
        if self.value == 0:
            return '_'
        return str(self.value)


class Group():
    """ Represents a group of 9 cells in sudoku which constrain each other, that is
        a row, a column or one of the 9 3x3 quadrants."""

    def __init__(self, cells: Cell, kind: str) -> None:
        assert len(cells) == 9, "There must be 9 cells in a group."
        self.cells = cells
        self.kind = kind
        self.known = set()
        self.unkown = set(range(1, 10))
        for cell in self.cells:
            cell.add_group(self)
            if cell.is_set:
                self.known.add(cell.value)
                self.unkown.discard(cell.value)
        # Remove options based on what is set in this group
        self.update_all()
    
    def update(self, cell):
        """ Call when a cell is set. Update all cells in group based on the new cell value. """
        assert cell in self.cells, "The cell does not appear to be in this group."
        value = cell.value
        self.known.add(value)
        self.known.discard(value)
        # Remove the value as an option from all cells in group.
        for other_cell in self.cells:
            if not other_cell.is_set:
                other_cell.remove_option(value)

    def update_all(self):
        """ Remove all values that are already set in the group from the 
            options of the cells that aren't set."""
        for cell in self.cells:
            cell.remove_group_known(self.known)

    def find_cell_options(self, cell):
        """ Check if there is a number in the group, that can only be in one cell. """
        pass


class SudokuBoard():

    def __init__(self, start):
        # Build the board with the start values
        self.board = []
        for i in range(9):
            row = []
            for j in range(9):
                cell = Cell(start[i][j], i, j)
                row.append(cell)
            self.board.append(row)
        # Make groups (this will autocomplete some of the board)
        self.groups = self.make_groups()

    def make_groups(self):
        all_groups = []
        # Group for each 3x3 quadrant
        for row_range in [(0,3), (3, 6), (6, 9)]:
            for col_range in [(0,3), (3, 6), (6, 9)]:
                group_cells = []
                for i in range(*row_range):
                    for j in range(*col_range):
                        group_cells.append(self.board[i][j])
                group = Group(group_cells, 'block')
                all_groups.append(group)
        # Group for each row
        for row in range(9):
            group_cells = self.board[row]
            group = Group(group_cells, 'row')
            all_groups.append(group)
        # Group for each column
        for col in range(9):
            group_cells = [self.board[i][col] for i in range(9)]
            group = Group(group_cells, 'column')
            all_groups.append(group)
        return all_groups

    def solve(self):
        raise NotImplementedError

    def __str__(self):
        string_board = ''
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if j in [3, 6]:
                    string_board = string_board + ' |'
                string_board = string_board + ' ' + str(cell)
            string_board = string_board + '\n'
            if i in [2, 5]:
                string_board = string_board + '-' * 22 + '\n'
        return string_board
            


if __name__=='__main__':
    args = parser.parse_args()
    starting_point = parse_sudoku_file(args.start)
    # 
    # for row in starting_point:
    #     print(row)
    # 
    sudoku = SudokuBoard(starting_point)
    print(sudoku)