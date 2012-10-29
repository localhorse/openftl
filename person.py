import pygame
from constants import *

if __name__ == "__main__":
    pass

# each person or alien in the game is represented by this class
class Person(pygame.sprite.Sprite):

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
        self._cur_x = x
        self._cur_y = y
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
            frames.append((pygame.Surface(temp_rect.size, flags=pygame.SRCALPHA).convert_alpha(), pygame.Surface(temp_rect.size, flags=pygame.SRCALPHA).convert_alpha()))
            unselected_surf, selected_surf = frames[len(frames) - 1]
            unselected_surf.blit(self._unselected_sheet, (0, 0), temp_rect, special_flags=BLEND_TYPE)
            selected_surf.blit(self._selected_sheet, (0, 0), temp_rect, special_flags=BLEND_TYPE)

        # discarding some values as we just want basically the first
        # image in here to begin with, then setting Sprite specific
        # values
        (self.image, _) = frames[0]
        (temp_frame, _) = frames[0]
        self.rect = temp_frame.get_rect()
            
    def update(self):
        self._move()
        self._animate()
        self._cur_frame()

    # if enough time has passed and we're moving, then move and change
    # the sprite direction
    def _move(self):

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
            
    # if enough time has passed and we're not idle, go to the next
    # animation frame
    def _animate(self):
        cur_time = pygame.time.get_ticks()
        if self._next_anim < cur_time:
            if self._cur_x != self._dst_x or self._cur_y != self._dst_y:
                self._anim_frame += 1
                if self._anim_frame > MAX_ANIM_FRAME:
                    self._anim_frame = 0
            else:
                self._anim_frame = 0
            self._next_anim = cur_time + self._anim_delay
            
    # returns the current frame (which would be different depending on
    # whether or not this Person is selected
    def _cur_frame(self):

        unselected_frame, selected_frame = self._frames[self._dir * 4 + self._anim_frame]

        if self._selected:
            temp_frame = selected_frame
        else:
            temp_frame = unselected_frame

        self.image = temp_frame
        

    def seek_pos(self, pos):
        x_pos, y_pos = pos
        # make sure the actual guy ends up pretty much dead center in
        # the mouse click
        if self._selected:
            self._dst_x = x_pos - ALIEN_WIDTH / 2
            self._dst_y = y_pos - ALIEN_HEIGHT / 2

    def bounding_box(self):
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


