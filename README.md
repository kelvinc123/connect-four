# Connect Four

Python implementation of connect four.

### Requirement
processing 3

### Config
see connect_four.pyde
```
SIZE = (6, 7)
CHIP_RAD = 100
THICKNESS = 15
ANIMATION_SPEED = 5
WIN_OPT = 4
AI = True
CONFIG = {
    "ONE_PLAYER_LEVEL": 4,
    "AI_COLOR": "YELLOW",
    "AI_VS_AI": False,
    "AI_RED_LEVEL": 2,
    "AI_YELLOW_LEVEL": 4
}
```

### AI
There are 4 AI levels, all implemented using **minimax** algorithm:

 * Level 1: Minimax depth = 1, score = {}
 * Level 2: Minimax depth = 1, score = {4 colors: 10000, 3 enemy colors: -100}
 * Level 3: Minimax depth = 1, score = {3 colors: 10, 4 colors: 10000, 3 enemy colors: -100}
 * Level 4: Minimax depth = 3, score = {3 colors: 10, 4 colors: 100000, 3 enemy colors: -100, 4 enemy colors: -10000}
