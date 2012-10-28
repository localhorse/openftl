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

        # not sure what the purpose of the offsets are?
        self._rooms_file = "./resources/data/%s.txt" % ship_type
        self._x_offset = 0
        self._y_offset = 2

        # this is actually going to be loaded from a file as well
        self._rooms = [{'id': 0, 'x': 14, 'y': 2, 'width': 1, 'height': 2, 'img': pygame.Surface(pygame.Rect((0, 0, TILE_WIDTH, TILE_HEIGHT)).size, flags=pygame.SRCALPHA).convert_alpha()}]
        self._rooms[0]['img'].fill(GRID_COLOR)
        x1, y1, x2, y2 = self._rooms[0]['img'].get_rect()
        x1 += 1
        y1 += 1
        x2 -= 1
        y2 -= 1
        pygame.draw.rect(self._rooms[0]['img'], ROOM_COLOR, pygame.Rect((x1, y1, x2, y2)))

    def bounding_box(self):
        # return a rect with the actual drawn character in the center
        # (just thinking that we could just as easily return the image
        # rect, duh... not sure why I did this? take a look --FIXME)
        return pygame.Rect(self._cur_x, self._cur_y, self._ship_width, self._ship_height)

    def update(self):

        # make sure any added rooms get drawn
        for room in self._rooms:

            for index in range(0, room['width']):
                temp_x = (room['x'] + self._x_offset + index) * TILE_WIDTH
                temp_y = (room['y'] + self._y_offset) * TILE_HEIGHT

                temp_x += self._cur_x
                temp_y += self._cur_y

                self._hull_img.blit(room['img'], (temp_x, temp_y), area=None, special_flags=BLEND_TYPE)

            for index in range(0, room['height']):
                temp_x = (room['x'] + self._x_offset) * TILE_WIDTH
                temp_y = (room['y'] + self._y_offset + index) * TILE_HEIGHT
                
                temp_x += self._cur_x
                temp_y += self._cur_y
                
                self._hull_img.blit(room['img'], (temp_x, temp_y), area=None, special_flags=BLEND_TYPE)

