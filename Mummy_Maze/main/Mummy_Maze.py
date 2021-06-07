# Remove PyGame library message
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

# start of code
from game_attr import *
import pygame
import numpy
import pyautogui
import time
import math
import os
# doing quick messages
from tkinter import *
from tkinter import messagebox

class Player(pygame.sprite.Sprite):
    def __init__(self, game, startpos = (0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        
        self.vec = pygame.math.Vector2

        self.start_pos = startpos
        self.x, self.y = startpos

        self.prev_moves = []

        h_tempo = game.rect_height * 0.5
        self.mwidth, self.mheight = (h_tempo * 0.75, h_tempo)
        self.mx, self.my = (((((self.game.space_x * 0.5) + self.game.rect_width) * 0.5) - (self.mwidth * 0.5)) + game.rect_width * (self.x - 1), ((((self.game.space_y * 0.5) + self.game.rect_height) * 0.5) - (self.mheight * 0.5)) + game.rect_height * (self.y - 1))

        self.image = pygame.Surface((self.mwidth, self.mheight))
        self.image.fill(player_color)
        self.rect = self.image.get_rect()
        self.pos = self.vec(self.mx, self.my)

        self.coords = (self.x, self.y)

        self.moved = False
        
    def update(self):
        x, y = (self.x, self.y)
        if not self.moved:
            self.keys = pygame.key.get_pressed()
            # change to elif to avoid diagonal movement (previously if)
            if self.keys[pygame.K_LEFT] and self.pos.x > self.game.rect_width and self.coords not in set(self.game.constraints["left"]):
                self.pos.x -= self.game.rect_width
                self.x -= 1
            elif self.keys[pygame.K_RIGHT] and self.pos.x < (self.game.py_width - self.mwidth - self.game.rect_width) and self.coords not in set(self.game.constraints["right"]):
                self.pos.x += self.game.rect_width
                self.x += 1
            elif self.keys[pygame.K_UP] and self.pos.y > self.game.rect_height and self.coords not in set(self.game.constraints["top"]):
                self.pos.y -= self.game.rect_height
                self.y -= 1
            elif self.keys[pygame.K_DOWN] and self.pos.y < (self.game.py_height - self.mheight - self.game.rect_height) and self.coords not in set(self.game.constraints["bottom"]):
                self.pos.y += self.game.rect_height
                self.y += 1
            elif self.keys[pygame.K_SPACE]:
                self.end_move(x, y)

            self.rect.topleft = self.pos
            self.coords = (self.x, self.y)

            if (x, y) != (self.coords):
                self.end_move(x, y)

    def end_move(self, x, y):
        self.prev_moves.append((x, y))
        self.moved = True
        self.game.turn += 1

    def undo(self):
        try:
            self.x, self.y = self.prev_moves[len(self.prev_moves) - 1]
            self.prev_moves.pop()
        except IndexError:
            pass

        self.mx, self.my = (((((self.game.space_x * 0.5) + self.game.rect_width) * 0.5) - (self.mwidth * 0.5)) + self.game.rect_width * (self.x - 1), ((((self.game.space_y * 0.5) + self.game.rect_height) * 0.5) - (self.mheight * 0.5)) + self.game.rect_height * (self.y - 1))

        self.pos = self.vec(self.mx, self.my)
        self.rect.topleft = self.pos
        self.coords = (self.x, self.y)

        self.moved = False

class Mummy(pygame.sprite.Sprite):
    def __init__(self, game, typing, startpos = (0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        
        self.vec = pygame.math.Vector2
        self.clock = pygame.time.Clock()

        self.start_pos = startpos
        self.x, self.y = startpos

        self.prev_moves = []

        h_tempo = game.rect_height * 0.5
        self.mwidth, self.mheight = (h_tempo * 0.75, h_tempo)
        self.mx, self.my = (((((self.game.space_x * 0.5) + self.game.rect_width) * 0.5) - (self.mwidth * 0.5)) + game.rect_width * (self.x - 1), ((((self.game.space_y * 0.5) + self.game.rect_height) * 0.5) - (self.mheight * 0.5)) + game.rect_height * (self.y - 1))

        self.typing = typing

        self.image = pygame.Surface((self.mwidth, self.mheight))
        if typing == "normal":
            self.image.fill(white_mummy_color)
        elif typing == "red":
            self.image.fill(red_mummy_color)
        self.rect = self.image.get_rect()
        self.pos = self.vec(self.mx, self.my)

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

        for _ in range(2):
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
                time.sleep(0.5)

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

        self.mx, self.my = (((((self.game.space_x * 0.5) + self.game.rect_width) * 0.5) - (self.mwidth * 0.5)) + self.game.rect_width * (self.x - 1), ((((self.game.space_y * 0.5) + self.game.rect_height) * 0.5) - (self.mheight * 0.5)) + self.game.rect_height * (self.y - 1))

        self.pos = self.vec(self.mx, self.my)
        self.rect.topleft = self.pos
        self.coords = (self.x, self.y)

class Scorpion(pygame.sprite.Sprite):
    def __init__(self, game, typing, startpos = (0, 0)):
        pygame.sprite.Sprite.__init__(self)
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

class Button(pygame.sprite.Sprite):
    def __init__(self, game, message, l, w, px, py, bg, fs, fcolor):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        
        self.vec = pygame.math.Vector2

        self.image = pygame.Surface((l, w))
        self.image.fill(bg)
        self.rect = self.image.get_rect()

        self.font = pygame.font.SysFont(FONT_NAME, fs)
        self.text = self.font.render(message, False, fcolor)
        x, y = self.rect.center
        x -= self.text.get_width() >> 1
        y -= self.text.get_height() >> 1

        self.image.blit(self.text, (x, y))

        self.pos = self.vec(px, py)
        self.rect.center = self.pos

class Tile(pygame.sprite.Sprite):
    def __init__(self, game, color, attrs, coords, dangerous = False):
        pygame.sprite.Sprite.__init__(self)
        self.game = game

        self.vec = pygame.math.Vector2

        x, y, l, w = attrs

        self.image = pygame.Surface((l, w))
        if dangerous:
            self.image.fill(killer_color)
        else:
            self.image.fill(color)
        self.rect = self.image.get_rect()

        self.coords = coords

        self.pos = self.vec(x, y)
        self.rect.topleft = self.pos
    
class Side(pygame.sprite.Sprite):
    def __init__(self, game, color, attrs):
        pygame.sprite.Sprite.__init__(self)
        self.game = game

        self.vec = pygame.math.Vector2

        x, y, l, w = attrs

        self.image = pygame.Surface((l, w))
        self.image.fill(color)
        self.rect = self.image.get_rect()

        self.pos = self.vec(x, y)
        self.rect.topleft = self.pos

class Game():
    def __init__(self):
        pygame.init()
        
        screen_width, screen_height = pyautogui.size()
        self.py_width, self.py_height = screen_width >> 1, screen_height >> 1
        self.screen = pygame.display.set_mode((self.py_width, self.py_height))
        pygame.display.set_caption(TITLE)
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.show_start = True
        self.font_name = pygame.font.match_font(FONT_NAME)

    def replace_sprites(self):
        size, startpos, goal, mummies, scorpions, traps, obstacles = self.sprite_args

        self.game_winner = None

        if obstacles is None:
            self.obstacles = []
        else:
            # set and dict is very fast
            self.obstacles = obstacles

        if traps is None:
            self.death_zones = []
        else:
            # set and dict is very fast
            self.death_zones = traps

        self.constraints = {
            "left": [],
            "right": [],
            "top": [],
            "bottom": []
        }

        self.numx_rect, self.numy_rect = size

        self.rect_width = self.py_width / self.numx_rect
        self.rect_height = self.py_height / self.numy_rect

        self.space_x = self.rect_width * 0.08
        self.space_y = self.rect_height * 0.08

        self.all_sprites = pygame.sprite.Group()

        for a in range(self.numx_rect):
            for b in range(self.numy_rect):
                a_cor = a + 1
                b_cor = b + 1
                attr = ((self.rect_width * a) + (self.space_x * 0.5), (self.rect_height * b) + (self.space_y * 0.5), self.rect_width - self.space_x, self.rect_height - self.space_y)

                # pygame.draw.rect(self.screen, color_theme, attr)
                if (a_cor, b_cor) in set(self.death_zones):
                    self.all_sprites.add(Tile(self, color_theme, attr, (a_cor, b_cor), True))
                else:
                    self.all_sprites.add(Tile(self, color_theme, attr, (a_cor, b_cor)))
                
                x, y, _, _ = attr
                w, h = (self.rect_width, self.rect_height)
                # Add border
                if a_cor == 1:
                    self.add_obstacle(["left"], x, y, w, h, False, a_cor, b_cor)
                elif a_cor == self.numx_rect:
                    self.add_obstacle(["right"], x, y, w, h, False, a_cor, b_cor)
                if b_cor == 1:
                    self.add_obstacle(["top"], x, y, w, h, False, a_cor, b_cor)
                elif b_cor == self.numy_rect:
                    self.add_obstacle(["bottom"], x, y, w, h, False, a_cor, b_cor)
                
                if (a_cor, b_cor) == goal["Coordinates"]:
                    self.place_goal(goal["Side"], x, y, w, h, goal["Coordinates"])
                elif (a_cor, b_cor) in self.obstacles:
                    self.add_obstacle(self.obstacles[(a_cor, b_cor)], x, y, w, h, True, a_cor, b_cor)

        self.finish = [goal["Coordinates"], goal["Side"]]

        self.player = Player(self, startpos)
        self.all_sprites.add(self.player)

        self.all_enemies = []
        for mummy_locations in mummies:
            mumm = Mummy(self, mummies[mummy_locations], mummy_locations)
            self.all_enemies.append(mumm)
            self.all_sprites.add(mumm)

        for scorp_locations in scorpions:
            scorp = Scorpion(self, scorpions[scorp_locations], scorp_locations)
            self.all_enemies.append(scorp)
            self.all_sprites.add(scorp)

        # for undo
        self.turn = 0
        self.moving_entities = 0
        self.killed_sprites = {}

    def new_adventure(self, size, startpos, goal, mummies, scorpions, traps, obstacles):
        # start a new game
        self.sprite_args = (size, startpos, goal, mummies, scorpions, traps, obstacles)
        self.replace_sprites()

        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()

        if self.moving_entities == len(self.all_enemies):
            self.moving_entities = 0
            self.player.moved = False
        
        enemy_coords = [enemy.coords for enemy in self.all_enemies]
        rep_coords = self.same_coords(enemy_coords)

        if self.player.coords in set(self.death_zones) or self.player.coords in set(enemy_coords):
            self.game_winner = "enemy"

            self.show_death_screen()

        elif len(rep_coords) > 0:
            fighting_areas = {}

            for rep_coord in rep_coords:
                fighting_areas[rep_coord] = []
            for index in range(len(enemy_coords)):
                if enemy_coords[index] in set(rep_coords):
                    fighting_areas[enemy_coords[index]].append(self.all_enemies[index])

            self.fight(fighting_areas)

        elif self.player.coords == self.finish[0]:
            self.game_winner = "player"

            self.all_sprites.update()
            pygame.display.flip()
            steps = 10
            if self.finish[1] == "left":
                for _ in range(math.ceil((self.rect_width / 2) / steps)):
                    self.all_sprites.draw(self.screen)
                    pygame.display.flip()
                    self.player.pos.x -= steps
                    self.player.rect.topleft = self.player.pos
                    time.sleep(0.1)
            elif self.finish[1] == "right":
                for _ in range(math.ceil((self.rect_width / 2) / steps)):
                    self.all_sprites.draw(self.screen)
                    pygame.display.flip()
                    self.player.pos.x += steps
                    self.player.rect.topleft = self.player.pos
                    time.sleep(0.1)
            elif self.finish[1] == "top":
                for _ in range(math.ceil((self.rect_height / 2) / steps)):
                    self.all_sprites.draw(self.screen)
                    pygame.display.flip()
                    self.player.pos.y -= steps
                    self.player.rect.topleft = self.player.pos
                    time.sleep(0.1)
            elif self.finish[1] == "bottom":
                for _ in range(math.ceil((self.rect_height / 2) / steps)):
                    self.all_sprites.draw(self.screen)
                    pygame.display.flip()
                    self.player.pos.y += steps
                    self.player.rect.topleft = self.player.pos
                    time.sleep(0.1)
            up_next = self.up_level()
            if up_next:
                self.show_win_screen()
            else:
                self.show_end_screen()

    def events(self):
        # Game Loop - events
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                if self.playing:
                    for sprite in self.all_sprites:
                        sprite.kill()
                    self.playing = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.replace_sprites()
                elif event.key == pygame.K_u:
                    self.undo_game()
                elif event.key == pygame.K_ESCAPE:
                    # print (self.constraints)
                    screen = Tk().wm_withdraw() #to hide the main window
                    messagebox.showinfo("Showing Solution","This feature is still unpolished, but it works\nPress OK to continue...")

                    self.solve_maze(self.player.coords, self.all_enemies, 0)
                    # check all solutions
                    if len(self.solutions) == 0:
                        messagebox.showinfo("Solution Not Found!","This Maze is Impossible!!!")
                    else:
                        shortest = self.solutions[0]
                        for i in self.solutions:
                            if len(self.solutions[i]) < len(shortest):
                                shortest = self.solutions[i]
                        messagebox.showinfo(f"{len(self.solutions)} Solutions Found!", f"The shortest solution is...\n{shortest}")
                    # print (self.solutions)

    def draw(self):
        # Game Loop - draw
        self.screen.fill(crease_color_theme)

        self.all_sprites.draw(self.screen)

        pygame.display.flip()

    def package_ctc(self, list_of_classes):
        new_list = []

        for thing in list_of_classes:
            new_list.append({
                "Class": type(thing),
                "Typing": thing.typing,
                "Coordinates": thing.coords
            })
        return new_list

    def same_coords(self, coords):
        repeat = set()
        seen = set()
        for coord in coords:
            if coord in seen:
                repeat.add(coord)
            seen.add(coord)
        return list(repeat)

    def revive(self, list_of_patients):
        for patient in list_of_patients:
            self.all_enemies.append(patient)
            self.all_sprites.add(patient)
            # patient.undo()

    def fight(self, to_fight):
        POWER = {
            (Mummy, "red"): 4,
            (Mummy, "normal"): 3,
            (Scorpion, "red"): 2,
            (Scorpion, "normal"): 1
            }
    
        for arena in to_fight:
            arena_powers = []
            for i in range(len(to_fight[arena])):
                arena_powers.append(POWER[type(to_fight[arena][i]), to_fight[arena][i].typing])

            strongest = max(arena_powers)
            no_alive = True

            self.killed_sprites[self.turn] = [] # {}
            for i in range(len(to_fight[arena])):
                candidate_power = POWER[type(to_fight[arena][i]), to_fight[arena][i].typing]
                if candidate_power == strongest and no_alive:
                    no_alive = False
                else:
                    # PIN ---- Sprite Freeze Shot
                    # self.killed_sprites[self.turn][to_fight[arena][i]] = {
                    #     "Typing" : to_fight[arena][i].typing,
                    #     "Pos_Death" : (to_fight[arena][i].x, to_fight[arena][i].y),
                    #     "History": to_fight[arena][i].prev_moves
                    #     }

                    self.killed_sprites[self.turn].append(to_fight[arena][i])

                    self.all_enemies.remove(to_fight[arena][i])
                    to_fight[arena][i].kill()

    def add_constraints(self, coords, side):
        if coords not in set(self.constraints[side]):
            self.constraints[side].append(coords)

    def place_goal(self, side, x, y, w, h, coords):
        if side == "left":
            self.all_sprites.add(Side(self, goal_color, (x - self.space_x,  y - self.space_y, self.space_x, h + self.space_y)))
        elif side == "right":
            self.all_sprites.add(Side(self, goal_color, (x + w - self.space_x,  y - self.space_y, self.space_x, h + self.space_y)))
        elif side == "top":
            self.all_sprites.add(Side(self, goal_color, (x - self.space_x,  y - self.space_y, w  + self.space_x, self.space_y)))
        elif side == "bottom":
            self.all_sprites.add(Side(self, goal_color, (x - self.space_x,  y + h - self.space_y, w  + self.space_x, self.space_y)))

    def add_obstacle(self, sides, x, y, w, h, record, x_cord, y_cord):
        for side in sides:
            if side == "left":
                # pygame.draw.line(self.screen, obby_color, (x - self.space_x * 0.57,  y - self.space_y), (x - self.space_x * 0.57, y + h), math.ceil(self.space_x)) # + self.space_y
                self.all_sprites.add(Side(self, obby_color, (x - self.space_x,  y - self.space_y, self.space_x, h + self.space_y)))
                if record:
                    self.add_constraints((x_cord, y_cord), "left")
                    self.add_constraints((x_cord - 1, y_cord), "right")
            elif side == "right":
                # pygame.draw.line(self.screen, obby_color, (x + w - self.space_x * 0.57,  y - self.space_y), (x + w - self.space_x * 0.57, y + h), math.ceil(self.space_x)) #  + self.space_y
                self.all_sprites.add(Side(self, obby_color, (x + w - self.space_x,  y - self.space_y, self.space_x, h + self.space_y)))
                if record:
                    self.add_constraints((x_cord, y_cord), "right")
                    self.add_constraints((x_cord + 1, y_cord), "left")
            elif side == "top":
                # pygame.draw.line(self.screen, obby_color, (x - self.space_x,  y - self.space_y * 0.57), (x + w, y - self.space_y * 0.57), math.ceil(self.space_y)) # + self.space_x
                self.all_sprites.add(Side(self, obby_color, (x - self.space_x,  y - self.space_y, w  + self.space_x, self.space_y)))
                if record:
                    self.add_constraints((x_cord, y_cord), "top")
                    self.add_constraints((x_cord, y_cord - 1), "bottom")
            elif side == "bottom":
                # pygame.draw.line(self.screen, obby_color, (x - self.space_x,  y + h - self.space_y * 0.57), (x + w, y + h - self.space_y * 0.57), math.ceil(self.space_y)) # + self.space_x
                self.all_sprites.add(Side(self, obby_color, (x - self.space_x,  y + h - self.space_y, w  + self.space_x, self.space_y)))
                if record:
                    self.add_constraints((x_cord, y_cord), "bottom")
                    self.add_constraints((x_cord, y_cord + 1), "top")

    def undo_game(self):
        self.turn -= 1

        self.game_winner = None

        if self.turn + 1 in self.killed_sprites:
            self.revive(self.killed_sprites[self.turn + 1])

        for thing in self.all_enemies:
            thing.undo()
        self.player.undo()

    def show_start_screen(self):
        if self.show_start:
            self.clickable_sprites = pygame.sprite.Group()

            height = self.py_height * (0.15)
            width = self.py_width * (0.8)
            font_size = math.ceil(height * (0.5))

            # start_opt = 0.4
            # opt_inc = 0.2

            # adv_button = Button(self, "Adventure Mode", width, height, self.py_width >> 1, ((self.py_height * start_opt) + math.ceil(height/2)), (0, 0, 0), font_size, (255, 255, 255))
            # create_button = Button(self, "Creative Mode", width, height, self.py_width >> 1, ((self.py_height * (start_opt + opt_inc)) + math.ceil(height/2)), (0, 0, 0), font_size, (255, 255, 255))
            # self.clickable_sprites.add(adv_button)
            # self.clickable_sprites.add(create_button)

            adv_button = Button(self, "Adventure Mode", width, height, self.py_width >> 1, (self.py_height >> 1) + math.ceil(height/2), (0, 0, 0), font_size, (255, 255, 255))
            self.clickable_sprites.add(adv_button)

            # game splash/start screen
            self.screen.fill(open_death_bg)
            # self.draw_text(TITLE, font_size << 1, (255, 255, 255), self.py_width >> 1, font_size)
            self.draw_text(TITLE, font_size << 1, (255, 255, 255), self.py_width >> 1, (self.py_height >> 1) * (0.5))
            self.clickable_sprites.draw(self.screen)

            pygame.display.flip()

            # self.version = self.wait_for_click({adv_button: "Adventure", create_button: "Creative"})
            self.version = self.wait_for_click({adv_button: "Adventure"})

    def show_death_screen(self):
        # game over/continue
        if not self.running:
            return

        height = self.py_height * (0.15)
        width = self.py_width * (0.8)
        font_size = math.ceil(height * (0.5))

        start_opt = 0.35
        opt_inc = 0.175

        undo_button = Button(self, "Undo", width, height, self.py_width >> 1, ((self.py_height * (start_opt)) + math.ceil(height/2)), (0, 0, 0), font_size, (255, 255, 255))
        retry_button = Button(self, "Retry", width, height, self.py_width >> 1, ((self.py_height * (start_opt + opt_inc)) + math.ceil(height/2)), (0, 0, 0), font_size, (255, 255, 255))
        back_button = Button(self, "Main Menu", width, height, self.py_width >> 1, ((self.py_height * (start_opt + (opt_inc * 2))) + math.ceil(height/2)), (0, 0, 0), font_size, (255, 255, 255))        
        self.clickable_sprites.add(undo_button)
        self.clickable_sprites.add(retry_button)
        self.clickable_sprites.add(back_button)

        # game death screen
        self.screen.fill(open_death_bg)
        self.draw_text("Game Over!", font_size << 1, (255, 255, 255), self.py_width >> 1, font_size << 1)
        self.clickable_sprites.draw(self.screen)

        pygame.display.flip()

        choice = self.wait_for_click({undo_button: "Undo", retry_button: "Retry", back_button: "Back"})

        if choice == "Undo":
            self.undo_game()
            self.run()
        elif choice == "Retry":
            self.replace_sprites()
            self.run()
        elif choice == "Back":
            for sprite in self.all_sprites:
                sprite.kill()
            self.playing = False
            # self.show_start_screen()

    def show_win_screen(self):
        height = self.py_height * (0.15)
        width = self.py_width * (0.8)
        font_size = math.ceil(height * (0.5))

        next_button = Button(self, "Next Level", width, height, self.py_width >> 1, (self.py_height >> 1) + math.ceil(height/2), (0, 0, 0), font_size, (255, 255, 255))
        self.clickable_sprites.add(next_button)

        # game splash/start screen
        self.screen.fill(open_death_bg)
        self.draw_text("You have escaped!", font_size << 1, (255, 255, 255), self.py_width >> 1, (self.py_height >> 1) * (0.5))
        self.clickable_sprites.draw(self.screen)

        pygame.display.flip()

        a = self.wait_for_click({next_button: "Next"})

        if a == "Next":
            self.show_start = False
            self.playing = False

    def show_end_screen(self):
        height = self.py_height * (0.15)
        width = self.py_width * (0.8)
        font_size = math.ceil(height * (0.5))

        # game splash/start screen
        self.screen.fill(open_death_bg)
        self.draw_text("You have defeated the game!", font_size << 1, (255, 255, 255), self.py_width >> 1, (self.py_height >> 1) * (0.5))

        pygame.display.flip()

        not_done = True
        while not_done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    for sprite in self.all_sprites:
                        sprite.kill()
                    self.playing = False
                    self.running = False
                    not_done = False

    def wait_for_click(self, buttons):
        to_return = 0
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    try:
                        for sprite in self.all_sprites:
                            sprite.kill()
                        self.playing = False
                    except AttributeError:
                        pass
                    waiting = False
                    self.running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()

                    clicked_sprites = [s for s in self.clickable_sprites if s.rect.collidepoint(pos)]
                    for s in clicked_sprites:
                        to_return = buttons[s]
                        self.clickable_sprites.empty()
                        waiting = False
        return to_return

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def current_level(self):
        os.chdir(".\\main")
        if os.path.exists("Level.txt") == False:
            f = open("Level.txt", "w+")
            f.write("1")
            lvl = 1
        else:
            f = open("Level.txt", "r")
            lvl = int(f.readline())
        f.close()
        os.chdir("..")

        return lvl

    def up_level(self):
        total_levels = len(BUILT_LVLS)
        current_level = self.current_level()

        os.chdir(".\\main")
        
        f = open("Level.txt", "r")
        lvl = int(f.readline())
        f.close()

        if lvl + 1 <= total_levels:
            f = open("Level.txt", "w")
            f.write(str(lvl + 1))
            f.close()

            os.chdir("..")
            return True
        else:
            os.chdir("..")
            return False

    def start_level(self):
        current_level = self.current_level()
        lvl = BUILT_LVLS[current_level]
        return (lvl["Size"], lvl["Start"], lvl["End"], lvl["Mummies"], lvl["Scorpions"], lvl["Traps"], lvl["Obstacles"])

    ### --- ALGO TERRITORY --- ###
    # a = [
    #     {
    #         "Class": Mummy,
    #         "Typing": "red",
    #         "Coordinates": (1, 2)
    #     }
    # ]
    # Executing => self.solve_maze(self.player.coords, a, 0)

    def to_dict(self, dict_list, coords):
        new_dict = {}
        for i in range(len(dict_list)):
            new_dict[i] = dict_list[i]

        new_dict["Player Coords"] = coords
        return new_dict

    def imaginary_fight(self, to_fight, people):
        POWER = {
            (Mummy, "red"): 4,
            (Mummy, "normal"): 3,
            (Scorpion, "red"): 2,
            (Scorpion, "normal"): 1
            }
    
        for arena in to_fight:
            arena_powers = []
            for i in range(len(to_fight[arena])):
                arena_powers.append(POWER[type(to_fight[arena][i]), to_fight[arena][i].typing])

            strongest = max(arena_powers)
            no_alive = True

            for i in range(len(to_fight[arena])):
                candidate_power = POWER[type(to_fight[arena][i]), to_fight[arena][i].typing]
                if candidate_power == strongest and no_alive:
                    no_alive = False
                else:
                    people.remove(to_fight[arena][i])

    def game_state(self, player_pos, enemies, enemy_coords):
        rep_coords = self.same_coords(enemy_coords)

        if len(rep_coords) > 0:
            fighting_areas = {}

            for rep_coord in rep_coords:
                fighting_areas[rep_coord] = []
            for index in range(len(enemy_coords)):
                if enemy_coords[index] in set(rep_coords):
                    fighting_areas[enemy_coords[index]].append(enemies[index])

            self.imaginary_fight(fighting_areas, enemies)

        if player_pos in set(self.death_zones) or player_pos in set(enemy_coords):
            return "enemy"
        elif player_pos == self.finish[0]:
            return "player"
        else:
            return None

    def move(self, coords, move_direction):
        x, y = coords

        if move_direction == "left":
            x -= 1
        elif move_direction == "right":
            x += 1
        elif move_direction == "top":
            y -= 1
        elif move_direction == "bottom":
            y += 1
        
        return (x, y)
    
    def find_possible_moves(self, current_coords):
        all_moves = ["left", "right", "top", "bottom", "idle"]

        # if in border
        x, y = current_coords
        if x == 1:
            all_moves.remove("left")
        elif x == self.numx_rect:
            all_moves.remove("right")
        if y == 1:
            all_moves.remove("top")
        elif y == self.numy_rect:
            all_moves.remove("bottom")

        # other obstacles
        all_moves_2loop = all_moves[:]
        for move in all_moves_2loop:
            if move != "idle":
                if current_coords in set(self.constraints[move]):
                    all_moves.remove(move)

        return all_moves

    def solve_maze(self, player_coords, enemies, depth, prev_situations = None):
        # tree-based algorithm --- based on the minimax algorithm, a customized variation

        if prev_situations is None:
            prev_situations = []

        # Setup
        enemy_coords = [enemy.coords for enemy in enemies]

        # if game ended
        if depth == 0:
            self.path = []
            self.solutions = {}
            # check game winner
            game_state = self.game_winner
        else:
            #check game winner
            game_state = self.game_state(player_coords, enemies, enemy_coords)

        if game_state != None:
            return ALGO_SCORE[game_state]

        enemies = self.package_ctc(enemies)

        # check if you have been here before (infinite loop prevention)
        current_situation = self.to_dict(enemies, player_coords)
        if current_situation in prev_situations:
            return ALGO_SCORE["enemy"]
        else:
            prev_situations.append(current_situation)

        best_score = 0
        # all possible moves
        nodes = self.find_possible_moves(player_coords)

        for child in nodes:
            if len(self.path) == depth:
                self.path.append(child)
            else:
                self.path[depth] = child

            new_player_coords = self.move(player_coords, child)

            # a = input()
            # if a == "y":
            #     print (self.constraints)
            # elif a == "test":
            #     print ((4, 3) in self.constraints["top"])
            # print (depth)
            # print (player_coords)
            # print (child) #, new_player_coords)
            # print ()
            # time.sleep(3)

            new_enemies = []
            # move enemies
            for enemy in enemies:
                con = enemy["Class"](self, enemy["Typing"], enemy["Coordinates"])
                con.movement(False, new_player_coords)
                
                new_enemies.append(con)

            # if nothing happened when idle
            if child == "idle" and enemies == self.package_ctc(new_enemies):
                return ALGO_SCORE["enemy"]

            score = self.solve_maze(new_player_coords, new_enemies, depth + 1, prev_situations)

            # if win
            if score == ALGO_SCORE["player"]:
                # print ("-------------------")
                # filter for spam paths --- check if it really solves problem
                test_player_coords = self.player.coords
                for move in self.path:
                    test_player_coords = self.move(test_player_coords, move)
                if test_player_coords == self.finish[0]:
                    # [:] means create another copy to prevent one edit from one list transfer to another
                    self.solutions[len(self.solutions)] = self.path[:]
                best_score = score

            self.path.pop(depth)

            # print (self.path)
            # print (self.solutions)
            # print ()

        return best_score

    ### --- ALGO TERRITORY --- ###        

def new_game():
    Mummy_Maze = Game()
    while Mummy_Maze.running:
        Mummy_Maze.show_start_screen()
        
        if Mummy_Maze.version == "Adventure":
            size, startpos, goal, mummies, scorpions, traps, obstacles = Mummy_Maze.start_level()
            Mummy_Maze.new_adventure(size, startpos, goal, mummies, scorpions, traps, obstacles)

        # Mummy_Maze.show_death_screen()

    pygame.quit()

if __name__ == "__main__":
    new_game()










