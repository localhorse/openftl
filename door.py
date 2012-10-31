import pygame
from constants import *

class Door(pygame.sprite.Sprite):

    """The Door class represents, obviously, the doors on the
    ship. This class is only ever instanced from Ship. Ship keeps a
    running list of doors as it loads them from the file. Constructor
    takes ship position, desired door position, the room ID to the
    left/above the door, the room ID to the right/below the door,
    whether it connects vertically or horizontally, and the offsets
    from the ship file. As with ship, the positions are not pixel
    coordinates but rather tile coordinates."""

    def __init__(self, ship_pos, pos, room_left, room_right, connect,
                 x_offset, y_offset, vert_offset):
        
        self._cur_x, self._cur_y = pos        
        self._ship_x, self._ship_y = ship_pos

        self._frames = []
        frames = self._frames
        self._next_anim = 0
        self._anim_delay = 50
        self._anim_frame = DOOR_CLOSED
        self._dest_frame = DOOR_CLOSED

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
            # loading both the yellow and the (upgraded) grey
            # door... first row contains the regular door, and we'll
            # point our rectangle there
            temp_rect = pygame.Rect((index * TILE_WIDTH, 0),
                                    (TILE_WIDTH, TILE_HEIGHT))
            frames.append((pygame.Surface(temp_rect.size,
                                          flags=pygame.SRCALPHA).convert_alpha(),
                                          pygame.Surface(temp_rect.size,
                                                         flags=pygame.SRCALPHA).convert_alpha()))
            reg_surf, upg_surf = frames[len(frames) - 1]
            reg_surf.blit(self._door_sheet, (0, 0), temp_rect,
                          special_flags=BLEND_TYPE)
            # adjust our "camera" rect one row down... the 2nd row
            # will contain upgraded door frames
            temp_rect = pygame.Rect((index * TILE_WIDTH, TILE_HEIGHT),
                                    (TILE_WIDTH, TILE_HEIGHT))
            upg_surf.blit(self._door_sheet, (0, 0), temp_rect,
                          special_flags=BLEND_TYPE)

            # these need to be oriented properly, so we'll rotate them
            # if needed
            if connect == VERTICAL:
                reg_surf = pygame.transform.rotate(reg_surf, 90)
                upg_surf = pygame.transform.rotate(upg_surf, 90)
                frames[len(frames) - 1] = (reg_surf, upg_surf)

        (self.image, _) = frames[0]
        self.rect = self.bounding_box()
            
    def update(self):
        self._animate()
        self._cur_frame()

    def _cur_frame(self):
        # this only needs its own method because later we'll need to
        # determine if we're drawing the regular or upgraded door
        (self.image, _) = self._frames[self._anim_frame]

    def _animate(self):
        cur_time = pygame.time.get_ticks()
        if self._next_anim < cur_time:
            # DOOR ANIM
            if self._anim_frame < self._dest_frame:
                self._anim_frame += 1
            elif self._anim_frame > self._dest_frame:
                self._anim_frame -= 1                                
            self._next_anim = cur_time + self._anim_delay
        # Group.update() doesn't seem concerned with redrawing this
        # unless the rect has changed!
        self.rect = self.bounding_box()

    # we'll need methods in Ship: open_all_doors(), close_all_doors()
    # --FIXME

    def open_door(self, open_sound=None):
        self._dest_frame = DOOR_OPENED
        if open_sound:
            open_sound.play()

    def close_door(self, close_sound=None):
        self._dest_frame = DOOR_CLOSED
        if close_sound:
            close_sound.play()

    def toggle_door(self, open_sound, close_sound):
        if self._dest_frame == DOOR_CLOSED:
            self.open_door(open_sound)
        else:
            self.close_door(close_sound)
        
    def get_pos(self):
        return (self._cur_x, self._cur_y)

    def get_connect(self):
        return self._connect

    def bounding_box(self, collision=False):
        """This method returns a rect that represents the position and
        size of this sprite. We can't use Sprite.image.get_rect() as
        that returns with a starting position of (0, 0). In this
        particular class this method also shrinks the bounding box
        below the size of the actual image, since the doors are much
        thinner than the door image."""
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
        if not collision:
            # this determines precisely where the image will be drawn
            # for the render group... this may or may not work when
            # the doors are modeled properly --FIXME
            if self._connect == HORIZONTAL:
                temp_x -= TILE_WIDTH / 2 - 1
            elif self._connect == VERTICAL:
                temp_y -= TILE_HEIGHT / 2
            return pygame.Rect(temp_x, temp_y, TILE_WIDTH, TILE_HEIGHT)
        else:
            # this determines the bounding box for collision detection
            # purposes (in this case the selection box) - it's all
            # kind of a hack and will have to be changed when I do the
            # doors properly, but as of right now I'm playing around
            # and it's functional --FIXME
            if self._connect == HORIZONTAL:
                temp_x -= 4
                return pygame.Rect(temp_x, temp_y, TILE_WIDTH / 4 + 4,
                                   TILE_HEIGHT)
            else:
                temp_y -= 4
                return pygame.Rect((temp_x, temp_y, TILE_WIDTH,
                                    TILE_HEIGHT / 4 + 4))

if __name__ == "__main__":
    pass


