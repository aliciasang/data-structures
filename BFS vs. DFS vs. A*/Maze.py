from __future__ import annotations
from enum import Enum
from typing import NamedTuple
from Stack import Stack
from Queue import Queue
from PriorityQueue import PriorityQueue
import random

################################################################################
class Contents(str, Enum):
    ''' create an enumeration to define what the visual contents of a Cell are;
        using str as a "mixin" (multiple inheritance) forces all the entries to
        be strings; using an Enum means no cell entry can be anything other
        than the options here
    '''
    # if the fancy Unicode versions don't display correctly in your terminal,
    # just use 'S', 'G', 'X', '*' instead
    EMPTY   = ' '
    START   = '⦿' #'S'
    GOAL    = '◆' #'G'
    BLOCKED = '░' #'X'
    PATH    = '★' #'*'

    def __str__(self) -> str: return self.value

################################################################################
class Position(NamedTuple):
    ''' just allows us to use .row and .col rather than the less-easy-to-read
        [0] and [1] for accessing values'''
    row: int
    col: int

    def __str__(self) -> str: return f"({self.row},{self.col})"

################################################################################
class SearchOrder(Enum):
    ''' enumeration for neighboring cells search order '''
    NSWE   = 1
    NESW   = 2
    RANDOM = 3

################################################################################
class Cell:
    ''' class that allows us to use Cell as a data type -- an ordered triple 
        of row, column, & cell contents 
        (see Contents class enumeration above) 
    '''
    __slots__ = ('_position', '_contents', '_parent', '_cost', '_heur')

    def __init__(self, row: int, col: int, contents: Contents):
        self._position:  Position = Position(row, col)
        self._contents:  Contents = contents
        self._parent:    Cell     = None    # parent of this Cell during exploration
        self._cost: float = float('inf')
        self._heur: float = 0

       
    def getPosition(self) -> Position:
        ''' method to return the (row,col) Position of this cell
        Returns:
            a Position object containing the cell's row and column
        '''
        return Position(self._position.row, self._position.col)

    def getParent(self) -> Cell:
        ''' method to return the parent of this Cell object as determined during
            maze exploration
        Returns:
            a Cell object corresponding to the cell that considered this cell
            during the exploration process
        '''
        return self._parent

    def setParent(self, parent: Cell) -> None:
        ''' setter method to update this Cell's parent
        Parameters:
            parent: a different Cell object
        Raises:
            ValueError if self == parent
        '''
        if self == parent: raise ValueError(f"a Cell cannot be its own parent")
        self._parent = parent

    def markOnPath(self) -> None:
        ''' method to identify this cell as being on the path from source
            to goal
        '''
        self._contents = Contents.PATH

    def isBlocked(self) -> bool:
        ''' Boolean method to indicate whether this cell contains a block
        Returns:
            True if the cell is blocked (cannot be explored), False o/w
        '''
        return self._contents == Contents.BLOCKED

    def isGoal(self) -> bool:
        ''' Boolean method to indicate whether this cell is the goal
        Returns:
            True if the cell is the maze goal, False o/w
        '''
        return self._contents == Contents.GOAL

    def __str__(self) -> str:
        ''' creates and returns a string representation of this cell
        Returns:
            a string identifying the cell's row, col, and cell contents
        '''
        contents = "[EMPTY]" if self._contents == Contents.EMPTY else self._contents
        string = f"({self._position.row}, {self._position.col}): {contents} "
        if self._parent is not None:
            string += f"({self._parent._position.row}, {self._parent._position.col})"
        return string

    def __repr__(self) -> str:
        ''' overriding __repr__ so that printing, e.g., a list of Cell objects
            (which will call __repr__ for each) will call __str__ for each, printing
            nicely
        Returns:
            a string identifying the cell's row, col, and cell contents
        '''
        return self.__str__()

    def __eq__(self, other: Cell) -> bool:
        ''' indicates whether a given other Cell is equal to this Cell
        Returns:
            True if this Cell and the other Cell are the same, False o/w
        '''
        return self._position.row == other._position.row and \
               self._position.col == other._position.col and \
               self._contents == other._contents

