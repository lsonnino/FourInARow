##############################
# General
##############################
GAME_NAME = 'Four in a Row'


##############################
# Session
##############################
TRAINING = 0
EVALUATING = 1

HUMAN_VS_HUMAN = 0
HUMAN_VS_AI = 1
AI_VS_AI = 2


##############################
# Graphics
##############################

# ----------------------------
# Gameplay
# ----------------------------

ROWS = 6
COLUMNS = 7

WINNING_MASK = [
    [
        [True, True, True, True]
    ],
    [
        [True],
        [True],
        [True],
        [True]
    ],
    [
        [True, False, False, False],
        [False, True, False, False],
        [False, False, True, False],
        [False, False, False, True]
    ],
    [
        [False, False, False, True],
        [False, False, True, False],
        [False, True, False, False],
        [True, False, False, False]
    ],
]

EMPTY_PIECE = 0
RED_PIECE = -1
BLUE_PIECE = 1

LEFT = -1
PLACE = 0
RIGHT = 1

# ----------------------------
# Window
# ----------------------------

WIN_SIZE = (1280, 720)

PIECE_RADIUS = 30
PIECE_OFFSET = 10

SELECTOR_WIDTH = 4
SELECTOR_RADIUS = 4

# ----------------------------
# Colors
# ----------------------------

BACKGROUND_COLOR = (230, 230, 240)
EMPTY_COLOR = (100, 100, 100)
RED_COLOR = (255, 59, 48)
BLUE_COLOR = (0, 122, 255)
SELECTOR_COLOR = (0, 255, 0)
TEXT_COLOR = (77, 76, 76)

# ----------------------------
# Text
# ----------------------------

FONT = "Arial"
FONT_SIZE = 20
