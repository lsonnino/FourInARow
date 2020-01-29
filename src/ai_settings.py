AI_NAME = 'Shikamaru'

discount_rate = 0.5  # must be between 0 and 1
learning_rate = 0.0001  # must be between 0 and 1

batch_size = 128
replay_memory_capacity = 65536

FULL_EXPLORATION_RATE_MODEL = 0
SMALL_EXPLORATION_RATE_MODEL = 1
NO_EXPLORATION_RATE_MODEL = 2
CONSTANT_EXPLORATION_RATE_MODEL = 3

max_exploration_rate = 0.001  # must be between 0 and 1
min_exploration_rate = 0.001  # must be between 0 and 1
exploration_decay_rate = 0.9999  # must be between 0 and 1


def set_exploration(min_exp, max_exp):
    global min_exploration_rate, max_exploration_rate

    min_exploration_rate = min_exp
    max_exploration_rate = max_exp
