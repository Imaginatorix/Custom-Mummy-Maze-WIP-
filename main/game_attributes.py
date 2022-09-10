TITLE: str = "Mummy Maze"
FPS: int = 8
FONT_NAME: str = "arial"

# Define colors
# Game assets
TILE_COLOR: tuple = (185, 156, 107)
OBSTACLE_COLOR: tuple = (169, 169, 169)
GOAL_COLOR: tuple = (0, 255, 0)
# Screen backgrounds
START_SCREEN_COLOR: tuple = (0, 155, 155)
DEATH_SCREEN_COLOR: tuple = (0, 0, 0)
GAME_BACKGROUND_COLOR: tuple = (180, 151, 102)
# Sprites
PLAYER_COLOR: tuple = (181, 101, 29)
NORMAL_MUMMY_COLOR: tuple = (255, 255, 255)
RED_MUMMY_COLOR: tuple = (255, 69, 0)
NORMAL_SCORPION_COLOR: tuple = (176, 141, 87)
RED_SCORPION_COLOR: tuple = (161, 61, 45)

ALGO_SCORE: dict = {
    "player" : 1,
    "enemy" : -1
}

'''
I got bored...
I will not continue it for now, maybe in the future.
Things to add left:
    Creative Mode (Click on cell, then if arrow (on direction put obstacle), if click + space, trap, if click + m, mummy, if click + s, scorpion)
    Gate + Key
'''

# "Type": "Visible"

# direction - left, right, top, bottom =repr> lrtb
# typeOfTile:[obstacles - which is direction](entity-variant)
# typeofTile - trap, goal@direction
# entity... variant =default> normal
# for each tile
# start can't have entity

# Examples
# trap:[lr](mummy-normal)
# goal@r:[tb](scorpion-red)
# [rt]

BUILT_LVLS: dict = {
    1: [["trap",           "trap",             None,    None, None    ],
        [None,             "[br](mummy-red)", None,    None, None    ],
        ["(scorpion-red)", None,               "(player)", None, None    ],
        [None,             None,               None,    None, None    ],
        [None,             None,               None,    None, "goal@r"]]
}

# BUILT_LVLS = {
#     1: {
#         "Size": (5, 5),
#         "Start": (3, 3),
#         "End": {
#             "Coordinates": (5, 5),
#             "Side": "right"
#         },
#         "Mummies": {(2, 2): "red"},
#         "Scorpions": {(1, 2): "red"},
#         "Traps": [(1, 1), (2, 1)],
#         "Obstacles": {
#             (2, 2): ["bottom", "right"]
#         }
#     },
    # 2: {"Size": (4, 4),
    #     "Start": (3, 3),
    #     "End": {
    #         "Coordinates": (1, 4),
    #         "Side": "right"
    #     },
    #     "Mummies": {(2, 2): "red"},
    #     "Scorpions": {(1, 1): "normal"},
    #     "Traps": [(1, 1), (2, 1)],
    #     "Obstacles": {
    #         (2, 2): ["bottom", "right"]
    #     }
    # },
    # # copy of a maze in the original mummy maze (Pyramid 15)
    # 3: {"Size": (10, 10),
    #     "Start": (9, 2),
    #     "End": {
    #         "Coordinates": (4, 10),
    #         "Side": "bottom"
    #     },
    #     "Mummies": {(9, 5): "normal"},
    #     "Scorpions": {(2, 1): "normal"},
    #     "Traps": [(7, 2)],
    #     "Obstacles": {
    #         (2, 1): ["left", "bottom"],
    #         (3, 2): ["left", "bottom"],
    #         (4, 2): ["bottom", "right"],
    #         (5, 2): ["bottom"],
    #         (6, 2): ["bottom", "right"],
    #         (7, 3): ["top", "bottom"],
    #         (8, 2): ["right"],
    #         (10, 2): ["top"],
    #         (4, 3): ["right"],
    #         (2, 4): ["left", "bottom"],
    #         (3, 4): ["bottom", "right"],
    #         (4, 5): ["left", "right"],
    #         (3, 6): ["left", "right"],
    #         (4, 7): ["left"],
    #         (2, 6): ["top"],
    #         (1, 8): ["top"],
    #         (2, 8): ["top", "bottom"],
    #         (3, 9): ["bottom"],
    #         (8, 4): ["bottom", "right"],
    #         (9, 5): ["left", "top"],
    #         (9, 6): ["bottom"],
    #         (8, 6): ["left", "top"],
    #         (7, 5): ["left"],
    #         (6, 7): ["top", "bottom"],
    #         (6, 8): ["left"],
    #         (6, 9): ["left"],
    #         (7, 8): ["bottom", "right"],
    #         (9, 8): ["left", "top"],
    #         (10, 9): ["bottom"],
    #         (8, 10): ["left"]
    #     }
    # }
# }


