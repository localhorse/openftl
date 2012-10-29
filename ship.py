import pygame
from constants import *

if __name__ == "__main__":
    pass

class Ship(pygame.sprite.Sprite):

    def __init__(self, ship_type, pos):

        pygame.sprite.Sprite.__init__(self)

        # os.join(), also check proper ship type --FIXME
        self._hull_filename = "./resources/img/ship/%s_base.png" % ship_type
        self.image = pygame.image.load(self._hull_filename).convert_alpha()

        self._cur_x, self._cur_y = pos
        # just grab the width and height
        (self._ship_width, self._ship_height, _, _) = self.image.get_rect()
        self.rect = self.bounding_box()

        self._rooms_filename = "./resources/data/%s.txt" % ship_type

        # prepare the empty room tile (just a beige box with grey
        # border)
        self._tile_img = pygame.Surface(pygame.Rect((0, 0, TILE_WIDTH, TILE_HEIGHT)).size, flags=pygame.SRCALPHA).convert_alpha()
        self._tile_img.fill(GRID_COLOR)
        x1, y1, x2, y2 = self._tile_img.get_rect()
        x1 += 1
        y1 += 1
        x2 -= 1
        y2 -= 1
        pygame.draw.rect(self._tile_img, ROOM_COLOR, pygame.Rect((x1, y1, x2, y2)))
        
        # these need to be loaded from file... what is hardcoded here
        # should be in kestral.txt
        self._x_offset = 0
        self._y_offset = 2

        self._rooms = self.load_rooms()

    def bounding_box(self):
        return pygame.Rect(self._cur_x, self._cur_y, self._ship_width, self._ship_height)

    def update(self):

        # draw the rooms to the proper place (later we'll avoid doing
        # this every time) --FIXME
        for room in self._rooms:
            temp_x = (room['x'] + self._x_offset) * TILE_WIDTH
            temp_y = (room['y'] + self._y_offset) * TILE_HEIGHT
            temp_x += self._cur_x
            temp_y += self._cur_y
            self.image.blit(room['img'], (temp_x, temp_y), area=None, special_flags=BLEND_TYPE)

    def load_rooms(self):

        rooms_file = open(self._rooms_filename, "r")
        rooms_list = []
        
        lines = rooms_file.readlines()

        for line in lines:
            temp = line.strip()
            line = temp
        
        rooms_file.close()

        for index, line in enumerate(lines):
            if "ROOM" in line:
                room_id = int(lines[index + 1])
                room_x = int(lines[index + 2])
                room_y = int(lines[index + 3])
                room_width = int(lines[index + 4])
                room_height = int(lines[index + 5])

                rooms_list.append({'id': room_id, 'x': room_x, 'y': room_y, 'width': room_width, 'height': room_height, 'img': pygame.Surface((room_width * TILE_WIDTH, room_height * TILE_HEIGHT), flags=pygame.SRCALPHA).convert_alpha()})

        for room in rooms_list:

            for index in range(0, room['width']):

                temp_x = index * TILE_WIDTH
                temp_y = 0

                room['img'].blit(self._tile_img, (temp_x, temp_y), area=None, special_flags=BLEND_TYPE)

            for index in range(0, room['height']):

                temp_x = 0
                temp_y = index * TILE_HEIGHT
                
                room['img'].blit(self._tile_img, (temp_x, temp_y), area=None, special_flags=BLEND_TYPE)

        return rooms_list

        
