import random
from constants import *

# Create a maze using the depth-first algorithm described at
# https://scipython.com/blog/making-a-maze/
# Christian Hill, April 2017.


class Cell:
    wall_pairs = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}

    def has_all_walls(self):
        return all(self.walls.values())

    def knock_down_wall(self, other, wall):
        self.walls[wall] = False
        other.walls[Cell.wall_pairs[wall]] = False


class Maze:
    def __init__(self, size):
        self.nx, self.ny = size, size
        self.maze_map = [[Cell(x, y) for y in range(self.ny)] for x in range(self.nx)]

    def cell_at(self, x, y):
        return self.maze_map[x][y]

    def find_valid_neighbours(self, cell):
        delta = [('W', (-1,0)),
                 ('E', (1,0)),
                 ('S', (0,1)),
                 ('N', (0,-1))]
        neighbours = []
        for direction, (dx,dy) in delta:
            x2, y2 = cell.x + dx, cell.y + dy
            if (0 <= x2 < self.nx) and (0 <= y2 < self.ny):
                neighbour = self.cell_at(x2, y2)
                if neighbour.has_all_walls():
                    neighbours.append((direction, neighbour))
        return neighbours

    def make_maze(self):
        # Total number of cells.
        n = self.nx * self.ny
        cell_stack = []
        current_cell = self.cell_at(0, 0)
        # Total number of visited cells during maze construction.
        nv = 1

        while nv < n:
            neighbours = self.find_valid_neighbours(current_cell)

            if not neighbours:
                # We've reached a dead end: backtrack.
                current_cell = cell_stack.pop()
                continue

            direction, next_cell = random.choice(neighbours)
            current_cell.knock_down_wall(next_cell, direction)
            cell_stack.append(current_cell)
            current_cell = next_cell
            nv += 1

    def __str__(self):
        maze_rows = ['-' * self.nx*2]
        for y in range(self.ny):
            maze_row = ['|']
            for x in range(self.nx):
                if self.maze_map[x][y].walls['E']:
                    maze_row.append(' |')
                else:
                    maze_row.append('  ')
            maze_rows.append(''.join(maze_row))
            maze_row = ['|']
            for x in range(self.nx):
                if self.maze_map[x][y].walls['S']:
                    maze_row.append('-+')
                else:
                    maze_row.append(' +')
            maze_rows.append(''.join(maze_row))
        return '\n'.join(maze_rows)

    @staticmethod
    def north_boundary(cell_y):
        cell_width = MAZE_WIDTH / MAZE_DIMENSION
        return cell_y * cell_width + BORDER_SIZE + WALL_WIDTH

    @staticmethod
    def south_boundary(cell_y):
        cell_width = MAZE_WIDTH / MAZE_DIMENSION
        return (cell_y + 1) * cell_width + BORDER_SIZE

    @staticmethod
    def west_boundary(cell_x):
        cell_width = MAZE_WIDTH / MAZE_DIMENSION
        return cell_x * cell_width + BORDER_SIZE + WALL_WIDTH

    @staticmethod
    def east_boundary(cell_x):
        cell_width = MAZE_WIDTH / MAZE_DIMENSION
        return (cell_x + 1) * cell_width + BORDER_SIZE


def generate_maze(size):
    maze = Maze(size)
    maze.make_maze()

    #  TODO
    '''
    walls = []
    for x in range(size):
        for y in range(size):
            cell = maze.cell_at(x, y)
            val = 0
            if cell.walls['N']:
                val += 1
            val = val << 1
            if cell.walls['S']:
                val += 1
            val = val << 1
            if cell.walls['W']:
                val += 1
            val = val << 1
            if cell.walls['E']:
                val += 1
            walls.append(val)
    '''
    return maze



