import game_attributes as attr
import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height, coords, tile_type="default", color=None):
        super().__init__()
        self.game = game
        self.coords = coords

        self.vec = pygame.math.Vector2

        # default color
        if color is None:
            color = attr.TILE_COLOR

        self.image = pygame.Surface((width, height))
        # If Trap
        if tile_type == "trap":
            self.image.fill(attr.DEATH_SCREEN_COLOR)
        elif tile_type == "goal":
            self.image.fill(color)
        # If default
        elif tile_type == "default":
            self.image.fill(color)

        # Get shape info
        self.rect = self.image.get_rect()

        # Position on (x, y) with anchor in topleft
        self.pos = self.vec(x, y)
        self.rect.topleft = self.pos
