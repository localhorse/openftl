import sys
import time
import pygame
from person import Person
from constants import *

if __name__ == "__main__":

    window = pygame.display.set_mode((640, 480))
    # use os.path.join()
    human = Person("/home/mothra/Projects/openftl/resources/img/people/engi_player_green.png")

    clock = pygame.time.Clock()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif event.key == pygame.K_a:
                    human.walk_left()
                elif event.key == pygame.K_d:
                    human.walk_right()
                elif event.key == pygame.K_w:
                    human.walk_up()
                elif event.key == pygame.K_s:
                    human.walk_down()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # right mouse button
                if event.button == 3:
                    human.seek_pos(event.pos)

        human.draw(window)
        pygame.display.flip()
        human.animate(pygame.time.get_ticks())
        human.move(pygame.time.get_ticks())

        clock.tick()

