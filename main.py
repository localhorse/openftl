import sys
import time
import pygame
from person import Person
from ship import Ship
from constants import *
from selection import SelectionRect
from pygame.locals import *

if __name__ == "__main__":

    clock = pygame.time.Clock()

    window = pygame.display.set_mode((800, 600))

    # kestrel is mispelled only in the data files
    kestrel = Ship("kestral", (50, 50))

    human = Person("human", (250, 250), 150, 20)
    rock = Person("rock", (300, 300), 300, 40)
    slug = Person("slug", (325, 275), 100, 15)

    all_chars = pygame.sprite.OrderedUpdates((kestrel, human, rock, slug))

    clock = pygame.time.Clock()

    select_on = False
    first_iter = True
    draw_selection = False
    selection = None

    # move this somewhere else afterwards --FIXME
    rshift_pressed = False
    lshift_pressed = False

    lctrl_pressed = False
    rctrl_pressed = False

    # just testing something (remove) --FIXME
    kestrel.load_rooms()    

    while True:

        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key ==  K_RSHIFT:
                    rshift_pressed = True
                if event.key == K_LSHIFT:
                    lshift_pressed = True
                if event.key == K_RCTRL:
                    rctrl_pressed = True
                if event.key == K_LCTRL:
                    lctrl_pressed = True
                if event.key == K_ESCAPE:
                    sys.exit()
            elif event.type == KEYUP:
                if event.key == K_RSHIFT:
                    rshift_pressed = False
                if event.key == K_LSHIFT:
                    lshift_pressed = False
                if event.key == K_RCTRL:
                    rctrl_pressed = False
                if event.key == K_LCTRL:
                    lctrl_pressed = False
            elif event.type == MOUSEBUTTONDOWN:
                # right mouse button (or left + ctrl for Mac users)
                if event.button == 3 or (event.button == 1 and (lctrl_pressed or rctrl_pressed)):
                    # put these in a sprite group instead --FIXME
                    for alien in [human, rock, slug]:
                        alien.seek_pos(event.pos)
                elif event.button == 1:
                    if not select_on:
                        select_on = True
                        selection = SelectionRect(window, event.pos, col=(255, 255, 255))
            elif event.type == MOUSEMOTION:
                if select_on:
                    rect = selection.updateRect(event.pos)
                    draw_selection = True
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                if select_on:
                    select_on = False
                    rect = selection.updateRect(event.pos)
                    draw_selection = False
                    # these should be in a sprite group
                    for alien in [human, rock, slug]:
                        if alien.bounding_box().colliderect(rect):
                            alien.select()
                        else:
                            alien.deselect()

        window.fill((0, 0, 0))

        # we would clear here with Group.clear() if (didn't seem to
        # work properly, will attempt again --FIXME
        all_chars.update()
        update_rects = all_chars.draw(window)

        if draw_selection:
            selection.draw(window)
        else:
            if selection:
                selection.hide(window)

        pygame.display.update(update_rects)

