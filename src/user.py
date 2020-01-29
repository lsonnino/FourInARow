import pygame
import numpy as np
from src import constants, ai


def decode_action(action):
    if action == 0:
        return constants.LEFT
    if action == 1:
        return constants.RIGHT
    if action == 2:
        return constants.PLACE

    return constants.NONE


def encode_action(action):
    if action == constants.LEFT:
        return 0

    if action == constants.RIGHT:
        return 1

    if action == constants.PLACE:
        return 2

    return -1


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

    return decode_action(action)
