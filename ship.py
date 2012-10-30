import pygame
from constants import *
from door import Door

class Ship(pygame.sprite.Sprite):

    # the ship placement can only be in increments of (TILE_WIDTH,
    # TILE_HEIGHT) so we'll need pos to not actually be screen
    # coordinates
    def __init__(self, ship_type, pos):

        pygame.sprite.Sprite.__init__(self)

        # os.join(), also check proper ship type --FIXME
        self._hull_filename = "./resources/img/ship/%s_base.png" % ship_type
        self.image = pygame.image.load(self._hull_filename).convert_alpha()

        self._cur_x, self._cur_y = pos
        # just grab the width and height
        (self._ship_width, self._ship_height, _, _) = self.image.get_rect()
        self.rect = self.bounding_box()

        self._shipdata_filename = "./resources/data/%s.txt" % ship_type

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
        
        # somehow these aren't exactly right, they're not lining up
        # with the ship the way they do in FTL... although the rooms
        # are fine relative to each other, it must be the offsets
        # somehow
        self._x_offset, self._y_offset, self._vert_offset = self._load_offsets()

        # load the rooms from the data file
        self._rooms = self._load_rooms()

        # try loading the doors...
        self._doors = self._load_doors()

        # draw the rooms into the main ship graphic (not to the
        # screen)
        self._draw_rooms()

    def bounding_box(self):
        return pygame.Rect(self._cur_x * TILE_WIDTH, self._cur_y * TILE_HEIGHT, self._ship_width, self._ship_height)

    def update(self):
        pass

    # draw the rooms to the Sprite image surface
    def _draw_rooms(self):

        for room in self._rooms:
            temp_x = ((room['x'] + self._x_offset) * TILE_WIDTH) + self._cur_x * TILE_WIDTH
            temp_y = ((room['y'] + self._y_offset) * TILE_HEIGHT) + self._vert_offset + self._cur_y * TILE_HEIGHT

            # draw room
            self.image.blit(room['img'], (temp_x, temp_y), area=None, special_flags=BLEND_TYPE)

            # draw room borders

            temp_rect = room['img'].get_rect()
            x1, y1, x2, y2 = temp_rect

            x1 = temp_x
            y1 = temp_y

            x2 += x1
            y2 += y1
            
            pygame.draw.lines(self.image, (0, 0, 0), True, [(x1, y1), (x2, y1), (x2, y1), (x2, y2), (x2, y2), (x1, y2), (x1, y2), (x1, y1)], 2)

    # loads the x and y offsets from the data file... these values
    # describe how much the rooms are offset from (0, 0) of the ship
    # image
    def _load_offsets(self):

        ship_data = open(self._shipdata_filename, "r")
        lines = ship_data.readlines()
        ship_data.close()

        x_offset = 0
        y_offset = 0
        vertical = 0

        for index, line in enumerate(lines):
            temp = line.strip()
            line = temp
            if "X_OFFSET" in line:
                x_offset = int(lines[index + 1])
            if "Y_OFFSET" in line:
                y_offset = int(lines[index + 1])
            if "VERTICAL" in line:
                vertical = int(lines[index + 1])

        return (x_offset, y_offset, vertical)
            
    def _load_rooms(self):

        rooms_file = open(self._shipdata_filename, "r")
        rooms_list = []
        
        lines = rooms_file.readlines()
        rooms_file.close()
        
        for line in lines:
            temp = line.strip()
            line = temp

        # load each room from file
        for index, line in enumerate(lines):
            if "ROOM" in line:
                room_id = int(lines[index + 1])
                room_x = int(lines[index + 2])
                room_y = int(lines[index + 3])
                room_width = int(lines[index + 4])
                room_height = int(lines[index + 5])
                room_img = pygame.Surface((room_width * TILE_WIDTH, room_height * TILE_HEIGHT), flags=pygame.SRCALPHA).convert_alpha()

                rooms_list.append({'id': room_id, 'x': room_x, 'y': room_y, 'width': room_width, 'height': room_height, 'img': room_img})

        # draw the tiles into each room image
        for room in rooms_list:
            for width_index in range(0, room['width']):
                for height_index in range(0, room['height']):
                    temp_x = width_index * TILE_WIDTH
                    temp_y = height_index * TILE_HEIGHT
                    room['img'].blit(self._tile_img, (temp_x, temp_y), area=None, special_flags=BLEND_TYPE)

        return rooms_list

        
    def _load_doors(self):

        # the cost of loading this file every time is probably
        # trivial, but it would also be trivial to have it loaded and
        # parsed all in one shot --FIXME
        doors_file = open(self._shipdata_filename, "r")
        doors_list = []

        lines = doors_file.readlines()
        doors_file.close()

        for line in lines:
            temp = line.strip()
            line = temp

        # load each door from the file
        for index, line in enumerate(lines):
            if "DOOR" in line:
                door_x = int(lines[index + 1])
                door_y = int(lines[index + 2])
                # the room above or to the left of this door
                room_left = int(lines[index + 3])
                # the room below or to the right
                room_right = int(lines[index + 4])
                # if this is 0, the rooms connect vertically, if 1
                # they connect horizontally
                connect = int(lines[index + 5])
                # create a new Door object for each door found, this
                # will contain an animated sprite as well as the info
                # we just loaded from the file
                doors_list.append(Door(self.get_pos(), (door_x, door_y), room_left, room_right, connect, self._x_offset, self._y_offset, self._vert_offset))

        return doors_list

    def get_doors(self):
        return self._doors

    def get_pos(self):
        return (self._cur_x, self._cur_y)
        
if __name__ == "__main__":
    pass
