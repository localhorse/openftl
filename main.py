import sys
import time
import pygame
from person import Person
from ship import Ship
from door import Door
from constants import *
from selection import SelectionRect
from pygame.locals import *
from pathfinder.pathfinder import PathFinder

if __name__ == "__main__":

    bg_color = (0, 5, 10)

    clock = pygame.time.Clock()

    # by default FTL is minimum 1280x720, I'd like to scale
    # things... it might be fairly hard to see but it will at least
    # run on platforms without that resolution.
    screen_width = 1280
    screen_height = screen_width / 16 * 9
    display_flags = pygame.DOUBLEBUF | pygame.HWSURFACE
    
    window = pygame.display.set_mode((screen_width, screen_height), display_flags, 32)

    # this should probably be linked to the Door class somehow, but I
    # don't really want to load a sound for every instance of Door and
    # I'm not sure how else to do it right now --FIXME
    pygame.mixer.init()
    door_open_sound = pygame.mixer.Sound("./resources/audio/waves/ui/bp_door_open.ogg")
    # "./resources/audio/waves/ui/bp_door_close.ogg" is for closing
    # EVERY door
    door_close_sound = door_open_sound
    
    # these coordinates are not screen coordinates, but rather X *
    # TILE_WIDTH would be the X screen coordinate
    player_ship = Ship("kestral", (5, 4))

    human = Person("human", player_ship.get_room_pos(0), 150, 20)
    rock = Person("rock", player_ship.get_room_pos(1), 300, 40)

    # add all sprites into this render group, OrderedUpdates() draws
    # the sprites in the order they were added, and optionally returns
    # a list of rects which represent where the screen needs to be
    # redrawn
    all_sprites = pygame.sprite.OrderedUpdates(player_ship)

    # we need to add each item in player_ship.get_doors() to the
    # all_sprites group
    for door in player_ship.get_doors():
        all_sprites.add(door)

    all_sprites.add((human, rock))
    
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
                    for alien in [human, rock]:
                        if alien.selected():
                            alien.seek_pos(event.pos)
                            # let's try to test the path finder with the
                            # map we made
                            pf = PathFinder(player_ship.map.successors,
                                            player_ship.map.move_cost,
                                            player_ship.map.move_cost)
                            # do we need to add/subtract the offsets here
                            # before passing to PathFinder? getting late
                            # and I'm confused --FIXME
                            test_path = list(pf.compute_path(alien.cur_tile(player_ship),
                                                             alien.dst_tile(player_ship)))
                            # print debug info
                            print(test_path)
                        
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
                                door.toggle_door(door_open_sound,
                                                 door_close_sound)

                    # these should be in a sprite group --FIXME
                    for alien in [human, rock]:
                        if alien.bounding_box().colliderect(rect):
                            if not door_clicked:
                                alien.select()
                                # print debug info
                                print(alien.cur_tile(player_ship))
                        else:
                            alien.deselect()

        window.fill(bg_color)

        # we would clear here with Group.clear() if it worked (didn't
        # seem to work properly, will attempt again --FIXME
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

