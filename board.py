'''
Name : Kelvin Christian
Github : student-KelvinChristian
'''

from chip import Chip


class Board:

    def __init__(self, SPACE, SIZE, CHIP_RAD, BORDER_THICKNESS, WIN_OPT):
        self.BORDER_THICKNESS = BORDER_THICKNESS
        self.size = SIZE
        self.space = SPACE
        self.chip_rad = CHIP_RAD
        self.board = [["NA"] * self.size[1] for i in range(self.size[0])]
        self.next_chip = Chip("RED", self.chip_rad)
        self.win_opt = WIN_OPT

    def display_board(self):

        '''
        Display all the chips with the border
        '''

        # display all chips in the board
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.board[i][j] != "NA":
                    self.board[i][j].display()

        # display border
        fill(0, 0, 0.8)
        for i in range(self.size[0] + 1):
            x_hor = 0
            y_hor = (i + 1) * self.chip_rad - (self.BORDER_THICKNESS / 2)
            rect(x_hor, y_hor, self.space['w'], self.BORDER_THICKNESS)

        for j in range(self.size[1] + 1):
            x_ver = j * self.chip_rad - (self.BORDER_THICKNESS / 2)
            y_ver = self.chip_rad - (self.BORDER_THICKNESS / 2)
            rect(x_ver, y_ver, self.BORDER_THICKNESS, self.space['h'])

    def simplify_board(self):
        '''
        Get the string representation of all chips in the board
        '''
        new_board = [["NA"] * self.size[1] for i in range(self.size[0])]
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                slot_val = self.board[i][j]
                if slot_val != "NA":
                    new_board[i][j] = slot_val.color
                else:
                    new_board[i][j] = "NA"

        return new_board

    def change_turn(self):
        '''
        Method to change next chip color
        '''
        if self.next_chip.color == "RED":
            self.next_chip = Chip("YELLOW", self.chip_rad)
        else:
            self.next_chip = Chip("RED", self.chip_rad)

    def add_chip(self, row, col):
        '''
        Method to add chip to the board
        '''
        self.next_chip.x_pos = (col + 0.5) * self.chip_rad
        self.next_chip.y_pos = (self.size[0] - row + 0.5) * self.chip_rad
        self.board[row][col] = self.next_chip

    @property
    def is_win(self):
        '''
        Method to check if there is a winner

        return boolean value
        '''

        # check horizontal
        for row in range(self.size[0]):
            for col in range(self.size[1] - self.win_opt + 1):
                if self.check_consecutive(row, col, r_inc=0, c_inc=1):
                    return True

        # check vertical
        for row in range(self.size[0] - self.win_opt + 1):
            for col in range(self.size[1]):
                if self.check_consecutive(row, col, r_inc=1, c_inc=0):
                    return True

        # check diagonal up-right
        for row in range(self.size[0] - self.win_opt + 1):
            for col in range(self.size[1] - self.win_opt + 1):
                if self.check_consecutive(row, col, r_inc=1, c_inc=1):
                    return True

        # check for diagonal up-left
        for row in range(self.size[0] - self.win_opt + 1):
            for col in range((self.win_opt - 1), self.size[1]):
                if self.check_consecutive(row, col, r_inc=1, c_inc=-1):
                    return True

        return False

    @property
    def is_draw(self):
        '''
        Method to check if the board is full

        return boolean value
        '''
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                if self.board[row][col] == "NA":
                    return False

        return True

    def check_consecutive(self, row, col, r_inc=1, c_inc=1):
        '''
        Method to check consecutive chips

        Given a row, columns, and their increments. Check
        for their colors. Returns True if there are four
        consecutive chips with the same color.

        Input:
            row: row for the last player turn (type: int)
            col: column for the last player turn (type: int)
            r_inc: 1, 0, -1 (type: int)
            c_inc: 1, 0, -1 (type: int)

        Output:
            Boolean value (True of False)
        '''

        # get the subset of board to check
        sub_list = [
            self.board[row + (r_inc * i)][col + (c_inc * i)]
            for i in range(self.win_opt)
        ]

        # check if the color for the chips in the subset are the same
        vec = [
            chip.color == self.next_chip.color
            for chip in sub_list if chip != "NA"
        ]

        return sum(vec) == self.win_opt

    def display_winner(self, who):
        FONT_THICKNESS = 5
        fill(0)
        textSize(self.chip_rad * 0.6)
        textAlign(LEFT)
        for i in range(-1 * FONT_THICKNESS, FONT_THICKNESS + 1):
            text(who + " WINS", (self.space['w'] / 3) + i, self.space['h'] / 2)
            text(who + " WINS", self.space['w'] / 3, (self.space['h'] / 2) + i)
        fill(1)
        text(who + " WINS", self.space['w'] / 3, self.space['h'] / 2)

    def display_draw(self):
        FONT_THICKNESS = 5
        fill(0)
        textSize(self.chip_rad * 0.6)
        textAlign(LEFT)
        for i in range(-1 * FONT_THICKNESS, FONT_THICKNESS + 1):
            text("DRAW", (self.space['w'] / 3) + i, self.space['h'] / 2)
            text("DRAW", self.space['w'] / 3, (self.space['h'] / 2) + i)
        fill(1)
        text("DRAW", self.space['w'] / 3, self.space['h'] / 2)
