TITLE = "Mummy Maze"
FPS = 8
FONT_NAME = "Arial"

# define colors
player_color = (181, 101, 29)
color_theme = (185, 156, 107)
crease_color_theme = (180, 151, 102)
obby_color = (169, 169, 169)
goal_color = (0, 255, 0)
open_death_bg = (0, 155, 155)
killer_color = (0, 0, 0)
red_mummy_color = (255, 69, 0)
white_mummy_color = (255, 255, 255)
normal_scorpion_color = (176, 141, 87)
red_scorpion_color = (161, 61, 45)

ALGO_SCORE = {
    "player" : 5,
    "enemy" : -5
}

'''
I got bored...
I will not continue it for now, maybe in the future.
Things to add left:
    Creative Mode (Click on cell, then if arrow (on direction put obstacle), if click + space, trap, if click + m, mummy, if click + s, scorpion)
    Gate + Key
'''

# "Type": "Visible"

BUILT_LVLS = {
    1: {
        "Size": (5, 5),
        "Start": (3, 3),
        "End": {
            "Coordinates": (5, 5),
            "Side": "right"
        },
        "Mummies": {(2, 2): "red"},
        "Scorpions": {(1, 2): "red"},
        "Traps": [(1, 1), (2, 1)],
        "Obstacles": {
            (2, 2): ["bottom", "right"]
        }
    },
    2: {"Size": (4, 4),
        "Start": (3, 3),
        "End": {
            "Coordinates": (1, 4),
            "Side": "right"
        },
        "Mummies": {(2, 2): "red"},
        "Scorpions": {(1, 1): "normal"},
        "Traps": [(1, 1), (2, 1)],
        "Obstacles": {
            (2, 2): ["bottom", "right"]
        }
    },
    # copy of a maze in the original mummy maze (Pyramid 15)
    3: {"Size": (10, 10),
        "Start": (9, 2),
        "End": {
            "Coordinates": (4, 10),
            "Side": "bottom"
        },
        "Mummies": {(9, 5): "normal"},
        "Scorpions": {(2, 1): "normal"},
        "Traps": [(7, 2)],
        "Obstacles": {
            (2, 1): ["left", "bottom"],
            (3, 2): ["left", "bottom"],
            (4, 2): ["bottom", "right"],
            (5, 2): ["bottom"],
            (6, 2): ["bottom", "right"],
            (7, 3): ["top", "bottom"],
            (8, 2): ["right"],
            (10, 2): ["top"],
            (4, 3): ["right"],
            (2, 4): ["left", "bottom"],
            (3, 4): ["bottom", "right"],
            (4, 5): ["left", "right"],
            (3, 6): ["left", "right"],
            (4, 7): ["left"],
            (2, 6): ["top"],
            (1, 8): ["top"],
            (2, 8): ["top", "bottom"],
            (3, 9): ["bottom"],
            (8, 4): ["bottom", "right"],
            (9, 5): ["left", "top"],
            (9, 6): ["bottom"],
            (8, 6): ["left", "top"],
            (7, 5): ["left"],
            (6, 7): ["top", "bottom"],
            (6, 8): ["left"],
            (6, 9): ["left"],
            (7, 8): ["bottom", "right"],
            (9, 8): ["left", "top"],
            (10, 9): ["bottom"],
            (8, 10): ["left"]
        }
    }
}


