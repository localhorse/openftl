import pygame
from constants import *

if __name__ == "__main__":
    pass

# each person or alien in the game is represented by this class
class Person(pygame.sprite.Sprite):

    def __init__(self, sheet_file, pos, anim_delay, move_delay):

        self._anim_delay = anim_delay
        self._move_delay = move_delay
        self._frames = []
        self._dir = DOWN
        self._next_animate = 0
        self._anim_frame = 0
        self._next_move = 0

        x, y = pos
        self._cur_x = x
        self._cur_y = y
        self._dst_x = self._cur_x
        self._dst_y = self._cur_y

        frames = self._frames
        
        pygame.sprite.Sprite.__init__(self)

        # be sure to convert_alpha() on the original sprite sheet
        self.sheet = pygame.image.load(sheet_file).convert_alpha()
        sheet = self.sheet
        
        # go through each column in the top row of the sprite sheet,
        # and load each walking animation
        for index in range(0, SPRITE_COLS):

            temp_rect = pygame.Rect((index * SPRITE_WIDTH, 0),
                                    (SPRITE_WIDTH, SPRITE_HEIGHT))
            frames.append(pygame.Surface(temp_rect.size).convert())
            frames[len(frames) - 1].blit(sheet, (0, 0), temp_rect)

    def move(self, cur_time):
        if self._next_move < cur_time:
            if self._cur_x != self._dst_x or self._cur_y != self._dst_y:
                if self._cur_x > self._dst_x:
                    self._cur_x -= SPEED
                    self.walk_left()
                elif self._cur_x < self._dst_x:
                    self._cur_x += SPEED
                    self.walk_right()
                elif self._cur_y > self._dst_y:
                    self._cur_y -= SPEED
                    self.walk_up()
                elif self._cur_y < self._dst_y:
                    self._cur_y += SPEED
                    self.walk_down()
            self._next_move = cur_time + self._move_delay
        
    def animate(self, cur_time):
        if self._next_animate < cur_time:
            if self._cur_x != self._dst_x or self._cur_y != self._dst_y:
                self._anim_frame += 1
                if self._anim_frame > MAX_ANIM_FRAME:
                    self._anim_frame = 0
            else:
                self._anim_frame = 0
            self._next_animate = cur_time + self._anim_delay

    # this is just for debugging, to draw any arbitrary frame from our
    # sprite
    def draw_frame(self, surface, frame_num):
        surface.blit(self._frames[frame_num], (0, 0))

    def walk_left(self):
        self._dir = LEFT

    def walk_right(self):
        self._dir = RIGHT

    def walk_up(self):
        self._dir = UP

    def walk_down(self):
        self._dir = DOWN

    def draw(self, surface):
        surface.blit(self._frames[self._dir * 4 + self._anim_frame], (self._cur_x, self._cur_y))

    def seek_pos(self, pos):
        x_pos, y_pos = pos
        # make sure the actual guy ends up pretty much dead center in
        # the mouse click
        self._dst_x = self._round_speed(x_pos - SPRITE_WIDTH / 2)
        self._dst_y = self._round_speed(y_pos - SPRITE_HEIGHT / 2)

    # makes sure we round the x and y to the proper increment (based
    # on speed) so we don't get stuck running back and forth
    def _round_speed(self, x):
        return divmod(x, SPEED)[0] * SPEED
