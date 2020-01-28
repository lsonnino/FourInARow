import pygame
import numpy as np


def request_human_action(action_space):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        return action_space[1]
    elif keys[pygame.K_LEFT]:
        return action_space[0]
    elif keys[pygame.K_RIGHT]:
        return action_space[2]


def request_ai_action(action_space):
    return np.random.choice(action_space, 1)[0]
