"""
selection.py - C&C like selection rectangles
Raiser, Frank - Aug 3, 2k++
crashchaos at gmx.net

This is a simple and ready-to-use class which adds C&C (Command & Conquer)
like selection rectangles to your games/apps so that the user can resize
a rectangle to cover some area on the screen (f.ex. to choose all units in
that area)

You can run this sample right away using the supplied main() method if you
want to check the effect.

A short description on the usage of this class:
1) Initiate the class passing it the surface to display the rectangle on,
   the starting point of your selection rectangle and an optional color
   in which to draw the rectangle (defaults to black)
2) Check for MOUSEMOTION and then call updateRect() and draw() methods (this
   is doing the main work)
3) After the user released the mousebutton (or whenever you want actually)
   make a final call to updateRect() (it will return the selection rectangle
   and you might want to save that in some var ;).
4) Don't forget to call the hide() method to clear the final selection
   rectangle (unless you're totally redrawing the screen anyways)

Possible customizations:
1) the default drawing color (line X)
2) use another surfarray method (pixels3d is used here which only works
   for surfaces with 32 or 24 bpp - shouldn't be that hard)
3) something else I didn't think of :)

Dependencies:
1) pygame w/ surfarray support
2) PyNumeric
"""

import pygame,pygame.surfarray
from pygame.locals import *
##import Numeric,copy
import copy

class SelectionRect:
    """ class SelectionRect
    utility class for using selection rectangles
    """
    def __init__(self,screen,start,col=(0,0,0)):
        """ __init__(self,screen,start,col=(0,0,0))
        Constructor. Pass starting point of selection rectangle in 'start'
        and color value in which the selection rectangle shall be drawn
        in 'col'
        """
        self.start         = start
        self.col           = col
        self.oldrect       = start[0],start[1],1,1
        tmp                = screen.get_at((start[0],start[1]))[:3]
        self.screen_backup = [[tmp],[tmp],[tmp],[tmp]]
        
    def updateRect(self,now):
        """ updateRect(self,now) -> rect tuple
        This returns a rectstyle tuple describing the selection rectangle
        between the starting point (passed to __init__) and the 'now' edge and
        updates the internal rectangle information for correct drawing.
        """
        x,y = self.start
        mx,my = now
        if mx < x:
            if my < y:
                self.rect = mx,my,x-mx,y-my
            else:
                self.rect = mx,y,x-mx,my-y
        elif my < y:
            self.rect = x,my,mx-x,y-my
        else:
            self.rect = x,y,mx-x,my-y
        return self.rect

    def draw(self,screen):
        """ draw(self,screen)
        This hides the old selection rectangle and draws the current one
        """
        # just some shortcuts :P
        surf = pygame.surfarray.pixels3d(screen)
        r    = self.rect
        # hide selection rectangle
        self.hide(screen)
        
        # update background information
        self.screen_backup[0] = copy.copy(surf[r[0]:r[0]+r[2],r[1]])
        self.screen_backup[1] = copy.copy(surf[r[0]:r[0]+r[2],r[1]+r[3]-1])
        self.screen_backup[2] = copy.copy(surf[r[0],r[1]:r[1]+r[3]])
        self.screen_backup[3] = copy.copy(surf[r[0]+r[2]-1,r[1]:r[1]+r[3]])

        # draw selection rectangle:
        surf[r[0]:r[0]+r[2],r[1]]        = self.col
        surf[r[0]:r[0]+r[2],r[1]+r[3]-1] = self.col
        surf[r[0],r[1]:r[1]+r[3]]        = self.col
        surf[r[0]+r[2]-1,r[1]:r[1]+r[3]] = self.col

        self.oldrect = r
        
        pygame.display.update(r)

    def hide(self,screen):
        """ hide(self,screen)
        This hides the selection rectangle using the stored background
        information. You usually call this after you're finished with the
        selection to hide the last rectangle.
        """
        surf = pygame.surfarray.pixels3d(screen)
        x,y,x2,y2 = self.oldrect[0],self.oldrect[1],\
                    self.oldrect[0]+self.oldrect[2],\
                    self.oldrect[1]+self.oldrect[3]
        surf[x:x2,y   ] = self.screen_backup[0]
        surf[x:x2,y2-1] = self.screen_backup[1]
        surf[x,   y:y2] = self.screen_backup[2]
        surf[x2-1,y:y2] = self.screen_backup[3]
        pygame.display.update(self.oldrect)

def main():
    """ main()
    Simple test program for showing off the selection rectangles
    """
    pygame.init()
    screen = pygame.display.set_mode((640,480),0,24)

    # create a dotted background
    surf = pygame.surfarray.pixels3d(screen)
    surf[:] = (255,255,255)
    surf[::4,::4] = (0,0,255)
    pygame.display.update()

    # make up a test loop
    finished = 0
    selection_on = 0
    while not finished:
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                finished = 1
            elif e.type == MOUSEBUTTONDOWN and e.button == 1:
                if not selection_on:
                    # begin with selection as the user pressed down the left
                    # mouse button
                    selection_on = 1
                    selection = SelectionRect(screen,e.pos)
            elif e.type == MOUSEMOTION:
                if selection_on:
                    # update the selection rectangle while the mouse is moving
                    selection.updateRect(e.pos)
                    selection.draw(screen)
            elif e.type == MOUSEBUTTONUP and e.button == 1:
                if selection_on:
                    # stop selection when the user released the button
                    selection_on = 0
                    rect = selection.updateRect(e.pos)
                    # don't forget this!
                    # (or comment it out if you really want the final selection
                    #  rectangle to remain visible)
                    selection.hide(screen)
                    # just FYI
                    print "Final selection rectangle:",rect

    pygame.quit()

if __name__ == '__main__': main()
