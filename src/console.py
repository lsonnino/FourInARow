import pygame
import numpy as np
from src import settings, constants, user
from src.game import Game


class Console(object):
    def __init__(self, is_player_1_ai, is_player_2_ai):
        if settings.SHOW_GRAPHICS:
            pygame.init()
            pygame.font.init()
            pygame.display.set_caption(constants.GAME_NAME)

            self.window = pygame.display.set_mode(constants.WIN_SIZE)
            self.clock = pygame.time.Clock()
            self.font = pygame.font.SysFont(constants.FONT, constants.FONT_SIZE)

        self.on = True
        self.pause = False
        self.pressed = False

        self.is_player_1_ai = is_player_1_ai
        self.is_player_2_ai = is_player_2_ai
        self.game = Game()
        self.winner = constants.EMPTY_PIECE
        self.is_won = False

    def __get_state(self):
        return self.game.get_state()

    def change_perspective(self, old_state, action, reward, next_state):
        reward = -reward

        old_state = self.game.change_perspective(old_state)
        next_state = self.game.change_perspective(next_state)

        return old_state, action, reward, next_state

    def draw_text(self, x, y, text, color=constants.TEXT_COLOR, align_right=False, align_bottom=False):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()

        if align_right:
            text_rect.right = x
        else:
            text_rect.left = x

        if align_bottom:
            text_rect.bottom = y
        else:
            text_rect.top = y

        # Merge the texts with the window
        self.window.blit(text_surface, text_rect)

    def key_binding(self):
        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit
                self.on = False
                break

        # PRESSED KEYS
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:  # Quit
            self.on = False
        elif keys[pygame.K_p] and not self.pressed:  # Pause/resume the game
            self.pause = not self.pause
            self.pressed = True
        elif not keys[pygame.K_p] and self.pressed:
            self.pressed = False

    def refresh_graphics(self):
        if settings.SHOW_GRAPHICS:
            pygame.display.flip()
            self.clock.tick(settings.FPS)

    def has_game_ended(self):
        return self.is_won

    def frame(self):
        reward = 0
        old_state = self.__get_state()
        next_state = old_state
        action = constants.NONE

        if settings.SHOW_GRAPHICS:
            self.key_binding()

        if not self.on:
            return old_state, reward, action, next_state

        if self.pause or self.has_game_ended():
            self.refresh_graphics()
            return old_state, reward, action, next_state

        if not self.game.can_play():
            self.on = False
            self.is_won = True
        else:
            result, action, next_state = self.game.play(self)

            if not result:
                reward -= 5

        self.winner = self.game.check_winners()
        if self.winner != constants.EMPTY_PIECE:
            self.is_won = True

            if result:
                reward += 100  # player has won

        if self.has_game_ended():
            self.pause = True

        if settings.SHOW_GRAPHICS:
            self.game.draw(self.window)

            action_str = "None"
            if action == constants.LEFT:
                action_str = "Left"
            elif action == constants.RIGHT:
                action_str = "Right"
            elif action == constants.PLACE:
                action_str = "Place"

            self.draw_text(
                constants.PIECE_OFFSET,
                constants.WIN_SIZE[1] - constants.PIECE_OFFSET,
                "Action: " + action_str,
                align_bottom=True
            )

            self.draw_text(
                constants.PIECE_OFFSET,
                constants.WIN_SIZE[1] - 2 * constants.PIECE_OFFSET,
                "Reward: " + str(reward),
                align_bottom=True
            )

            if self.has_game_ended():
                if self.winner == constants.EMPTY_PIECE:
                    text = 'Nobody won'
                else:
                    text = 'Winner is ' + ('BLUE' if self.winner == constants.BLUE_PIECE else 'RED') + ' !!'

                self.draw_text(
                    constants.PIECE_OFFSET,
                    constants.PIECE_OFFSET,
                    text
                )

            if self.pause:
                self.draw_text(
                    constants.WIN_SIZE[0] - constants.PIECE_OFFSET,
                    constants.PIECE_OFFSET,
                    '| PAUSE |',
                    align_right=True
                )

        self.refresh_graphics()

        return old_state, reward, action, next_state

    def request_action(self, player_id):
        if player_id == 0:
            checker_ai = self.is_player_1_ai
        elif player_id == 1:
            checker_ai = self.is_player_2_ai

        if checker_ai:
            return user.request_ai_action(self.__get_state())
        else:
            return user.request_human_action()

    def reset(self):
        self.on = True
        self.pause = False
        self.winner = constants.EMPTY_PIECE
        self.is_won = False
        self.game.reset()

    def quit(self):
        pygame.quit()
