from src.console import Console
from src.session import *
from src.constants import AI_VS_AI
from src.settings import SHOW_GRAPHICS

PLAYER_1_ACTION_REQUEST = None
PLAYER_2_ACTION_REQUEST = None


def set_session():
    global PLAYER_1_ACTION_REQUEST, PLAYER_2_ACTION_REQUEST, SHOW_GRAPHICS

    if EVALUATING or PLAYERS != AI_VS_AI:
        settings.SHOW_GRAPHICS = True
    else:
        settings.SHOW_GRAPHICS = False

    if PLAYERS == HUMAN_VS_HUMAN:
        PLAYER_1_ACTION_REQUEST = user.request_human_action
        PLAYER_2_ACTION_REQUEST = user.request_ai_action
    else:
        print('Unsupported players')
        exit(1)


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


set_session()
main()
