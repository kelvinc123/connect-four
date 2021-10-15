'''
Name : Kelvin Christian
Github : student-KelvinChristian
'''

from board import Board
from chip import Chip


CHIP_RAD = 100
THICK = 18
WIN_OPT = 4

CHIPS = []
for i in range(10):
    CHIPS.append(Chip("YELLOW", CHIP_RAD))
    CHIPS.append(Chip("RED", CHIP_RAD))


def test_board_size():

    # empty board
    SIZE = (0, 0)
    SPACE = {'w': SIZE[1] * CHIP_RAD, 'h': (SIZE[0] + 1) * CHIP_RAD}
    board = Board(SPACE, SIZE, CHIP_RAD, THICK, WIN_OPT)
    assert board.board == []

    # 2x2 board
    SIZE = (2, 2)
    SPACE = {'w': SIZE[1] * CHIP_RAD, 'h': (SIZE[0] + 1) * CHIP_RAD}
    board = Board(SPACE, SIZE, CHIP_RAD, THICK, WIN_OPT)
    assert board.board == [["NA", "NA"], ["NA", "NA"]]

    # 4x4 board
    SIZE = (4, 4)
    SPACE = {'w': SIZE[1] * CHIP_RAD, 'h': (SIZE[0] + 1) * CHIP_RAD}
    board = Board(SPACE, SIZE, CHIP_RAD, THICK, WIN_OPT)
    assert board.board == [
        ["NA", "NA", "NA", "NA"],
        ["NA", "NA", "NA", "NA"],
        ["NA", "NA", "NA", "NA"],
        ["NA", "NA", "NA", "NA"]
    ]


def test_winning():
    SIZE = (7, 9)
    SPACE = {'w': SIZE[1] * CHIP_RAD, 'h': (SIZE[0] + 1) * CHIP_RAD}
    board = Board(SPACE, SIZE, CHIP_RAD, THICK, WIN_OPT)

    board.board[0][0] = CHIPS.pop()  # red
    board.board[0][1] = CHIPS.pop()  # yellow
    board.board[0][2] = CHIPS.pop()  # red
    board.board[0][3] = CHIPS.pop()  # yellow
    assert not board.is_win

    board.board[1][0] = CHIPS.pop()  # red
    board.board[1][1] = CHIPS.pop()  # yellow
    board.board[2][0] = CHIPS.pop()  # red
    board.board[0][4] = CHIPS.pop()  # yellow
    assert not board.is_win

    board.board[3][0] = CHIPS.pop()  # red
    assert board.is_win


def test_add_chip():
    SIZE = (2, 5)
    SPACE = {'w': SIZE[1] * CHIP_RAD, 'h': (SIZE[0] + 1) * CHIP_RAD}
    board = Board(SPACE, SIZE, CHIP_RAD, THICK, WIN_OPT)

    # add chip twice
    board.add_chip(0, 3)
    board.next_chip = Chip("YELLOW", 100)
    board.add_chip(0, 2)

    assert board.simplify_board() == [
        ["NA", "NA", "YELLOW", "RED", "NA"],
        ["NA", "NA", "NA", "NA", "NA"],
    ]
