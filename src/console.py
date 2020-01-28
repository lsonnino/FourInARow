import pygame
from src import settings, constants
from src.game import Game


class Console(object):
    def __init__(self, player_1_action_request, player_2_action_request):
        if settings.SHOW_GRAPHICS:
            pygame.init()
            pygame.font.init()
            pygame.display.set_caption(constants.GAME_NAME)

            self.window = pygame.display.set_mode(constants.WIN_SIZE)
            self.clock = pygame.time.Clock()
            self.font = pygame.font.SysFont(constants.FONT, constants.FONT_SIZE)

            self.on = True
            self.pause = False

            self.player_1_action_request = player_1_action_request
            self.player_2_action_request = player_2_action_request
            self.game = Game()
            self.winner = constants.EMPTY_PIECE

    def draw_text(self, x, y, text, color=constants.TEXT_COLOR):
        text_surface = self.font.render(text, False, color)
        # Merge the texts with the window
        self.window.blit(text_surface, (x, y))

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
        return self.winner != constants.EMPTY_PIECE

    def frame(self):
        if settings.SHOW_GRAPHICS:
            self.key_binding()

        if not self.on:
            return

        if self.pause:
            self.refresh_graphics()
            return

        self.game.play(self)

        self.winner = self.game.check_winners()
        if self.has_game_ended():
            self.pause = True

        if settings.SHOW_GRAPHICS:
            self.game.draw(self.window)

            if self.has_game_ended():
                self.draw_text(
                    constants.PIECE_OFFSET,
                    constants.PIECE_OFFSET,
                    'Winner is ' + ('BLUE' if self.winner == constants.BLUE_PIECE else 'RED') + ' !!'
                )

        self.refresh_graphics()

    def request_action(self, player_id, action_space):
        player_action_request = self.player_1_action_request if player_id == 0 else self.player_2_action_request

        return player_action_request(action_space)

    def reset(self):
        self.on = True
        self.pause = False
        self.winner = constants.EMPTY_PIECE
        self.game.reset()
