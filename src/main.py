from src.console import Console
from src.session import *
from src.constants import AI_VS_AI
from src.settings import SHOW_GRAPHICS
from src.ai_settings import min_exploration_rate, max_exploration_rate
from src import user

PLAYER_1_ACTION_REQUEST = None
PLAYER_2_ACTION_REQUEST = None


def set_session():
    global PLAYER_1_ACTION_REQUEST, PLAYER_2_ACTION_REQUEST, SHOW_GRAPHICS, min_exploration_rate, max_exploration_rate

    if EVALUATING or PLAYERS != AI_VS_AI:
        SHOW_GRAPHICS = True
    else:
        SHOW_GRAPHICS = False

    if PLAYERS == HUMAN_VS_HUMAN:
        PLAYER_1_ACTION_REQUEST = user.request_human_action
        PLAYER_2_ACTION_REQUEST = user.request_human_action
    else:
        print('Unsupported players')
        exit(1)

    if EXPLORATION_RATE_MODEL == FULL_EXPLORATION_RATE_MODEL:
        max_exploration_rate = 1
        min_exploration_rate = 0.01
    elif EXPLORATION_RATE_MODEL == SMALL_EXPLORATION_RATE_MODEL:
        max_exploration_rate = 0.5
        min_exploration_rate = 0.005
    elif EXPLORATION_RATE_MODEL == CONSTANT_EXPLORATION_RATE_MODEL:
        max_exploration_rate = 0.001
        min_exploration_rate = 0.001
    elif EXPLORATION_RATE_MODEL == NO_EXPLORATION_RATE_MODEL:
        max_exploration_rate = 0
        min_exploration_rate = 0


def main():
    console = Console(PLAYER_1_ACTION_REQUEST, PLAYER_2_ACTION_REQUEST)

    for game_number in range(NUMBER_OF_GAMES):
        while console.on:
            console.frame()

            if console.has_game_ended():
                if PLAYERS != AI_VS_AI and not console.pause:  # Request human to press 'p' to continue
                    console.pause = True

                if not console.pause:
                    console.reset()

    console.quit()


set_session()
main()
