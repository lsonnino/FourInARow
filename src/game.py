from src.constants import *
import numpy as np
import pygame


class Map(object):
    def __init__(self):
        self.field = np.zeros((COLUMNS, ROWS), dtype=int)
        self.columns_height = np.zeros(COLUMNS, dtype=int)

    def __check_mask(self, x, y, player, mask):
        dx = 0

        count = 0

        while 0 <= x + dx < COLUMNS:
            if dx >= len(mask):
                break

            dy = 0

            while 0 <= y + dy < ROWS:

                if dy >= len(mask[dx]):
                    break

                if mask[dx][dy] and self.field[x + dx][y + dy] != player:
                    return False
                elif mask[dx][dy]:
                    count += 1

                dy += 1

            dx += 1

        return count == 4  # 4 in a row are needed to win

    def __get_column_height(self, x):
        if x < 0 or x >= COLUMNS:
            return ROWS
        else:
            return self.columns_height[x]

    def can_place(self):
        for x in range(COLUMNS):
            if self.__get_column_height(x) != ROWS:
                return True

        return False

    def place(self, player, x):
        if self.__get_column_height(x) >= ROWS:
            return False

        self.field[x, self.columns_height[x]] = player
        self.columns_height[x] += 1

        return True

    def check_winners(self):
        players = [RED_PIECE, BLUE_PIECE]

        for x in range(COLUMNS):
            for y in range(ROWS):
                for player in players:
                    for mask in WINNING_MASK:
                        if self.__check_mask(x, y, player, mask):
                            return player

        return EMPTY_PIECE

    def reset(self):
        self.__init__()


