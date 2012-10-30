import pygame
from constants import *

class Door(pygame.sprite.Sprite):

    # again, this x, y position is not a screen pixel position but
    # rather a grid of TILE_WIDTH by TILE_HEIGHT sized tiles - we'll
    # do this eventually for everything but the Person class, it will
    # be easier to scale
    def __init__(self, ship_pos, pos, room_left, room_right, connect, x_offset, y_offset, vert_offset):
        
        self._cur_x, self._cur_y = pos        
        self._ship_x, self._ship_y = ship_pos

        self._frames = []
        frames = self._frames
        self._next_anim = 0
        self._anim_delay = 100
        self._anim_frame = 0

        self._x_offset = x_offset
        self._y_offset = y_offset
        self._vert_offset = vert_offset

        self._connect = connect

        pygame.sprite.Sprite.__init__(self)

        self._door_file = "./resources/img/effects/door_sheet.png"

        self._door_sheet = pygame.image.load(self._door_file).convert_alpha()

        # go through each column in the top rown and load all 5 door
        # positions
        for index in range(0, DOOR_FRAMES):
            temp_rect = pygame.Rect((index * TILE_WIDTH, 0),
                                    (TILE_WIDTH, TILE_HEIGHT))
            # loading both the yellow and the (upgraded) grey door
            frames.append((pygame.Surface(temp_rect.size, flags=pygame.SRCALPHA).convert_alpha(), pygame.Surface(temp_rect.size, flags=pygame.SRCALPHA).convert_alpha()))
            reg_surf, upg_surf = frames[len(frames) - 1]
            reg_surf.blit(self._door_sheet, (0, 0), temp_rect, special_flags=BLEND_TYPE)
            temp_rect = pygame.Rect((index * TILE_WIDTH, TILE_HEIGHT),
                                    (TILE_WIDTH, TILE_HEIGHT))
            upg_surf.blit(self._door_sheet, (0, 0), temp_rect, special_flags=BLEND_TYPE)

            if connect == VERTICAL:
                reg_surf = pygame.transform.rotate(reg_surf, 90)
                upg_surf = pygame.transform.rotate(upg_surf, 90)
                frames[len(frames) - 1] = (reg_surf, upg_surf)

        (self.image, _) = frames[0]
        self.rect = self.bounding_box()
            
    def update(self):
        self._test_anim()
        self._cur_frame()

    def _cur_frame(self):
        # this only needs its own method because later we'll need to
        # determine if we're drawing the regular or upgraded door
        (self.image, _) = self._frames[self._anim_frame]

    def _test_anim(self):
        cur_time = pygame.time.get_ticks()
        if self._next_anim < cur_time:
            self._anim_frame += 1
            if self._anim_frame >= DOOR_FRAMES:
                self._anim_frame = 0
            self._next_anim = cur_time + self._anim_delay
        # Group.update() doesn't seem concerned with redrawing this
        # unless the rect has changed!
        self.rect = self.bounding_box()

    def bounding_box(self):
        temp_x = (self._ship_x + self._cur_x + self._x_offset) * TILE_WIDTH
        temp_y = ((self._ship_y + self._cur_y + self._y_offset) * TILE_HEIGHT) + self._vert_offset
        # it would appear that in most cases the info in the data file
        # for the doors (specifically the ids of rooms the door is
        # connecting to) is not actually needed... in most cases the
        # doors belong to the room either directly above (in the case
        # of horizontal doors) or directly to the left of (in the case
        # of vertical) the door. I expect that there may be ships
        # where there are 2 vertical or 2 horizontal doors per room,
        # in which case it would be more ambiguous... this will have
        # to be changed --FIXME
        if self._connect == HORIZONTAL:
            temp_x -= TILE_WIDTH / 2 - 1
        elif self._connect == VERTICAL:
            temp_y -= TILE_HEIGHT / 2
        return pygame.Rect(temp_x, temp_y, TILE_WIDTH, TILE_HEIGHT)

if __name__ == "__main__":
    pass

