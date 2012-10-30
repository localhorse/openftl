import pygame
from constants import *

class Door(pygame.sprite.Sprite):

    # again, this x, y position is not a screen pixel position but
    # rather a grid of TILE_WIDTH by TILE_HEIGHT sized tiles - we'll
    # do this eventually for everything but the Person class, it will
    # be easier to scale
    def __init__(self, pos, room_left, room_right, connect):
        
        self._cur_x, self._cur_y = pos        
        self._frames = []
        frames = self._frames
        self._next_anim = 0
        self._anim_delay = 200
        self._anim_frame = 0

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

            (self.image, _) = frames[0]
            self.rect = self.image.get_rect()
            
    def update(self):
        self._test_anim()
        self._cur_frame()

    def _cur_frame(self):
        # this only needs its own method because later we'll need to
        # determine if we're drawing the regular or upgraded door
        (_, self.image) = self._frames[self._anim_frame]

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
        return pygame.Rect(self._cur_x * TILE_WIDTH, self._cur_y * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
    
if __name__ == "__main__":
    pass


