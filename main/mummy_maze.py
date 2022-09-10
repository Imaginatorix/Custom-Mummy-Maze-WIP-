# # Remove PyGame library message
# from os import environ
# environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import game_attributes as attr
from engine import solver, state
from methods import drawer, loader, screens
import pygame
import numpy
import time
import os
# doing quick messages
from tkinter import messagebox


class Mummy_Maze(drawer.Drawer, loader.Loader, screens.Screens):
    def __init__(self):
        pygame.init()

        # Attributes
        self.clock = pygame.time.Clock()
        self.FONT = pygame.font.match_font(attr.FONT_NAME)
        self.TITLE = attr.TITLE
        self.LEVELS = attr.BUILT_LVLS
        self.FPS = attr.FPS
        # Colors
        # Game assets
        self.TILE_COLOR = attr.TILE_COLOR
        self.OBSTACLE_COLOR = attr.OBSTACLE_COLOR
        self.GOAL_COLOR = attr.GOAL_COLOR
        # Screen backgrounds
        self.START_SCREEN_COLOR = attr.START_SCREEN_COLOR
        self.DEATH_SCREEN_COLOR = attr.DEATH_SCREEN_COLOR
        self.GAME_BACKGROUND_COLOR = attr.GAME_BACKGROUND_COLOR
        # Sprites
        self.PLAYER_COLOR = attr.PLAYER_COLOR
        self.NORMAL_MUMMY_COLOR = attr.NORMAL_MUMMY_COLOR
        self.RED_MUMMY_COLOR = attr.RED_MUMMY_COLOR
        self.NORMAL_SCORPION_COLOR = attr.NORMAL_SCORPION_COLOR
        self.RED_SCORPION_COLOR = attr.RED_SCORPION_COLOR

        # Get desktop dimensions
        desktopInfo = pygame.display.Info()
        # Display window has 1/2 width and 1/2 height of fill screen
        self.screen_width, self.screen_height = desktopInfo.current_w >> 1, desktopInfo.current_h >> 1
        # Create screen
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(self.TITLE)

        # Start Game
        self.start = True
        self.start_game()


    def start_game(self):
        ''' Start Game '''
        self.running = True
        while self.running:
            # Switch between screens
            # Non-Gaming Screen
            if self.start:
                # Initialize Game Mode
                self.game_mode = None
                # Choose Game Mode
                self.screens("start")
                # End Start Screen
                self.start = False

            # Playing/Game Screen
            # Play Game in Adventure Mode
            if self.game_mode == "Adventure":
                self.run_game(1)
            # Play Game in Creative Mode (create a level)
            elif self.game_mode == "Creative":
                pass

        # Destroy Screen
        pygame.quit()


    def run_game(self, level):
        ''' Game Loop '''
        self.playing = True
        self.game_state = self.LEVELS[level]
        self.reload_state = True
        while self.playing:
            self.clock.tick(self.FPS)
            self.game_events()
            self.game_updates()
            self.game_draw()


    def game_updates(self):
        ''' Game Loop - Update '''
        pass


    def game_events(self):
        ''' Game Loop - Events '''
        for event in pygame.event.get():
            # Check for closing window
            if event.type == pygame.QUIT:
                self.exit_game()
            # Key press
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and "l" in self.legal_moves:
                    self.game_state = state.result(self.game_state, "l")
                    self.reload_state = True
                elif event.key == pygame.K_RIGHT and "r" in self.legal_moves:
                    self.game_state = state.result(self.game_state, "r")
                    self.reload_state = True
                elif event.key == pygame.K_UP and "t" in self.legal_moves:
                    self.game_state = state.result(self.game_state, "t")
                    self.reload_state = True
                elif event.key == pygame.K_DOWN and "b" in self.legal_moves:
                    self.game_state = state.result(self.game_state, "b")
                    self.reload_state = True


    def game_draw(self):
        ''' Game Loop - Draw '''
        if self.reload_state == True:
            # Load everything
            self.load_level_sprites(self.game_state)
            # Check legal moves for less lag
            self.legal_moves = state.actions(self.game_state)
            # Terminate reload
            self.reload_state = False

        # Add background color
        self.screen.fill(self.GAME_BACKGROUND_COLOR)
        # Draw all sprites/ Draw level
        self.all_sprites.draw(self.screen)

        # Show on screen
        pygame.display.flip()


    def exit_game(self):
        ''' Exit all loops by making conditions False '''
        self.playing = False
        self.running = False


if __name__ == "__main__":
    Mummy_Maze()
