import pygame
import numpy as np
from src import constants, ai


def request_human_action():
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        return constants.PLACE
    elif keys[pygame.K_LEFT]:
        return constants.LEFT
    elif keys[pygame.K_RIGHT]:
        return constants.RIGHT
    else:
        return constants.NONE


def request_ai_action(state):
    action = ai.agent.choose_action(state)

    if action == 0:
        return constants.LEFT
    elif action == 1:
        return constants.RIGHT
    else:
        return constants.PLACE
