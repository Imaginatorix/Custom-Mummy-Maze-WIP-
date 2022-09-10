import pygame

class Side(pygame.sprite.Sprite):
    def __init__(self, game, color, x, y, width, height):
        super().__init__()
        self.game = game

        self.vec = pygame.math.Vector2

        self.image = pygame.Surface((width, height))
        self.image.fill(color)

        # Get shape info
        self.rect = self.image.get_rect()

        # Position on (x, y) with anchor in topleft
        self.pos = self.vec(x, y)
        self.rect.topleft = self.pos
