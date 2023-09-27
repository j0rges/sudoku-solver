# Sudoku Solver

This is a repository with a simple algorithm to solve sudokus.
It is only a small project I have made for fun. I first made a
sudoku solver script, which wasn't even able to solve hard sudokus,
when I was in secondary school and barely knew the basics of Python.
This is my solution now that I have more coding experience.

The way it works is very simple, each cell has a list of possible
values, when the length of this list is one, the cell is considered
to have its final value (it is set). When the board is parsed, or any value
is set, then these values are removed from the other cells in the same
row, column and square. 

If after doing the above, there is still cells with more than one possible
value, then it makes guesses in a Depth First Search manner until it finds
a set of guesses that lets it complete the board.


## Installation

All you need to do is clone this repository. The script doesn't
use any libraries that are not part of the Python Standard Library
(thus there is no need for a `requirements.txt` file)


## How to use

You need to follow 2 steps to solve a sudoku:

1. Create a file containing the sudoku you want to solve, see how to do so [here](### Sudoku file format)
2. Execute the solver script: `python3 solve_sudoky.py <filename>`


## Sudoku file format

The program parses plain text files with 9 lines in the following format:

- In a cell that has a number, insert the number.
- In a cell that is empty, put a `.` (dot/full stop)
- Separate the value of each cell with a whitespace
- Insert a new line after each row

For example:
```
. . . . 5 4 7 8 .
. 7 8 . 6 2 9 . .
1 . 6 8 9 7 . . .
. . 4 6 7 5 3 . 2
6 . 2 . . . 5 . 8
. 5 . 9 2 . 4 6 .
2 8 5 7 1 . . . .
. . 9 5 8 6 . . 7
7 . . 2 . . . . 3
```

There is several example files included in the repository, with different levels of difficulty:

* [easy.txt](easy.txt)
* [medium.txt](medium.txt)
* [hard.txt](hard.txt)
* [expert.txt](expert.txt)


