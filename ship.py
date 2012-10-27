import pygame
from constants import *

if __name__ == "__main__":
    pass

class Ship():

    def __init__(self, type, pos):

        self._pos = pos

        # os.join(), also check proper ship type
        self._hull_file = "./resources/img/ship/%s_base.png" % (type)
        self._hull_img = pygame.image.load(self._hull_file).convert_alpha()

    def draw(self, surface, pos=0, rect=0):
        if rect:
            # only draw part of the ship
            surface.blit(self._hull_img, pos, rect, special_flags=BLEND_TYPE)
            print("*** %s ***" % rect)
        else:
            # draw it all
            surface.blit(self._hull_img, self._pos, special_flags=BLEND_TYPE)
        
