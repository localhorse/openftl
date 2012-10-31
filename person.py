import pygame
from constants import *

class Person(pygame.sprite.Sprite):
    """Each person or alien in the game is represented by this
    class. The constructor must be provided with species type as a
    string, a tuple representing X, Y position, and an animation and
    move delay."""

    def __init__(self, species, pos, anim_delay, move_delay):

        self._selected = False

        # anim and move delays are used when determining if enough
        # time has passed to perform the next movement or animation
        # frame
        self._anim_delay = anim_delay
        self._move_delay = move_delay
        self._next_anim = 0
        self._next_move = 0

        self._frames = []
        frames = self._frames

        self._dir = DOWN
        self._anim_frame = 0

        x, y = pos
        self._cur_x = self._round_tile(x)
        self._cur_y = self._round_tile(y)
        self._dst_x = self._cur_x
        self._dst_y = self._cur_y

        pygame.sprite.Sprite.__init__(self)

        # use os.join, also make sure species is valid --FIXME
        self._selected_file = "./resources/img/people/%s_player_green.png" % species
        self._unselected_file = "./resources/img/people/%s_player_yellow.png" % species

        self._selected_sheet = pygame.image.load(self._selected_file).convert_alpha()
        self._unselected_sheet = pygame.image.load(self._unselected_file).convert_alpha()
        # go through each column in the top row of the sprite sheet,
        # and load each walking animation for each cardinal direction
        for index in range(0, ALIEN_COLS):

            temp_rect = pygame.Rect((index * ALIEN_WIDTH, 0),
                                    (ALIEN_WIDTH, ALIEN_HEIGHT))
            frames.append((pygame.Surface(temp_rect.size,
                                          flags=pygame.SRCALPHA).convert_alpha(),
                                          pygame.Surface(temp_rect.size,
                                                         flags=pygame.SRCALPHA).convert_alpha()))
            unselected_surf, selected_surf = frames[len(frames) - 1]
            unselected_surf.blit(self._unselected_sheet, (0, 0),
                                 temp_rect, special_flags=BLEND_TYPE)
            selected_surf.blit(self._selected_sheet, (0, 0),
                               temp_rect, special_flags=BLEND_TYPE)

        # discarding some values as we just want basically the first
        # image in here to begin with, then setting Sprite specific
        # values
        (self.image, _) = frames[0]
        (temp_frame, _) = frames[0]
        self.rect = self.bounding_box()
            
    def update(self):
        self._move()
        self._animate()
        self._cur_frame()

    def _move(self):
        """This moves the sprite: if enough time has passed according
        to move_delay, then the sprite's position will be moved and the
        rect updated."""

        cur_time = pygame.time.get_ticks()

        if self._next_move < cur_time:

            if self._cur_x != self._dst_x or self._cur_y != self._dst_y:

                if self._cur_x > self._dst_x:
                    self._cur_x -= 1
                    self._dir = LEFT
                elif self._cur_x < self._dst_x:
                    self._cur_x += 1
                    self._dir = RIGHT

                if self._cur_y > self._dst_y:
                    self._cur_y -= 1
                    self._dir = UP
                elif self._cur_y < self._dst_y:
                    self._cur_y += 1
                    self._dir = DOWN

            self._next_move = cur_time + self._move_delay
            self.rect = self.bounding_box()
            
    def _animate(self):
        """If enough time has passed and our state is not idle, then
        this method will go to the next animation frame."""
        cur_time = pygame.time.get_ticks()
        if self._next_anim < cur_time:
            if self._cur_x != self._dst_x or self._cur_y != self._dst_y:
                self._anim_frame += 1
                if self._anim_frame > MAX_ANIM_FRAME:
                    self._anim_frame = 0
            else:
                self._anim_frame = 0
            self._next_anim = cur_time + self._anim_delay
            
    def _cur_frame(self):
        """This method returns the current frame that should be
        drawn... this frame will be different depending on whether or
        not the sprite has been selected."""
        unselected_frame, selected_frame = self._frames[self._dir * 4 + self._anim_frame]

        if self._selected:
            temp_frame = selected_frame
        else:
            temp_frame = unselected_frame

        self.image = temp_frame
        

    def seek_pos(self, pos):
        """This method simply sets a destination for our sprite, which
        will then seek that destination until it is reached."""
        x_pos, y_pos = pos
        # make sure the actual guy ends up pretty much dead center in
        # the tile where the mouse was clicked (this behavior will
        # change)
        if self._selected:
            self._dst_x = self._round_tile(x_pos)
            self._dst_y = self._round_tile(y_pos)

    def bounding_box(self):
        """This method returns a rect that represents the position and
        size of this sprite. We can't use Sprite.image.get_rect() as
        that returns with a starting position of (0, 0)."""
        return pygame.Rect(self._cur_x, self._cur_y, ALIEN_WIDTH, ALIEN_HEIGHT)

    def toggle_selected(self):
        if self._selected:
            self._selected = False
        else:
            self._selected = True

    def select(self):
        self._selected = True

    def deselect(self):
        self._selected = False

    def get_pos(self):
        return (self._cur_x, self._cur_y)

    def selected(self):
        return self._selected

    # just testing something temporarily, this should return a
    # location corresponding to the map/grid, not including the
    # offsets... either that or we need to subtract the offsets at the
    # other end --FIXME
    def get_tile(self):
        return (self._cur_x / TILE_WIDTH, self._cur_y / TILE_HEIGHT)
    
    def seek_tile(self, tile_pos):
        tile_x, tile_y = tile_pos
        if self._selected:
            self._dst_x = self._round_tile(tile_x * TILE_WIDTH)
            self._dst_y = self._round_tile(tile_y * TILE_HEIGHT)
            
    def _round_tile(self, coord):
        """This method ensures that seek_pos() can't choose any old
        arbitrary coordinates... given an X or Y value, _round_tile()
        will return the corresponding value which would refer to the
        center of the closest tile."""
        # could have just as easily used TILE_HEIGHT, since they are
        # the same, but if they ever become different, this will need
        # to be changed (not really a concern, as a LOT would need
        # changing)
        return divmod(coord, TILE_WIDTH)[0] * TILE_WIDTH

if __name__ == "__main__":
    pass

