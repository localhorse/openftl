import sys
import time
import platform
import pygame
from person import Person
from ship import Ship
from door import Door
from constants import *
from selection import SelectionRect
from pygame.locals import *

if __name__ == "__main__":

    bg_color = (0, 5, 10)

    clock = pygame.time.Clock()

    # by default FTL is minimum 1280x720, I'd like to scale
    # things... it might be fairly hard to see but it will at least
    # run on platforms without that resolution.
    screen_width = 1280
    screen_height = screen_width / 16 * 9
    display_flags = pygame.DOUBLEBUF | pygame.HWSURFACE
    
    # for some reason 32 fails on Ryan's Mac and 24 causes my surface
    # to not have hardware acceleration on Linux (and presumably
    # Windows)
    if "Darwin" in platform.system():
        window = pygame.display.set_mode((screen_width, screen_height), display_flags, 24)
    else:
        window = pygame.display.set_mode((screen_width, screen_height), display_flags, 32)

    # these coordinates are not screen coordinates, but rather X *
    # TILE_WIDTH would be the X screen coordinate
    player_ship = Ship("fed_cruiser", (5, 4))

    human = Person("human", 0, player_ship.get_room_pos(0), 100, 12)
    human.add_to_ship(player_ship)
    
    engi_one = Person("engi", 1, player_ship.get_room_pos(1), 100, 12)
    engi_one.add_to_ship(player_ship)

    engi_two = Person("engi", 2, player_ship.get_room_pos(2), 100, 12)
    engi_two.add_to_ship(player_ship)

    rock = Person("rock", 3, player_ship.get_room_pos(3), 100, 28)
    rock.add_to_ship(player_ship)

    # add all sprites into this render group, with LayeredUpdates we
    # can move things to the front or back
    all_sprites = pygame.sprite.LayeredUpdates(player_ship)
    all_sprites.move_to_back(player_ship)

    # we need to add each item in player_ship.get_doors() to the
    # all_sprites group
    for door in player_ship.get_doors():
        all_sprites.add(door)

    all_sprites.add((human, engi_one, engi_two, rock))
    
    clock = pygame.time.Clock()

    # a bunch of booleans involved in the click/drag selection process
    select_on = False
    first_iter = True
    draw_selection = False
    selection = None

    # move this somewhere else afterwards --FIXME
    rshift_pressed = False
    lshift_pressed = False
    lctrl_pressed = False
    rctrl_pressed = False

    window.fill(bg_color)
    pygame.display.update()

    # the main game loop... we'll just check for input events, update
    # based on input, clear the screen entirely, update sprite
    # movement & animation, draw the selection box if it's being used,
    # and finally update the display
    while True:

        # this is just a rough guess but 80 puts it at about mantis
        # speed if we update the position once per sprite update... we
        # will definitely want to do something about this later,
        # though --FIXME
        clock.tick(80)

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
                    for alien in [human, engi_one, engi_two, rock]:
                        if alien.selected():
                            # set the goal or final destination
                            alien.set_goal(event.pos)
                            alien.compute_path()
                        
                elif event.button == 1:
                    if not select_on:
                        select_on = True
                        selection = SelectionRect(window, event.pos,
                                                  col=(255, 255, 255))
            elif event.type == MOUSEMOTION:
                if select_on:
                    rect = selection.updateRect(event.pos)
                    draw_selection = True
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                if select_on:
                    select_on = False
                    rect = selection.updateRect(event.pos)
                    draw_selection = False

                    # here's where we'll check if they clicked a door
                    (_, _, rect_width, rect_height) = rect
                    door_clicked = False
                    if rect_width < 15 and rect_height < 15:
                        for door in player_ship.get_doors():
                            if door.bounding_box(collision=True).colliderect(rect):
                                door_clicked = True
                                door.toggle_door()

                    # these should be in a sprite group --FIXME
                    for alien in [human, engi_one, engi_two, rock]:
                        if alien.bounding_box().colliderect(rect):
                            if not door_clicked:
                                if not lshift_pressed and not rshift_pressed:
                                    alien.select()
                                else:
                                    alien.toggle_selected()
                        elif not lshift_pressed and not rshift_pressed:
                            alien.deselect()

        window.fill(bg_color)

        # we would clear here with Group.clear() if it worked (didn't
        # seem to work properly, will attempt again --FIXME

        for alien in [human, engi_one, engi_two, rock]:
            if alien.is_moving():
                all_sprites.move_to_front(alien)
            else:
                all_sprites.move_to_back(alien)
                all_sprites.move_to_back(player_ship)
                
        all_sprites.update()
        sprite_rects = all_sprites.draw(window)
        
        # if the user is currently selecting something, we should draw
        # the box now, on top of everything else
        if draw_selection:
            selection.draw(window)
        else:
            if selection:
                selection.hide(window)

        pygame.display.update(sprite_rects)

