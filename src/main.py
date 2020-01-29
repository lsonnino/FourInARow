from src.console import Console
from src.session import *
from src.constants import AI_VS_AI
from src import settings, ai_settings, ai

IS_PLAYER_1_AI = False
IS_PLAYER_2_AI = False


# todo list
#   - use state in user.request_ai_action
#   - reward system (even for the looser !!)


def set_session():
    global IS_PLAYER_1_AI, IS_PLAYER_2_AI

    if EVALUATING or PLAYERS != AI_VS_AI:
        settings.SHOW_GRAPHICS = True
    else:
        settings.SHOW_GRAPHICS = False

    if PLAYERS == HUMAN_VS_HUMAN:
        IS_PLAYER_1_AI = False
        IS_PLAYER_2_AI = False
    elif PLAYERS == HUMAN_VS_AI:
        IS_PLAYER_1_AI = False
        IS_PLAYER_2_AI = True
    elif PLAYERS == AI_VS_AI:
        IS_PLAYER_1_AI = True
        IS_PLAYER_2_AI = True
    else:
        print('Unsupported players')
        exit(1)

    if IS_PLAYER_1_AI or IS_PLAYER_2_AI:
        ai.set_agent(ai.Agent(name=ai_settings.AI_NAME))

    if EXPLORATION_RATE_MODEL == FULL_EXPLORATION_RATE_MODEL:
        ai_settings.max_exploration_rate = 1
        ai_settings.min_exploration_rate = 0.01
    elif EXPLORATION_RATE_MODEL == SMALL_EXPLORATION_RATE_MODEL:
        ai_settings.max_exploration_rate = 0.5
        ai_settings.min_exploration_rate = 0.005
    elif EXPLORATION_RATE_MODEL == CONSTANT_EXPLORATION_RATE_MODEL:
        ai_settings.max_exploration_rate = 0.001
        ai_settings.min_exploration_rate = 0.001
    elif EXPLORATION_RATE_MODEL == NO_EXPLORATION_RATE_MODEL:
        ai_settings.max_exploration_rate = 0
        ai_settings.min_exploration_rate = 0


def main():
    console = Console(IS_PLAYER_1_AI, IS_PLAYER_2_AI)

    for game_number in range(NUMBER_OF_GAMES):
        while console.on:
            could_play, reward, action = console.frame()

            if console.has_game_ended():
                if PLAYERS != AI_VS_AI and not console.pause:  # Request human to press 'p' to continue
                    console.pause = True
                elif PLAYERS == AI_VS_AI or not console.pause:
                    break

        console.reset()

    console.quit()


set_session()
main()
