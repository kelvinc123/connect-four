'''
Name : Kelvin Christian
Github : student-KelvinChristian
'''

from game_controller import GameController

####################################################################
######################### gameplay options #########################
SIZE = (6, 7)  # define the size[0]xsize[1] board
CHIP_RAD = 100  # radius of each chip 
THICKNESS = 15  # board frame thickness
ANIMATION_SPEED = 5  # speed of chip falling down
WIN_OPT = 4  # number of consequence chips to win (default is 4)
AI = True  # set this to true for battle vs ai
CONFIG = {
    # player vs computer config
    "ONE_PLAYER_LEVEL": 4,  # level of AI, pick from [1,2,3,4],
    "AI_COLOR": "YELLOW",  # ["RED", "YELLOW"], red goes first
    # computer vs computer config
    "AI_VS_AI": False,  # set true for ai vs ai
    "AI_RED_LEVEL": 2,
    "AI_YELLOW_LEVEL": 4,
}
####################################################################
####################################################################

SPACE = {'w': SIZE[1] * CHIP_RAD, 'h': (SIZE[0] + 1) * CHIP_RAD}
gc = GameController(SPACE, CHIP_RAD, SIZE, 
                    ANIMATION_SPEED, THICKNESS,
                    AI, CONFIG, WIN_OPT)

def setup():
    size(SPACE['w'], SPACE['h'])
    colorMode(RGB, 1)
    noStroke()

def draw():
    background(0.75)
    gc.update()

def mouseReleased():

    if mouseY < CHIP_RAD and 0 < mouseX < SPACE['w']:
        gc.handle_mousereleased()
