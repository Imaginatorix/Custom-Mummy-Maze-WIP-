from sprites.assets import button
import pygame
import math

class Screens():
    def wait_for_click(self, button_sprites, return_values):
        ''' Wait until a button is pressed '''
        waiting = True
        while waiting:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                # If user exits while waiting
                if event.type == pygame.QUIT:
                    try:
                        # Destroy all sprites
                        for sprite in self.all_sprites:
                            sprite.kill()
                    except AttributeError:
                        pass

                    # Loop out
                    waiting = False
                    self.exit_game()

                # If user presses the mouse
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()

                    # Loop all buttons and check if it's clicked
                    clicked_sprites = [clickable_sprite for clickable_sprite in button_sprites if clickable_sprite.rect.collidepoint(pos)]
                    if len(clicked_sprites) != 0:
                        considered_sprite = clicked_sprites[0]
                        return return_values[considered_sprite]


    def screens(self, screen_type):
        ''' Draw non-playable screen with buttons '''
        clickable_sprites = pygame.sprite.Group()
        # {Button: Return_Value}
        return_values = {}

        # Start Screen
        if screen_type == "start":
            height = self.screen_height * (0.15)
            width = self.screen_width * (0.8)
            font_size = math.ceil(height * (0.5))

            adventure_button = button.Button(self, "Adventure Mode", width, height, self.screen_width >> 1, (self.screen_height >> 1) + math.ceil(height/2), (0, 0, 0), self.FONT, font_size, (255, 255, 255))
            clickable_sprites.add(adventure_button)
            return_values[adventure_button] = "Adventure"

            # Draw screen
            # Background Color
            self.screen.fill(self.START_SCREEN_COLOR)
            self.draw_text(self.TITLE, font_size << 1, (255, 255, 255), self.screen_width >> 1, font_size)

            clickable_sprites.draw(self.screen)
            pygame.display.flip()

            self.game_mode = self.wait_for_click(clickable_sprites, return_values)

        clickable_sprites.empty()
