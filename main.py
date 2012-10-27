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
    kestral = Ship("kestral", (50, 50))

    clock = pygame.time.Clock()

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

        kestral.draw(window)
        human.draw(window)
        rock.draw(window)
        pygame.display.flip()
        human.animate(pygame.time.get_ticks())
        human.move(pygame.time.get_ticks())

        clock.tick()

