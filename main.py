import sys
import time
import pygame
from person import Person
from ship import Ship
from constants import *
from selection import SelectionRect

if __name__ == "__main__":

    window = pygame.display.set_mode((800, 600))
    window.convert_alpha()
    window.set_alpha(0)

    human = Person("human", (250, 250), 150, 20)
    rock = Person("rock", (300, 300), 300, 40)
    slug = Person("slug", (325, 275), 100, 15)

    kestral = Ship("kestral", (50, 50))

    clock = pygame.time.Clock()

    kestral.draw(window)

    select_on = False

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # right mouse button
                if event.button == 3:
                    for alien in [human, rock, slug]:
                        alien.seek_pos(event.pos)
                elif event.button == 1:
                    if not select_on:
                        select_on = True
                        selection = SelectionRect(window, event.pos, col=(0, 255, 0))
            elif event.type == pygame.MOUSEMOTION:
                if select_on:
                    rect = selection.updateRect(event.pos)
                    selection.draw(window)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if select_on:
                    select_on = False
                    rect = selection.updateRect(event.pos)
                    selection.hide(window)
                    for alien in [human, rock, slug]:
                        if alien.bound_box().colliderect(rect):
                            alien.select()
                        else:
                            alien.deselect()

        # this is kind of ridiculous performance wise, we need to
        # reimplement code that will draw only portions of the
        # background
        ##window.fill((0, 0, 0))
        ##kestral.draw(window)
        
        for alien in [human, rock, slug]:
            alien.draw(window)
        
        pygame.display.flip()
        
        for alien in [human, rock, slug]:
            alien.animate(pygame.time.get_ticks())

        for alien in [human, rock, slug]:
            alien.move(pygame.time.get_ticks())

        clock.tick()

