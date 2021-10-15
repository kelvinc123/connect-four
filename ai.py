'''
Name : Kelvin Christian
Github : student-KelvinChristian
'''

import copy
import random


class Ai:

    def __init__(self, color, board_size, win_opt, level):
        self.color = color
        self.size = board_size
        self.win_opt = win_opt

        if self.color == "RED":
            self.enemy_color = "YELLOW"
        else:
            self.enemy_color = "RED"

        self.set_level(level)

    def set_level(self, level):
        if level <= 1:
            self.score_dict = {}
            self.minimax_depth = 1
        elif level == 2:
            self.score_dict = {
                (self.color, 4): 10000,
                (self.enemy_color, 3): -100
            }
            self.minimax_depth = 1
        elif level == 3:
            self.score_dict = {
                (self.color, 3): 10,
                (self.color, 4): 10000,
                (self.enemy_color, 3): -100,
            }
            self.minimax_depth = 1
        elif level >= 4:
            self.score_dict = {
                (self.color, 3): 10,
                (self.color, 4): 100000,
                (self.enemy_color, 3): -100,
                (self.enemy_color, 4): -10000
            }
            self.minimax_depth = 3

    def analyze(self, board):
        '''
        Method to get the current board information and
        get the next best possible moves for ai

        Input:
            board: (type: list of lists of board)

        Output:
            move_row, move_col: (int, int)
        '''

        # get all possible positions (the last row must not filled yet)
        valid_positions = [
            i for i in range(self.size[1])
            if board[self.size[0] - 1][i] == "NA"
        ]

        # iterate over all possible position and get the score
        scores = []
        for position in valid_positions:

            # add chip to the new board according to the position
            new_board = self.add_chip(board, position, self.color)

            # apply minimax algorithm
            score = self.minimax(
                new_board, self.minimax_depth - 1, -1e8, 1e8, False
            )
            scores.append(score)

        # get the next positions that have maximum score
        index_max = [i for i in range(len(scores)) if scores[i] == max(scores)]

        # get the position according to the random index_max in case
        # there are more than 1 max values
        move_col = valid_positions[random.choice(index_max)]

        # get which row to put chip
        move_row = 0
        for i in range(self.size[0] - 1, 0, -1):

            # if the row below it has filled, assign current row
            if board[i-1][move_col] != "NA":
                move_row = i
                break

        return move_row, move_col

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        '''
        Minimax function to select best possible moves with
        alpha-beta pruning

        Reference : https://www.youtube.com/watch?v=l-hh51ncgDI

        Input:
            board: (type: list of lists of board)
            depth: (type: int)
            alpha: (type: int)
            beta: (type: int)
            maximizing_player: (type: bool)
        Output:
            score: (type: int)
        '''

        # check if there's a winning player
        game_over = self.get_combination(board, "RED", self.win_opt)
        game_over += self.get_combination(board, "YELLOW", self.win_opt)
        game_over = game_over > 0

        if depth == 0 or game_over:
            return self.get_score_board(board)

        # the position is valid if the topmost row is "NA"
        valid_positions = [
            i for i in range(self.size[1])
            if board[self.size[0] - 1][i] == "NA"
        ]

        if maximizing_player:
            max_eval = -1e8
            for position in valid_positions:
                new_board = self.add_chip(board, position, self.color)
                evaluation = self.minimax(
                    new_board, depth - 1, alpha, beta, False
                )
                max_eval = max(max_eval, evaluation)

                # alpha-beta pruning
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = 1e8
            for position in valid_positions:
                new_board = self.add_chip(board, position, self.enemy_color)
                evaluation = self.minimax(
                    new_board, depth - 1, alpha, beta, True
                )
                min_eval = min(min_eval, evaluation)

                # alpha-beta pruning
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return min_eval

    def add_chip(self, board, col, color):
        '''
        Method to add chip to the board according to the
        column choices
        '''

        # copy the board to prevent overwritting original board
        new_board = copy.deepcopy(board)

        for row in range(self.size[0]):
            if new_board[row][col] == "NA":
                new_board[row][col] = color
                break

        return new_board

    def get_score_board(self, board):

        total_score = 0
        for key in self.score_dict.keys():

            # check the number of combination according to key[0] and key[1]
            num_comb = self.get_combination(board, key[0], key[1])

            # multiply with the pre-defined score and add to total
            total_score += num_comb * self.score_dict[key]

        return total_score

    def get_combination(self, board, color, num_chips):
        '''
        Method to get the number of combination in the board
        according to the parameter

        Input:
            board: (type: list of lists of board)
            color: (type: str) -> color of chip that will be checked
            num_chips: (type: int) -> number of chips required in a subset
        '''
        total = 0
        # check horizontal
        for row in range(self.size[0]):
            for col in range(self.size[1] - self.win_opt + 1):
                if self.calc_consecutive(board, color, num_chips,
                                         row, col,
                                         r_inc=0, c_inc=1):
                    total += 1

        # check vertical
        for row in range(self.size[0] - self.win_opt + 1):
            for col in range(self.size[1]):
                if self.calc_consecutive(board, color, num_chips,
                                         row, col,
                                         r_inc=1, c_inc=0):
                    total += 1

        # check diagonal up-right
        for row in range(self.size[0] - self.win_opt + 1):
            for col in range(self.size[1] - self.win_opt + 1):
                if self.calc_consecutive(board, color, num_chips,
                                         row, col,
                                         r_inc=1, c_inc=1):
                    total += 1

        # check for diagonal up-left
        for row in range(self.size[0] - self.win_opt + 1):
            for col in range((self.win_opt - 1), self.size[1]):
                if self.calc_consecutive(board, color, num_chips,
                                         row, col,
                                         r_inc=1, c_inc=-1):
                    total += 1

        return total

    def calc_consecutive(self, board, color, num_chips,
                         row, col, r_inc=1, c_inc=1):
        '''
        Method to calculate consecutive chips

        Given a row, columns, their increments, color, and number of chips
        required. Check for the number of chip in the subset
        Returns True if there are a total of num of chips on that subset
        and the number of NA in the subset is win_opt - num


        Input:
            row: row for the last player turn (type: int)
            col: column for the last player turn (type: int)
            r_inc: 1, 0, -1 (type: int)
            c_inc: 1, 0, -1 (type: int)
            color: "YELLOW", "RED" (type: str)
            num: (type: int)

        Output:
            Boolean value (True of False)
        '''

        # get the subset of board to check
        sub_list = [
            board[row + (r_inc * i)][col + (c_inc * i)]
            for i in range(self.win_opt)
        ]

        # calculate the number of chips having that color
        vec = [
            chip == color for chip in sub_list
            if chip != "NA"
        ]
        condition_1 = sum(vec) == num_chips

        # calculate the number of empty slots
        na_vec = [slot == "NA" for slot in sub_list]
        condition_2 = sum(na_vec) == self.win_opt - num_chips

        return condition_1 and condition_2
