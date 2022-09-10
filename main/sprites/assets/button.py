import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self, game, message, width, height, px, py, bg, font_name, font_size, font_color):
        super().__init__()
        self.game = game
        
        self.vec = pygame.math.Vector2

        # Draw rectangle
        self.image = pygame.Surface((width, height))
        self.image.fill(bg)

        # Get shape info
        self.rect = self.image.get_rect()

        # Draw message
        self.font = pygame.font.SysFont(font_name, font_size)
        self.text = self.font.render(message, False, font_color)
        # Center text
        x, y = self.rect.center
        x -= self.text.get_width() >> 1
        y -= self.text.get_height() >> 1

        # Draw text on rectangle
        self.image.blit(self.text, (x, y))

        # Position on (px, py) with anchor in the center
        self.pos = self.vec(px, py)
        self.rect.center = self.pos
