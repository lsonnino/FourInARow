import pygame
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

            self.is_player_1_ai = is_player_1_ai
            self.is_player_2_ai = is_player_2_ai
            self.game = Game()
            self.winner = constants.EMPTY_PIECE
            self.is_won = False

    def draw_text(self, x, y, text, color=constants.TEXT_COLOR, align_right=False):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align_right:
            text_rect.right = x
        else:
            text_rect.left = x
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
        elif keys[pygame.K_p]:  # Pause/resume the game
            self.pause = not self.pause

    def refresh_graphics(self):
        if settings.SHOW_GRAPHICS:
            pygame.display.flip()
            self.clock.tick(settings.FPS)

    def has_game_ended(self):
        return self.is_won

    def frame(self):
        if settings.SHOW_GRAPHICS:
            self.key_binding()

        if not self.on:
            return

        if self.pause:
            self.refresh_graphics()
            return

        if not self.game.can_play():
            self.on = False
            self.is_won = True
        else:
            self.game.play(self)

        self.winner = self.game.check_winners()
        if self.winner != constants.EMPTY_PIECE:
            self.is_won = True

        if self.has_game_ended():
            self.pause = True

        if settings.SHOW_GRAPHICS:
            self.game.draw(self.window)

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

    def request_action(self, player_id, action_space):
        if player_id == 0:
            player_action_request = user.request_ai_action if self.is_player_1_ai else user.request_human_action
        elif player_id == 1:
            player_action_request = user.request_ai_action if self.is_player_2_ai else user.request_human_action

        return player_action_request(action_space)

    def reset(self):
        self.on = True
        self.pause = False
        self.winner = constants.EMPTY_PIECE
        self.game.reset()

    def quit(self):
        pygame.quit()
