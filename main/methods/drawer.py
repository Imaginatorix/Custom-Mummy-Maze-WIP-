import pygame

class Drawer():
    def draw_text(self, text, size, color, x, y):
        ''' Draw text on screen '''
        # Load font
        font = pygame.font.Font(self.FONT, size)
        text_surface = font.render(text, True, color)
        # Position sprite
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        # Draw on screen
        self.screen.blit(text_surface, text_rect)

