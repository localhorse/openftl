import pygame

ALIEN_WIDTH =  35
ALIEN_HEIGHT = 35
ALIEN_COLS = 16

TILE_WIDTH = 35
TILE_HEIGHT = 35

ROOM_COLOR = (230, 226, 219)
GRID_COLOR = (172, 169, 164)

DOWN = 0
RIGHT = 1
UP = 2
LEFT = 3

# 0, 1, 2, 3
MAX_ANIM_FRAME = 3

# stuff like speed, and the movement and animation delays shouldn't be
# here... they should be defined in the Person class (or subclass of
# it) in init() because there will be different speeds for different
# Persons.

SPEED = 1

##BLEND_TYPE = pygame.BLEND_ADD
BLEND_TYPE = 0
