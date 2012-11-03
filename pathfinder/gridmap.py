from collections import defaultdict
from math import sqrt


class GridMap(object):
    """ Represents a rectangular grid map. The map consists of 
        nrows X ncols coordinates (squares). Some of the squares
        can be blocked (by obstacles).
    """

    # this is probably a horrible idea, but I'm sending the ship class
    # with the GridMap initialization so that we can determine of
    # rooms are present between points --danny
    def __init__(self, nrows, ncols, ship=None):
        """ Create a new GridMap with the given amount of rows
            and columns.
        """
        self.nrows = nrows
        self.ncols = ncols

        self._ship = ship
        
        self.map = [[0] * self.ncols for i in range(self.nrows)]
        self.blocked = defaultdict(lambda: False)
    
    def set_blocked(self, coord, blocked=True):
        """ Set the blocked state of a coordinate. True for 
            blocked, False for unblocked.
        """
        self.map[coord[0]][coord[1]] = blocked
    
        if blocked:
            self.blocked[coord] = True
        else:
            if coord in self.blocked:
                del self.blocked[coord]
    
    def move_cost(self, c1, c2):
        """ Compute the cost of movement from one coordinate to
            another. 
            
            The cost is the Euclidean distance.
        """
        return sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2)
    
    # change this method to - if self._ship is present - check c and
    # each item in slist and see if there is a wall between them and
    # no door... if this is the case that node must be removed from
    # the list of successors --danny
    def successors(self, c):
        """ Compute the successors of coordinate 'c': all the 
            coordinates that can be reached by one step from 'c'.
        """
        slist = []
        temp_slist = []
        
        for drow in (-1, 0, 1):
            for dcol in (-1, 0, 1):
                if drow == 0 and dcol == 0:
                    continue 
                    
                newrow = c[0] + drow
                newcol = c[1] + dcol
                if (    0 <= newrow <= self.nrows - 1 and
                        0 <= newcol <= self.ncols - 1 and
                        self.map[newrow][newcol] == 0):
                    temp_slist.append((newrow, newcol))

        for c2 in temp_slist:
            # avoid using diagonal movement, avoid passing through a
            # wall (unless there is a door present) --danny
            y1, x1 = c
            y2, x2 = c2
            if x1 == x2 or y1 == y2:
                if self._ship.wall_present(c, c2):
                    if self._ship.door_present(c, c2):
                        slist.append(c2)
                else:
                    slist.append(c2)

        return slist
    
    def printme(self):
        """ Print the map to stdout in ASCII
        """
        for row in range(self.nrows):
            for col in range(self.ncols):
                print "%s" % ('O' if self.map[row][col] else '.'),
            print ''