################################################################################
class Maze:
    ''' class representing a 2D maze of Cell objects '''
    __slots__ = ('_grid', '_num_rows', '_num_cols', '_start', '_goal', '_search_order', '_path_length', '_num_cells_pushed', '_num_cells_explored')
 
    def __init__(self, rows: int = 10, cols: int = 10,
                       start:        Position = None, \
                       goal:         Position = None, \
                       prop_blocked: float = 0.2, \
                       search_order: SearchOrder = SearchOrder.NSWE, \
                       debug: bool = False):
        ''' initializer method for a Maze object
        Parameters:
            rows:          number of rows in the grid
            cols:          number of columns in the grid
            start:         Position object indicating the (row,col) of the start cell
            goal:          Position object indicating the (row,col) of the goal cell
            prop_blocked:  proportion of cells to be blocked (between 0.0 and 1.0)
            search_order:  SearchOrder enum -- one of NSWE, NESW, or RANDOM
            debug:         whether to use one of the Maze examples from course slides
        Raises:
            TypeError  if prop_blocked is not a float
            ValueError if prop_blocked is not in (0,1)
            TypeError  if start or goal is not a Position object
            ValueError if row/col of start or goal is out of range
        '''

        msg = "prop_blocked must be a float between 0 and 1"
        try:
            float(prop_blocked)
        except:
            raise TypeError(msg)
        else:
            if prop_blocked < 0 or prop_blocked > 1:
                raise ValueError(msg)

        # if user doesn't specify either start or goal, force them to
        # be respectively in the UL and LR corners
        if start is None or goal is None:
            start = Position(0,0)
            goal  = Position(rows - 1, cols - 1)

        if not isinstance(start, Position) or not isinstance(goal, Position):
            raise TypeError("start and goal must both be Position objects")

        if start.row < 0 or start.row >= rows or \
           start.col < 0 or start.col >= cols:
            raise ValueError("invalid (row,col) given for start cell")
        if goal.row  < 0 or goal.row  >= rows or \
           goal.col  < 0 or goal.col  >= cols:
            raise ValueError("invalid (row,col) given for goal cell")

        if debug: 
            # to match DCS 229 slides example
            rows = 6; cols = 5;
            start = Position(5, 0)
            goal  = Position(0, 4)

        self._num_rows     = rows
        self._num_cols     = cols
        self._start        = Cell(start.row, start.col, Contents.START)
        self._goal         = Cell(goal.row,  goal.col,  Contents.GOAL)
        self._search_order = search_order
        self._path_length = 0
        self._num_cells_pushed = 0
        self._num_cells_explored = 0

        # create a rows x cols 2D list of Cell objects, intially all empty
        self._grid: list[list[Cell]] = \
            [ [Cell(r,c, Contents.EMPTY) for c in range(cols)] for r in range(rows) ]

        # set the start and goal cells (overriding two empty Cell objects from above)
        self._grid[start.row][start.col] = self._start
        self._grid[goal.row][goal.col]   = self._goal

        # put blocks at random spots in the grid, using given proportion;  
        # start by creating a collapsed 1D version of the grid, then
        #   remove the start and goal, and then randomly pick cells to block;
        # note that we are using identical object references in both 
        #   options and self._grid so that updates to options will be seen
        #   in self._grid (i.e., options is not a deep copy of cells);
        if not debug: 
            options = [cell for row in self._grid for cell in row]
            options.remove(self._start)
            options.remove(self._goal)
            blocked = random.sample(options, k = round((rows * cols - 2) * prop_blocked))
            for b in blocked: 
                b._contents = Contents.BLOCKED  # this is changing self._grid!
        else:
            # for example from slides
            pos = [(1,0),(1,3),(2,1),(2,4),(3,2),(5,1),(5,3),(5,4)]
            for p in pos:
                self._grid[p[0]][p[1]]._contents = Contents.BLOCKED

    def __str__(self) -> str:
        ''' creates a str version of the Maze, showing contents, with cells
            delimited by vertical pipes 
        Returns:
            a str representation of the Maze
        '''
        maze_str = ""
        for row in self._grid:  # row : list[Cell] 
            maze_str += "|" + "|".join([cell._contents for cell in row]) + "|\n"
        return maze_str[:-1]  # remove the final \n

    def getStart(self) -> Cell: 
        ''' accessor method to return the Cell object corresponding to the Maze start
        Returns:
            the Cell object at the Maze start location
        '''
        return self._start

    def getGoal(self) -> Cell:
        ''' accessor method to return the Cell object corresponding to the Maze goal
        Returns:
            the Cell object at the Maze goal location
        '''
        return self._goal

    def getSearchLocations(self, cell: Cell) -> list[Cell]:
        ''' method to return a list of Cell objects of valid places to explore
            (i.e., not blocked and within the grid)
        Parameters:
            cell:  the current Cell being explored
        Returns:
            a list of valid Cell objects (in N/S/W/E exploration) for further
            consideration
        '''
        direction_movements = {"N": (-1, 0), "S": (1, 0), "W": (0, -1), "E": (0, 1)}

        if self._search_order == SearchOrder.NSWE:
            directions = ["N", "S", "W", "E"]
        elif self._search_order == SearchOrder.NESW:
            directions = ["N", "E", "S", "W"]
        elif self._search_order == SearchOrder.RANDOM:
            directions = ["N", "S", "E", "W"]
            random.shuffle(directions)
            
        neighbors = []
        pos = cell.getPosition()
        row, col = pos.row, pos.col

        for i in directions: 
            dr, dc = direction_movements[i]
            new_row, new_col = row + dr, col + dc

            if 0 <= new_row < self._num_rows and 0 <= new_col < self._num_cols:
                neighbor = self._grid[new_row][new_col]
                if not neighbor.isBlocked():
                    neighbors.append(neighbor)

        return neighbors

    def dfs(self) -> Cell | None:
        ''' method to perform DFS (using a stack) to implement maze searching
        Returns:
            a Cell object corresponding to the Maze goal, or None if no goal
            can be found
        ''' 
        self._num_cells_explored = 0
        
        start = self.getStart()
        goal = self.getGoal()

        stack = Stack()
        explored = set()

        stack.push(start)
        explored.add(start.getPosition())

        while not stack.isEmpty():
            current = stack.pop()
            self._num_cells_explored += 1

            if current.isGoal():
                return current

            for neighbor in self.getSearchLocations(current):
                pos = neighbor.getPosition()
                if pos not in explored:
                    neighbor.setParent(current)
                    stack.push(neighbor)
                    explored.add(pos)

        return None

    def bfs(self) -> Cell | None:
        ''' method to perform BFS (using a queue) to implement maze searching
        Returns:
            a Cell object corresponding to the Maze goal, or None if no goal
            can be found
        ''' 
        self._num_cells_explored = 0

        start = self.getStart()
        goal = self.getGoal()

        queue = Queue()
        explored = set()

        queue.push(start)
        explored.add(start.getPosition())

        while not queue.isEmpty():
            current = queue.pop()
            self._num_cells_explored += 1

            if current.isGoal():
                return current

            for neighbor in self.getSearchLocations(current):
                pos = neighbor.getPosition()
                if pos not in explored:
                    neighbor.setParent(current)
                    queue.push(neighbor)
                    explored.add(pos)

        return None
    
    def manhattan(self, cell1: Cell, cell2: Cell) -> int:
        pos1, pos2 = cell1.getPosition(), cell2.getPosition()
        return abs(pos1.row - pos2.row) + abs(pos1.col - pos2.col)

    
    def aStar(self) -> Cell | None:
        ''' method to perform A* (using a priority queue) to implement maze searching
        Returns:
            a Cell object corresponding to the Maze goal, or None if no goal
            can be found
        '''
        self._num_cells_explored = 0

        start = self.getStart()
        goal = self.getGoal()

        to_explore = PriorityQueue[float, Cell]()
        seen: dict[Position, float] = {}

        start._cost = 0
        start._heur = self.manhattan(start, goal)
        to_explore.insert(start._cost + start._heur, start)
        seen[start.getPosition()] = 0
        self._num_cells_explored += 1

        while not to_explore.isEmpty():
            entry = to_explore.removeMin()
            current = entry.value

            if current.isGoal():
                return current

            for neighbor in self.getSearchLocations(current):
                pos = neighbor.getPosition()
                new_cost = current._cost + 1

                if pos not in seen or new_cost < seen[pos]:
                    self._num_cells_explored += 1

                    neighbor._cost = new_cost
                    neighbor._heur = self.manhattan(neighbor, goal)
                    neighbor.setParent(current)
                    seen[pos] = new_cost
                    to_explore.insert(neighbor._cost + neighbor._heur, neighbor)

        return None

    def showPath(self, goal: Cell) -> None:
        ''' method to update the path from start to goal, identifying the steps
            along the way as belonging to the path (updating the cell via
            .markOnPath, which will change that cell's ._contents to
            Contents.PATH), printing the final resulting solutions
        Parameters:
            goal: a Cell object corresponding to the goal location
        Returns:
            nothing -- just updates the cells in the grid to identify those on the path
        '''

        path = []
        cell = goal
        while cell._parent is not None:
            path.append(cell)
            cell = cell._parent
        path.append(cell)  # should be the start
        assert(cell == self._start)

        path.reverse()  # reverse the list

        for cell in path:
            if cell != self._start and cell != self._goal:
                cell.markOnPath()
        
        self._path_length = len(path)

        # print the maze, i.e., using __str__ which will show the solved maze
        print(self)

