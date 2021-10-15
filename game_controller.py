'''
Name : Kelvin Christian
Github : student-KelvinChristian
'''

from chip import Chip
from board import Board
from ai import Ai
import os


class GameController:

    def __init__(self, SPACE, CHIP_RAD, SIZE,
                 ANIMATION_SPEED, THICK,
                 USE_AI, CONFIG, WIN_OPT=4):
        self.SIZE = SIZE
        self.SPACE = SPACE
        self.CHIP_RAD = CHIP_RAD
        self.ANIMATION_SPEED = ANIMATION_SPEED
        self.AI = USE_AI
        self.WIN_OPT = WIN_OPT

        # attributes for gameplay logic
        self.board = Board(self.SPACE, self.SIZE, self.CHIP_RAD,
                           THICK, self.WIN_OPT)
        self.game_over = False
        self.winner = None
        self.draw = False
        self.ai_turn = False

        # set up the AI
        self.AI_VS_AI = CONFIG["AI_VS_AI"]
        if self.AI:

            if not self.AI_VS_AI:
                self.ai_machine = Ai(
                    CONFIG["AI_COLOR"].upper(), self.SIZE, self.WIN_OPT,
                    CONFIG["ONE_PLAYER_LEVEL"]
                )
                self.wait_time = 35
            else:
                self.ai_machine_red = Ai(
                    "RED", self.SIZE, self.WIN_OPT,
                    CONFIG["AI_RED_LEVEL"]
                )
                self.ai_machine_yellow = Ai(
                    "YELLOW", self.SIZE, self.WIN_OPT,
                    CONFIG["AI_YELLOW_LEVEL"]
                )
                self.wait_time = 0

        # attributes for adding chip to the board only
        self.next_row = None
        self.next_col = None

        # attributes for animation purposes
        self.animated = False
        self.y_dest = None

    def update(self):

        # check if the game is still played
        if not self.game_over:

            # check if ai is activated
            if self.AI:

                # check if the game is ai vs ai
                if self.AI_VS_AI:
                    self.ai_turn = True
                elif self.board.next_chip.color == self.ai_machine.color:
                    self.ai_turn = True

            # if animated, can't do other things
            if self.animated:
                self.handle_animated_and_add_chip()

            # if not animated and it's ai turn
            elif self.ai_turn:

                # waiting time for ai (delay the moves)
                if self.wait_time > 0:
                    self.wait_time -= 1

                # ai moves for one player game
                elif not self.AI_VS_AI:
                    move_row, move_col = self.ai_machine.analyze(
                        self.board.simplify_board()
                    )
                    self.handle_each_turn(move_row, move_col)
                    self.wait_time = 40  # reset wait time

                # ai moves for computer vs computer
                else:
                    if self.board.next_chip.color == "RED":
                        move_row, move_col = self.ai_machine_red.analyze(
                            self.board.simplify_board()
                        )
                    else:
                        move_row, move_col = self.ai_machine_yellow.analyze(
                            self.board.simplify_board()
                        )
                    self.handle_each_turn(move_row, move_col)

            # if not ai turn, view all choices by pressing the mouse button
            elif mousePressed:
                if mouseY < self.CHIP_RAD and 0 < mouseX < self.SPACE['w']:
                    self.handle_mousepressed()

            # draw the border
            self.board.display_board()

        # if it's game over and the result is draw (all chips on the board)
        elif self.draw:
            self.board.display_board()
            self.board.display_draw()

        else:
            self.board.display_board()
            self.board.display_winner(self.winner)

    def handle_mousereleased(self):
        '''
        Method to handle mouse released for player's turn and
        get the chip position in terms of row and column.
        This position will be passed to the handle_each_turn
        function.
        '''

        if not self.game_over and not self.animated and not self.AI_VS_AI:

            next_color = self.board.next_chip.color
            if not self.AI or next_color != self.ai_machine.color:

                move_col = mouseX // self.CHIP_RAD
                # check if the last slot is not filled yet
                if self.board.board[self.SIZE[0] - 1][move_col] == "NA":

                    # find where to put the next chip
                    move_row = 0
                    for i in range(self.SIZE[0]-1, 0, -1):

                        # if the row below it has filled, assign current row
                        if self.board.board[i-1][move_col] != "NA":
                            move_row = i
                            break

                    self.handle_each_turn(move_row, move_col)

    def handle_mousepressed(self):
        '''
        Method to view choices for player
        '''
        if not self.game_over and not self.animated and not self.AI_VS_AI:

            next_color = self.board.next_chip.color
            if not self.AI or next_color != self.ai_machine.color:

                move_col = mouseX // self.CHIP_RAD
                # check if the last slot is not filled yet
                if self.board.board[self.SIZE[0] - 1][move_col] == "NA":

                    # display choices
                    self.board.next_chip.display(
                        x=int((move_col + 0.5) * self.CHIP_RAD),
                        y=int(0.5 * self.CHIP_RAD)
                    )

    def handle_each_turn(self, move_row, move_col):
        '''
        Method to handle each turn for any player / AI
        set the attributes needed for animation and adding chip
        to the board
        '''

        # stored value of which row and col to the attributes
        self.next_row = move_row
        self.next_col = move_col

        # initialize position for the chip for animating (top row)
        self.board.next_chip.x_pos = int(
            (move_col + 0.5) * self.CHIP_RAD
        )
        self.board.next_chip.y_pos = int(0.5 * self.CHIP_RAD)
        self.y_dest = int((self.SIZE[0] - move_row + 0.5) * self.CHIP_RAD)

        # start animated
        self.animated = True

    def handle_animated_and_add_chip(self):
        '''
        Method to animate chip falling down and add chip to board
        after choosing which column for the chip. This method also
        check for the winner
        '''
        y_pos = self.board.next_chip.y_pos
        # check if the chip has reach its destination
        if y_pos >= self.y_dest:

            # add chip to the board
            self.board.add_chip(self.next_row, self.next_col)

            # check if adding the chip resulting in winning the game
            if self.board.is_win:
                self.game_over = True
                self.winner = self.board.next_chip.color

                # the winner will be recorded if the game mode is
                # player vs computer and player wins the game
                if self.AI and not self.AI_VS_AI:
                    if self.winner != self.ai_machine.color:
                        self.record_winner()

            # check if adding the chip resulting in draw (board full)
            elif self.board.is_draw:
                self.game_over = True
                self.draw = True

            # if the game hasn't finished yet
            else:
                self.ai_turn = False
                self.board.change_turn()

            # set animated = false to go to the next turn
            self.animated = False

        # if the chip is almost reach the destination
        elif y_pos + self.board.next_chip.SPEED > self.y_dest:
            self.board.next_chip.y_pos = self.y_dest
            self.board.next_chip.display()
        else:
            # fall animation
            self.board.next_chip.display_fall(acc=self.ANIMATION_SPEED)

    def input(self, message=''):
        '''
        Input method for asking the name of the winner
        '''
        from javax.swing import JOptionPane
        return JOptionPane.showInputDialog(frame, message)

    def record_winner(self):
        '''
        Method to add the winner name and score to scores.txt
        '''

        name = self.input('Congratulations, You win the game\nEnter your name')

        # check if scores.txt is exists
        if not os.path.exists("scores.txt"):
            with open("scores.txt", "w") as f:
                pass

        # read the file
        with open("scores.txt", "r") as f:
            scores = f.read()

        # convert to list of lists of scores
        if scores != "":
            scores_dict = {
                score.split(" ")[0]: int(score.split(" ")[1])
                for score in scores.split("\n")
            }
        else:
            scores_dict = {}

        # add +1 to the dictionary
        if name in scores_dict.keys():
            scores_dict[name] += 1
        else:
            scores_dict[name] = 1

        # combine and stored to a string variable
        counter = 0
        result = ""
        for k, v in scores_dict.items():
            result += k + " " + str(v)
            counter += 1
            if counter != len(scores_dict.keys()):
                result += "\n"

        # write the scores to scores.txt
        with open("scores.txt", "w") as f:
            f.write(result)
