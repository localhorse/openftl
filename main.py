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
    window.convert_alpha()
    window.set_alpha(0)

    human = Person("human", (250, 250), 150, 20)
    rock = Person("rock", (300, 300), 300, 40)
    slug = Person("slug", (325, 275), 100, 15)

    all_chars = pygame.sprite.RenderUpdates((human, rock, slug))

    kestral = Ship("kestral", (50, 50))

    clock = pygame.time.Clock()

    kestral.draw(window)
    pygame.display.flip()

    select_on = False
    first_iter = True
    draw_selection = False
    selection = None

    # move this somewhere else afterwards --FIXME
    rshift_pressed = False
    lshift_pressed = False

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
                if event.key == K_ESCAPE:
                    sys.exit()
            elif event.type == KEYUP:
                if event.key == K_RSHIFT:
                    rshift_pressed = False
                if event.key == K_LSHIFT:
                    lshift_pressed = False
            elif event.type == MOUSEBUTTONDOWN:
                # right mouse button
                if event.button == 3:
                    for alien in [human, rock, slug]:
                        alien.seek_pos(event.pos)
                elif event.button == 1:
                    if not select_on:
                        select_on = True
                        selection = SelectionRect(window, event.pos, col=(0, 255, 0))
            elif event.type == MOUSEMOTION:
                if select_on:
                    rect = selection.updateRect(event.pos)
                    draw_selection = True
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                if select_on:
                    select_on = False
                    rect = selection.updateRect(event.pos)
                    draw_selection = False
                    for alien in [human, rock, slug]:
                        if alien.bound_box().colliderect(rect):
                            alien.select()
                        else:
                            alien.deselect()

        window.fill((0, 0, 0))
        kestral.draw(window)

        ##all_chars.clear(window, kestral.get_hull_img())
        all_chars.update()
        update_rects = all_chars.draw(window)

        if draw_selection:
            selection.draw(window)
        else:
            if selection:
                selection.hide(window)

        pygame.display.update(update_rects)
        all_chars.clear(window, kestral.get_hull_img())