class Game(object):
    def __init__(self):
        self.map = Map()
        self.current_player = BLUE_PIECE
        self.current_column = int(COLUMNS / 2)

    def __end_turn(self):
        self.current_column = int(COLUMNS / 2)
        self.current_player = RED_PIECE if self.current_player == BLUE_PIECE else BLUE_PIECE

    def __right(self):
        self.current_column += 1

        if self.current_column >= COLUMNS:
            self.current_column = COLUMNS - 1
            return False
        else:
            return True

    def __left(self):
        self.current_column -= 1

        if self.current_column < 0:
            self.current_column = 0
            return False
        return True

    def __place(self):
        return self.map.place(self.current_player, self.current_column)

    def __draw_piece(self, window, x, y):
        if self.map.field[x, y] == RED_PIECE:
            color = RED_COLOR
        elif self.map.field[x, y] == BLUE_PIECE:
            color = BLUE_COLOR
        else:
            color = EMPTY_COLOR

        absolute_x = WIN_SIZE[0] - COLUMNS * PIECE_DIAMETER - (COLUMNS - 1) * PIECE_OFFSET  # Get left-right margin
        absolute_x = absolute_x / 2  # Remove right margin
        absolute_x += x * (PIECE_DIAMETER + PIECE_OFFSET)  # move to the correct column

        field_height = ROWS * PIECE_DIAMETER + (ROWS - 1) * PIECE_OFFSET
        absolute_y = WIN_SIZE[1] - field_height  # Get top-bottom margin
        absolute_y = absolute_y / 2  # Remove bottom margin
        absolute_y += field_height  # move to bottom of the field
        absolute_y -= y * (PIECE_DIAMETER + PIECE_OFFSET)  # move to the right row

        pygame.draw.circle(
            window,
            color,
            (
                int(absolute_x + PIECE_DIAMETER / 2),
                int(absolute_y - PIECE_DIAMETER / 2)
            ),
            int(PIECE_DIAMETER / 2)
        )

    def __draw_selector(self, surface):
        """
        Based on this tutorial:
            https://archives.seul.org/pygame/users/Mar-2008/msg00538.html
        """
        selector_color = RED_COLOR if self.current_player == RED_PIECE else BLUE_COLOR

        x = WIN_SIZE[0] - COLUMNS * PIECE_DIAMETER - (COLUMNS - 1) * PIECE_OFFSET  # Get left-right margin
        x = x / 2  # Remove right margin
        x += self.current_column * (PIECE_DIAMETER + PIECE_OFFSET)  # move to the correct column
        x -= (PIECE_OFFSET + SELECTOR_WIDTH) / 2  # move next to selected column

        field_height = ROWS * PIECE_DIAMETER + (ROWS - 1) * PIECE_OFFSET
        rectangle_height = field_height + PIECE_OFFSET + SELECTOR_WIDTH
        y = WIN_SIZE[1] - field_height  # Get top-bottom margin
        y = y / 2  # Remove bottom margin
        y -= (PIECE_OFFSET + SELECTOR_RADIUS) / 2  # move on op of selected column

        rect = pygame.Rect(
            x,
            y,
            PIECE_DIAMETER + PIECE_OFFSET + SELECTOR_WIDTH,
            rectangle_height
        )

        clip = surface.get_clip()

        # left and right
        surface.set_clip(clip.clip(rect.inflate(0, -SELECTOR_RADIUS * 2)))
        pygame.draw.rect(surface, selector_color, rect.inflate(1 - SELECTOR_WIDTH, 0), SELECTOR_WIDTH)

        # top and bottom
        surface.set_clip(clip.clip(rect.inflate(-SELECTOR_RADIUS * 2, 0)))
        pygame.draw.rect(surface, selector_color, rect.inflate(0, 1 - SELECTOR_WIDTH), SELECTOR_WIDTH)

        # top left corner
        surface.set_clip(clip.clip(rect.left, rect.top, SELECTOR_RADIUS, SELECTOR_RADIUS))
        pygame.draw.ellipse(surface, selector_color, pygame.Rect(rect.left, rect.top, 2 * SELECTOR_RADIUS,
                                                                 2 * SELECTOR_RADIUS), SELECTOR_WIDTH)

        # top right corner
        surface.set_clip(clip.clip(rect.right - SELECTOR_RADIUS, rect.top, SELECTOR_RADIUS, SELECTOR_RADIUS))
        pygame.draw.ellipse(
            surface,
            selector_color,
            pygame.Rect(
                rect.right - 2 * SELECTOR_RADIUS, rect.top, 2 * SELECTOR_RADIUS, 2 * SELECTOR_RADIUS
            ),
            SELECTOR_WIDTH
        )

        # bottom left
        surface.set_clip(clip.clip(rect.left, rect.bottom - SELECTOR_RADIUS, SELECTOR_RADIUS, SELECTOR_RADIUS))
        pygame.draw.ellipse(
            surface,
            selector_color,
            pygame.Rect(
                rect.left, rect.bottom - 2 * SELECTOR_RADIUS, 2 * SELECTOR_RADIUS, 2 * SELECTOR_RADIUS
            ),
            SELECTOR_WIDTH
        )

        # bottom right
        surface.set_clip(clip.clip(rect.right - SELECTOR_RADIUS, rect.bottom - SELECTOR_RADIUS, SELECTOR_RADIUS,
                                   SELECTOR_RADIUS))
        pygame.draw.ellipse(
            surface,
            selector_color,
            pygame.Rect(
                rect.right - 2 * SELECTOR_RADIUS, rect.bottom - 2 * SELECTOR_RADIUS, 2 * SELECTOR_RADIUS, 2 * SELECTOR_RADIUS
            ),
            SELECTOR_WIDTH
        )

        surface.set_clip(clip)

    def get_state(self):
        state = np.zeros(ROWS * COLUMNS + COLUMNS)

        for x in range(COLUMNS):
            for y in range(ROWS):
                state[x * ROWS + y] = self.current_player * self.map.field[x, y]

            if self.current_column == x:
                state[ROWS * COLUMNS] = 1.0

        return state

    def change_perspective(self, state):
        for x in range(COLUMNS):
            for y in range(ROWS):
                state[x * ROWS + y] = -state[x * ROWS + y]

        return state

    def can_play(self):
        return self.map.can_place()

    def play(self, console):
        action = console.request_action(
            0 if self.current_player == BLUE_PIECE else 1
        )

        if action == LEFT:
            result = self.__left()
            next_state = self.get_state()
        elif action == RIGHT:
            result = self.__right()
            next_state = self.get_state()
        elif action == PLACE:
            result = self.__place()
            next_state = self.get_state()
            if result:
                self.__end_turn()

        return result, action, next_state

    def draw(self, window):
        window.fill(BACKGROUND_COLOR)

        for x in range(COLUMNS):
            for y in range(ROWS):
                self.__draw_piece(window, x, y)

        self.__draw_selector(window)

    def check_winners(self):
        return self.map.check_winners()

    def reset(self):
        self.current_player = BLUE_PIECE
        self.current_column = int(COLUMNS / 2)
        self.map.reset()

