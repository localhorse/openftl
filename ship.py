import pygame
from constants import *

if __name__ == "__main__":
    pass

class Ship(pygame.sprite.Sprite):

    def __init__(self, ship_type, pos):

        pygame.sprite.Sprite.__init__(self)

        # os.join(), also check proper ship type
        self._hull_file = "./resources/img/ship/%s_base.png" % ship_type
        self._hull_img = pygame.image.load(self._hull_file).convert_alpha()

        self.image = self._hull_img

        self._cur_x, self._cur_y = pos
        # just grab the width and height
        (self._ship_width, self._ship_height, _, _) = self.image.get_rect()
        self.rect = self.bounding_box()

        self._rooms_file = "./resources/data/%s.txt" % ship_type

    def bounding_box(self):
        # return a rect with the actual drawn character in the center
        # (just thinking that we could just as easily return the image
        # rect, duh... not sure why I did this? take a look --FIXME)
        return pygame.Rect(self._cur_x, self._cur_y, self._ship_width, self._ship_height)

    def update(self):
        # we'd update the position here if it moved
        pass