###################
def main() -> None:
    print("Testing open maze with no blocks")
    maze = Maze(3, 3, start=Position(0, 0), goal=Position(2, 2), prop_blocked=0.0)
    print("Maze with no blocks:")
    print(maze)

    print("\nChecking neighbors of middle cell (1,1):")
    cell = maze._grid[1][1]
    neighbors = maze.getSearchLocations(cell)
    print("Found:", [str(n.getPosition()) for n in neighbors])
    print("Should be 4 directions\n")

    print("Checking neighbors of corner cell (0,0):")
    corner = maze._grid[0][0]
    neighbors_corner = maze.getSearchLocations(corner)
    print("Found:", [str(n.getPosition()) for n in neighbors_corner])
    print("Should be 2 directions (down, right) in a 3x3 open maze\n")

    print("Running DFS on empty maze:")
    result_dfs = maze.dfs()
    if result_dfs:
        print("DFS reached goal at:", result_dfs.getPosition())
    else:
        print("DFS did not find a path")

    print("DFS with some blocked cells")
    maze2 = Maze(3, 3, start=Position(0, 0), goal=Position(2, 2), prop_blocked=0.3)
    print("\nMaze with some blocks (DFS):")
    print(maze2)
    result_dfs2 = maze2.dfs()
    if result_dfs2:
        print("DFS reached goal at:", result_dfs2.getPosition())
    else:
        print("DFS could not reach goal")

    print("BFS on empty maze")
    maze3 = Maze(3, 3, start=Position(0, 0), goal=Position(2, 2), prop_blocked=0.0)
    print("\nRunning BFS on empty maze:")
    result_bfs = maze3.bfs()
    if result_bfs:
        print("BFS reached goal at:", result_bfs.getPosition())
    else:
        print("BFS did not find a path")

    print("BFS with some blocked cells")
    maze4 = Maze(3, 3, start=Position(0, 0), goal=Position(2, 2), prop_blocked=0.3)
    print("\nMaze with some blocks (BFS):")
    print(maze4)
    result_bfs2 = maze4.bfs()
    if result_bfs2:
        print("BFS reached goal at:", result_bfs2.getPosition())
    else:
        print("BFS could not reach goal")

 
    print("\nTesting DFS, BFS, and A* on 30x30 mazes with different seeds")
    seeds = [8675309, 5551212, 1234567]

    for seed in seeds:
        print(f"\nSeed: {seed}")

        print("Testing DFS")
        random.seed(seed)
        maze_dfs = Maze(30, 30, prop_blocked=0.20, search_order=SearchOrder.NSWE)
        maze_dfs._num_cells_pushed = 0  # you'll need to increment this inside dfs
        goal_dfs = maze_dfs.dfs()
        if goal_dfs:
            print("\nDFS Solved Maze:")
            maze_dfs.showPath(goal_dfs)
            print(f"DFS Path Length: {maze_dfs._path_length}")
            print(f"DFS Cells Pushed: {maze_dfs._num_cells_pushed}")
        else:
            print("\nDFS could not find a path")

        print("Testing BFS")
        random.seed(seed)
        maze_bfs = Maze(30, 30, prop_blocked=0.20, search_order=SearchOrder.NSWE)
        maze_bfs._num_cells_pushed = 0
        goal_bfs = maze_bfs.bfs()
        if goal_bfs:
            print("\nBFS Solved Maze:")
            maze_bfs.showPath(goal_bfs)
            print(f"BFS Path Length: {maze_bfs._path_length}")
            print(f"BFS Cells Pushed: {maze_bfs._num_cells_pushed}")
        else:
            print("\nBFS could not find a path")

        print("Testing A*")
        random.seed(seed)
        maze_astar = Maze(30, 30, prop_blocked=0.20, search_order=SearchOrder.NSWE)
        goal_astar = maze_astar.aStar()
        if goal_astar:
            print("\nA* Solved Maze:")
            maze_astar.showPath(goal_astar)
            print(f"A* Path Length: {maze_astar._path_length}")
            print(f"A* Cells Inserted: {maze_astar._num_cells_explored}")
        else:
            print("\nA* could not find a path")

if __name__ == "__main__":
    main()