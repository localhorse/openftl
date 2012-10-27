import sys
import time
import pygame
from person import Person
from ship import Ship
from constants import *

if __name__ == "__main__":

    window = pygame.display.set_mode((800, 600))
    window.convert_alpha()
    window.set_alpha(0)

    human = Person("human", (250, 250), 150, 20)
    rock = Person("rock", (300, 300), 300, 40)
    slug = Person("slug", (325, 275), 100, 20)
    kestral = Ship("kestral", (50, 50))

    clock = pygame.time.Clock()

    kestral.draw(window)

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
                    human.seek_pos(event.pos)
                    rock.seek_pos(event.pos)
                    slug.seek_pos(event.pos)
                elif event.button == 1:
                    if human.bound_box().collidepoint(event.pos):
                        human.select()
                        rock.deselect()
                        slug.deselect()
                    elif rock.bound_box().collidepoint(event.pos):
                        rock.select()
                        human.deselect()
                        slug.deselect()
                    elif slug.bound_box().collidepoint(event.pos):
                        slug.select()
                        human.deselect()
                        rock.deselect()

        # this is kind of ridiculous performance wise, we need to
        # reimplement code that will draw only portions of the
        # background
        window.fill((0, 0, 0))
        kestral.draw(window)
        
        human.draw(window)
        rock.draw(window)
        slug.draw(window)
        
        pygame.display.flip()
        
        human.animate(pygame.time.get_ticks())
        rock.animate(pygame.time.get_ticks())
        slug.animate(pygame.time.get_ticks())
        
        human.move(pygame.time.get_ticks())
        rock.move(pygame.time.get_ticks())
        slug.move(pygame.time.get_ticks())

        clock.tick()

