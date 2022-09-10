import game_attributes as attr
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, game, tile_width, tile_height, x, y, coordinates):
        super().__init__()
        self.game = game
        
        self.vec = pygame.math.Vector2

        # Record coordinates
        self.coordinates = coordinates

        # Solve for sprite dimensions
        self.basis_length = min(tile_width, tile_height)
        alpha = 0.45
        self.sprite_width, self.sprite_height = (self.basis_length * alpha * 0.8, self.basis_length * alpha)

        self.image = pygame.Surface((self.sprite_width, self.sprite_height))
        self.image.fill(attr.PLAYER_COLOR)

        # Get shape info
        self.rect = self.image.get_rect()

        # Position on (x, y) with anchor in center -- center on tile
        self.pos = self.vec(x + (tile_width / 2), y + (tile_height / 2))
        self.rect.center = self.pos
        

    # def update(self):
    #     pass
    #     x, y = self.coords
    #     if not self.moved:
    #         self.keys = pygame.key.get_pressed()
    #         # change to elif to avoid diagonal movement (previously if)
    #         if self.keys[pygame.K_LEFT] and self.pos.x > self.game.rect_width and self.coords not in set(self.game.constraints["left"]):
    #             self.pos.x -= self.game.rect_width
    #             x -= 1
    #         elif self.keys[pygame.K_RIGHT] and self.pos.x < (self.game.py_width - self.mwidth - self.game.rect_width) and self.coords not in set(self.game.constraints["right"]):
    #             self.pos.x += self.game.rect_width
    #             self.x += 1
    #         elif self.keys[pygame.K_UP] and self.pos.y > self.game.rect_height and self.coords not in set(self.game.constraints["top"]):
    #             self.pos.y -= self.game.rect_height
    #             self.y -= 1
    #         elif self.keys[pygame.K_DOWN] and self.pos.y < (self.game.py_height - self.mheight - self.game.rect_height) and self.coords not in set(self.game.constraints["bottom"]):
    #             self.pos.y += self.game.rect_height
    #             self.y += 1
    #         elif self.keys[pygame.K_SPACE]:
    #             self.end_move(x, y)

    #         self.rect.topleft = self.pos
    #         self.coords = (self.x, self.y)

    #         if (x, y) != (self.coords):
    #             self.end_move(x, y)


    # def end_move(self, x, y):
    #     self.moved = True
    #     self.game.turn += 1

