from sprites.assets.tile import Tile
from sprites.assets.side import Side
from sprites.entities.mummy import Mummy
from sprites.entities.scorpion import Scorpion
from sprites.entities.player import Player
import pygame

class Loader():
    def parse_cell(self, cell):
        ''' Return a dictionary representation of the cell '''
        # If empty
        if cell is None or cell == "":
            return {"tile_type": "default"}

        # Guide in game_attributes.py
        # Examples
        # trap:[lr](mummy-normal)
        # goal@r:[tb](scorpion-red)
        # [rt]

        # Sub dictionaries
        # Note: only one entity
        tile = {}

        # Separate tile_type and 'stuff' in tile
        cell_info = cell.split(":")

        # If not properly split
        if len(cell_info) == 1:
            # If it's the right side (or 'stuff' in tile)
            if "(" in cell_info[0]:
                # Put default:default on the left side for proper unpacking
                cell_info.insert(0, "default")

            # If it's the left side (or tile_type)
            else:
                # Put default:None on the right side for proper unpacking
                cell_info.append(None)

        # Unpack list
        tile_type, tile_objects = cell_info

        # Parse tile_type
        # If there is a need for splitting
        if "@" in tile_type:
            tile_type, tile_type_direction = tile_type.split("@")
            # Add into the dictionary
            tile["tile_type_direction"] = tile_type_direction

        # Either way, add the tile_type
        tile["tile_type"] = tile_type

        # Parse tile_objects
        # If None
        if tile_objects is None:
            # There will no longer be anything to be added to dictionary so return
            return tile

        def inside(left, right, string):
            try:
                return string[string.index(left) + 1:string.index(right)]
            except ValueError:
                return None

        obstacle_directions = inside("[", "]", tile_objects)
        entity_race = inside("(", ")", tile_objects)

        # Add to dictionary
        if obstacle_directions is not None:
            tile["obstacles"] = obstacle_directions

        # If there is no entity
        if entity_race is None:
            return tile

        # Parse entity_race
        # Initialize default values
        entity_variant = "normal"

        # If there is a need to split
        if "-" in entity_race:
            entity_race, entity_variant = entity_race.split("-")

        # Add to dictionary
        tile["entity"] = {}
        tile["entity"]["race"] = entity_race
        tile["entity"]["variant"] = entity_variant
        return tile


    def add_tile_side(self, sides, color, x, y, tile_width, tile_height, space_x, space_y, is_obstacle=False, x_coordinate=None, y_coordinate=None):
        ''' Add tile side, meant to be used by self.load_level_sprites '''
        for side in sides:
            if side == "l":
                self.all_sprites.add(Side(self, color, x - space_x,  y - space_y, space_x, 2*space_y + tile_height))
                # If it's an obstacle, add constraints
                if is_obstacle:
                    # If coordinates is not given
                    if x_coordinate is None or y_coordinate is None:
                        raise Exception("Trying to add constraints with unknown coordinates")
                    pass
                    
            elif side == "r":
                self.all_sprites.add(Side(self, color, x + tile_width,  y - space_y, space_x, 2*space_y + tile_height))
                # If it's an obstacle, add constraints
                if is_obstacle:
                    # If coordinates is not given
                    if x_coordinate is None or y_coordinate is None:
                        raise Exception("Trying to add constraints with unknown coordinates")
                    pass

            elif side == "t":
                self.all_sprites.add(Side(self, color, x - space_x,  y - space_y, 2*space_x + tile_width, space_y))
                # If it's an obstacle, add constraints
                if is_obstacle:
                    # If coordinates is not given
                    if x_coordinate is None or y_coordinate is None:
                        raise Exception("Trying to add constraints with unknown coordinates")
                    pass

            elif side == "b":
                self.all_sprites.add(Side(self, color, x - space_x,  y + tile_height, 2*space_x + tile_width, space_y))
                # If it's an obstacle, add constraints
                if is_obstacle:
                    # If coordinates is not given
                    if x_coordinate is None or y_coordinate is None:
                        raise Exception("Trying to add constraints with unknown coordinates")
                    pass


    def load_level_sprites(self, level_state):
        ''' Add all level sprites to a Group to be drawn '''
        self.all_sprites = pygame.sprite.Group()

        # Attributes
        level_height = len(level_state)
        # Under the assumption that it is a quadrilateral
        level_width = len(level_state[0])

        # For this, I want the cells to be square, and I want it to fill either screen dimension
        cell_width = cell_height = min(self.screen_width // level_width, self.screen_height // level_height)

        # Initial (x, y) to centralize
        # (Total / 2) - (Grid / 2)
        initial_x = (self.screen_width / 2) - (cell_width * level_width / 2)
        initial_y = (self.screen_height / 2) - (cell_height * level_height / 2)
        # Distance between each tile
        space_x = cell_width * 0.08
        space_y = cell_height * 0.08

        # Go through each cell of the level
        for y_index, row in enumerate(level_state):
            for x_index, cell in enumerate(row):
                # Get coordinates
                x_coordinate = x_index + 1
                y_coordinate = y_index + 1

                cell_information = self.parse_cell(cell)
                # I didn't know this can work even if I call the lambda function outside of the function it's defined in
                # Even if the numbers used is local
                self.get_coords = lambda x, y: (initial_x + (cell_width * (x - 1)) + (space_x / 2), initial_y + (cell_height * (y - 1)) + (space_y / 2))
                x, y = self.get_coords(x_coordinate, y_coordinate)
                # Give spacing
                tile_width = cell_width - space_x
                tile_height = cell_height - space_y

                # Draw tile
                self.all_sprites.add(Tile(self, x, y, tile_width, tile_height, (x_coordinate, y_coordinate), cell_information["tile_type"]))
                
                # Add borders
                # Left
                if x_coordinate == 1:
                    self.add_tile_side("l", self.OBSTACLE_COLOR, x, y, tile_width, tile_height, space_x, space_y, True, x_coordinate, y_coordinate)
                # Right
                elif x_coordinate == level_width:
                    self.add_tile_side("r", self.OBSTACLE_COLOR, x, y, tile_width, tile_height, space_x, space_y, True, x_coordinate, y_coordinate)
                # Top
                if y_coordinate == 1:
                    self.add_tile_side("t", self.OBSTACLE_COLOR, x, y, tile_width, tile_height, space_x, space_y, True, x_coordinate, y_coordinate)
                # Bottom
                elif y_coordinate == level_height:
                    self.add_tile_side("b", self.OBSTACLE_COLOR, x, y, tile_width, tile_height, space_x, space_y, True, x_coordinate, y_coordinate)
                
                # Add non-border obstacles
                if "obstacles" in cell_information:
                    self.add_tile_side(cell_information["obstacles"], self.OBSTACLE_COLOR, x, y, tile_width, tile_height, space_x, space_y, True, x_coordinate, y_coordinate)

                # If it's a tile_type with direction (but for now it's only goal)
                if cell_information["tile_type"] == "goal":
                    self.add_tile_side(cell_information["tile_type_direction"], self.GOAL_COLOR, x, y, tile_width, tile_height, space_x, space_y)

                # Add entities
                # No entity
                if "entity" not in cell_information:
                    continue

                if cell_information["entity"]["race"] == "player":
                    # Add player
                    self.all_sprites.add(Player(self, tile_width, tile_height, x, y, (x_coordinate, y_coordinate)))

