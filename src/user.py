import pygame
import numpy as np
from src import constants


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


def request_ai_action(map, player):
    state = np.zeros(constants.ROWS * constants.COLUMNS)

    for x in range(constants.COLUMNS):
        for y in range(constants.ROWS):
            state[x * constants.ROWS + y] = player * map.field[x, y]

    return np.random.choice([constants.LEFT, constants.RIGHT, constants.PLACE], 1)[0]
