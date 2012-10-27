import pygame

SPRITE_WIDTH =  35
SPRITE_HEIGHT = 35
SPRITE_COLS = 16

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
