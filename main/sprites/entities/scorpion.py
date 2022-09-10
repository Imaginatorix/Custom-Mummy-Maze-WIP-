import pygame

class Scorpion(pygame.sprite.Sprite):
    def __init__(self, game, typing, startpos = (0, 0)):
        super().__init__()
        self.game = game
        
        self.vec = pygame.math.Vector2
        self.clock = pygame.time.Clock()

        self.start_pos = startpos
        self.x, self.y = startpos

        self.prev_moves = []

        h_tempo = game.rect_height * 0.5
        self.swidth, self.sheight = (h_tempo * 0.75, h_tempo * 0.75)
        self.sx, self.sy = (((((self.game.space_x * 0.5) + self.game.rect_width) * 0.5) - (self.swidth * 0.5)) + game.rect_width * (self.x - 1), ((((self.game.space_y * 0.5) + self.game.rect_height) * 0.5) - (self.sheight * 0.5)) + game.rect_height * (self.y - 1))

        self.typing = typing

        self.image = pygame.Surface((self.swidth, self.sheight))
        if typing == "normal":
            self.image.fill(normal_scorpion_color)
        elif typing == "red":
            self.image.fill(red_scorpion_color)
        self.rect = self.image.get_rect()
        self.pos = self.vec(self.sx, self.sy)

        self.rect.topleft = self.pos
        self.coords = (self.x, self.y)
        
    def update(self):
        if self.game.player.moved:
            self.prev_moves.append((self.x, self.y))
            self.movement(True)

            self.game.moving_entities += 1

    def movement(self, to_be_moved, target = None):
        if target is None:
            target = self.game.player.coords

        to_move = False
        direction = self.find_direction(target)
        if direction == "left" and self.coords not in set(self.game.constraints["left"]):
            self.pos.x -= self.game.rect_width
            self.x -= 1
            to_move = to_be_moved
        elif direction == "right" and self.coords not in set(self.game.constraints["right"]):
            self.pos.x += self.game.rect_width
            self.x += 1
            to_move = to_be_moved
        elif direction == "top" and self.coords not in set(self.game.constraints["top"]):
            self.pos.y -= self.game.rect_height
            self.y -= 1
            to_move = to_be_moved
        elif direction == "bottom" and self.coords not in set(self.game.constraints["bottom"]):
            self.pos.y += self.game.rect_height
            self.y += 1
            to_move = to_be_moved

        self.rect.topleft = self.pos
        self.coords = (self.x, self.y)

        if to_move:
            self.game.draw()

    def find_direction(self, target):
        distance = numpy.subtract(target, self.coords)

        if self.typing == "normal":
            if distance[0] > 0:
                if self.coords not in set(self.game.constraints["right"]):
                    return "right"
                elif distance[1] > 0:
                    if self.coords not in set(self.game.constraints["bottom"]):
                        return "bottom"
                elif distance[1] < 0:
                    if self.coords not in set(self.game.constraints["top"]):
                        return "top"
            elif distance[0] < 0:
                if self.coords not in set(self.game.constraints["left"]):
                    return "left"
                elif distance[1] > 0:
                    if self.coords not in set(self.game.constraints["bottom"]):
                        return "bottom"
                elif distance[1] < 0:
                    if self.coords not in set(self.game.constraints["top"]):
                        return "top"
            else:
                if distance[1] > 0:
                    if self.coords not in set(self.game.constraints["bottom"]):
                        return "bottom"
                elif distance[1] < 0:
                    if self.coords not in set(self.game.constraints["top"]):
                        return "top"
        elif self.typing == "red":
            if distance[1] > 0:
                if self.coords not in set(self.game.constraints["bottom"]):
                    return "bottom"
                elif distance[0] > 0:
                    if self.coords not in set(self.game.constraints["right"]):
                        return "right"
                elif distance[0] < 0:
                    if self.coords not in set(self.game.constraints["left"]):
                        return "left"
            elif distance[1] < 0:
                if self.coords not in set(self.game.constraints["top"]):
                    return "top"
                elif distance[0] > 0:
                    if self.coords not in set(self.game.constraints["right"]):
                        return "right"
                elif distance[0] < 0:
                    if self.coords not in set(self.game.constraints["left"]):
                        return "left"
            else:
                if distance[0] > 0:
                    if self.coords not in set(self.game.constraints["right"]):
                        return "right"
                elif distance[0] < 0:
                    if self.coords not in set(self.game.constraints["left"]):
                        return "left"

    def undo(self):
        try:
            self.x, self.y = self.prev_moves[len(self.prev_moves) - 1]
            self.prev_moves.pop()
        except IndexError:
            pass

        self.sx, self.sy = (((((self.game.space_x * 0.5) + self.game.rect_width) * 0.5) - (self.swidth * 0.5)) + self.game.rect_width * (self.x - 1), ((((self.game.space_y * 0.5) + self.game.rect_height) * 0.5) - (self.sheight * 0.5)) + self.game.rect_height * (self.y - 1))

        self.pos = self.vec(self.sx, self.sy)
        self.rect.topleft = self.pos
        self.coords = (self.x, self.y)
