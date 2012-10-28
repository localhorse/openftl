import pygame
from constants import *

if __name__ == "__main__":
    pass

class Ship():

    def __init__(self, ship_type, pos):

        self._background = None

        self._pos = pos

        # os.join(), also check proper ship type
        self._hull_file = "./resources/img/ship/%s_base.png" % ship_type
        self._hull_img = pygame.image.load(self._hull_file).convert_alpha()

        self._rooms_file = "./resources/data/%s.txt" % ship_type

    def draw(self, surface):
        surface.blit(self._hull_img, self._pos, special_flags=BLEND_TYPE)
        if not self._background:
            self._background = surface.copy()

    def get_hull_img(self):
        return self._background
