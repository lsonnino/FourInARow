from src.console import Console
from src.session import *
from src.constants import AI_VS_AI, NONE, WIN_SIZE, PIECE_OFFSET
from src import settings, ai_settings, ai, user
import os

IS_PLAYER_1_AI = False
IS_PLAYER_2_AI = False
IS_AI = False


def set_session():
    global IS_PLAYER_1_AI, IS_PLAYER_2_AI, IS_AI

    if SESSION_TYPE == EVALUATING or PLAYERS != AI_VS_AI:
        settings.set_graphics(True)
    else:
        settings.set_graphics(False)

    if EXPLORATION_RATE_MODEL == FULL_EXPLORATION_RATE_MODEL:
        ai_settings.set_exploration(min_exp=0.01, max_exp=1)
    elif EXPLORATION_RATE_MODEL == SMALL_EXPLORATION_RATE_MODEL:
        ai_settings.set_exploration(min_exp=0.005, max_exp=0.5)
    elif EXPLORATION_RATE_MODEL == CONSTANT_EXPLORATION_RATE_MODEL:
        ai_settings.set_exploration(min_exp=0.001, max_exp=0.001)
    elif EXPLORATION_RATE_MODEL == NO_EXPLORATION_RATE_MODEL:
        ai_settings.set_exploration(min_exp=0, max_exp=0)

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
        IS_AI = True
        ai.set_agent(ai.Agent(name=ai_settings.AI_NAME))


def get_path(num):
    return DATA_DIR + '/' + AI_DIR + '/' + str(num)


def read_ai_num(num):
    path = get_path(num)
    try:
        ai.agent.load_models(path)
        return True
    except Exception:
        return False


def save_ai_num(num):
    path = get_path(num)

    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)
    elif os.path.exists(path):
        os.remove(path)

    ai.agent.save_models(path)


def main():
    console = Console(IS_PLAYER_1_AI, IS_PLAYER_2_AI)

    game_number = 1
    ai_gen = 1

    if IS_AI and read_ai_num(LOAD_AI):
        ai_gen = LOAD_AI + 1

    while game_number <= NUMBER_OF_GAMES:
        print("Playing with gen " + str(ai_gen) + " ...", end='')

        while console.on:
            old_state, reward, action, next_state = console.frame()

            if IS_AI and action != NONE:  # If action is NONE, the AI did not play (console off, ...)
                ai.agent.store_transition(
                    state=old_state,
                    chosen_action=user.encode_action(action),
                    reward=reward,
                    new_state=next_state,
                    terminal=console.is_won
                )

                if console.is_won:
                    old_state, reward, action, next_state = console.change_perspective(
                        old_state=old_state,
                        reward=reward,
                        action=action,
                        next_state=next_state
                    )
                    ai.agent.store_transition(
                        state=old_state,
                        chosen_action=user.encode_action(action),
                        reward=reward,
                        new_state=next_state,
                        terminal=console.is_won
                    )

                ai.agent.learn()

            if console.has_game_ended():
                if PLAYERS == AI_VS_AI or not console.pause:
                    break

        console.reset()

        print(" done \t\t end greed: " + str(round(ai.agent.epsilon * 100, 2)) + "%")

        if IS_AI and ai_gen > 0 and SAVE_EVERY > 0 and ai_gen % SAVE_EVERY == 0:
            save_ai_num(ai_gen)

        game_number += 1
        ai_gen += 1

    console.quit()


set_session()
main()
