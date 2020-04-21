from builtins import staticmethod

from src.simulations.simulation import Simulation
from src.simulations.floodfill.flood_fill_simulation import FloodFillSimulation
from src.simulations.wallfollow.constants import *
from src.simulations.bacteria.constants import BACTERIA_RADIUS_PX
from src.simulations.constants import START_X, START_Y
from src.constants import MAZE_DIMENSION
from src.maze import Maze


class WallFollowSimulation(Simulation):
    def __init__(self, maze, wall_orientation):
        super().__init__(maze)

        self.orientation = wall_orientation
        self.speed = WALL_FOLLOW_SPEED
        self.x = START_X
        self.y = START_Y
        self.radius = BACTERIA_RADIUS_PX
        self.direction = INITIAL_DIRECTION
        self.current_cell = (0, 0)
        self.next_cell = (0, 0)

        self.total_time = 0
        self.path = [(0, 0)]
        self.new_cell_to_draw = (0, 0)

    def initialize(self, frame):
        self.draw(frame, 0)
        self.resolve_next_cell()

    def finished(self):
        return self.current_cell[0] == MAZE_DIMENSION - 1 and self.current_cell[1] == MAZE_DIMENSION - 1

    def statistics(self):
        return {"Total Time": self.total_time,
                "Number Cells Explored": len(self.path),
                "Percent Exploration": len(self.path) / (MAZE_DIMENSION * MAZE_DIMENSION),
                "Route Distance": len(self.path)}

    def retrieve_path(self):
        if not self.finished():
            return []

        if self.path[-1][0] != MAZE_DIMENSION - 1 or self.path[-1][1] != MAZE_DIMENSION - 1:
            self.path.pop()
        return self.path

    def remove(self, frame):
        frame.delete(self.id)

    def draw(self, frame, delta):
        if self.new_cell_to_draw:
            frame.create_rectangle(*FloodFillSimulation.__get_rectangle_coords__(self.new_cell_to_draw), fill="green",
                                   outline="green")
            self.new_cell_to_draw = None

        self.id = frame.create_oval(self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y +
                                    self.radius, outline="red", fill="red")

    def resolve_next_cell(self):
        self.current_cell = self.next_cell
        current_x = self.current_cell[0]
        current_y = self.current_cell[1]

        walls = self.maze.cell_at(current_x, current_y).walls
        front_wall = self.wall_in_front(walls)
        orientation_wall = self.wall_in_orientation(walls)
        opposite_wall = self.wall_against_orientation(walls)

        if not orientation_wall:
            self.turn_towards_orientation()
        elif front_wall and opposite_wall:
            self.turn_against_orientation()
            self.turn_against_orientation()
        elif front_wall:
            self.turn_against_orientation()

        self.next_cell = self.cell_in_front(current_x, current_y)
        self.path.append(self.next_cell)
        self.new_cell_to_draw = self.next_cell

    def cell_in_front(self, current_x, current_y):
        if self.direction == 'N':
            return current_x, current_y - 1
        elif self.direction == 'S':
            return current_x, current_y + 1
        elif self.direction == 'W':
            return current_x - 1, current_y
        else:
            return current_x + 1, current_y

    def turn(self, orientation):
        if self.direction == 'N':
            if orientation == LEFT_ORIENTATION:
                self.direction = 'W'
            else:
                self.direction = 'E'
        elif self.direction == 'S':
            if orientation == LEFT_ORIENTATION:
                self.direction = 'E'
            else:
                self.direction = 'W'
        elif self.direction == 'W':
            if orientation == LEFT_ORIENTATION:
                self.direction = 'S'
            else:
                self.direction = 'N'
        else:
            if orientation == LEFT_ORIENTATION:
                self.direction = 'N'
            else:
                self.direction = 'S'

    def turn_towards_orientation(self):
        self.turn(self.orientation)

    def turn_against_orientation(self):
        if self.orientation == LEFT_ORIENTATION:
            self.turn(RIGHT_ORIENTATION)
        else:
            self.turn(LEFT_ORIENTATION)

    def wall_on_side(self, walls, orientation):
        if self.direction == 'N':
            if orientation == LEFT_ORIENTATION:
                return walls['W']
            else:
                return walls['E']
        elif self.direction == 'S':
            if orientation == LEFT_ORIENTATION:
                return walls['E']
            else:
                return walls['W']
        elif self.direction == 'W':
            if orientation == LEFT_ORIENTATION:
                return walls['S']
            else:
                return walls['N']
        else:
            if orientation == LEFT_ORIENTATION:
                return walls['N']
            else:
                return walls['S']

    def wall_in_orientation(self, walls):
        return self.wall_on_side(walls, self.orientation)

    def wall_against_orientation(self, walls):
        if self.orientation == LEFT_ORIENTATION:
            return self.wall_on_side(walls, RIGHT_ORIENTATION)
        else:
            return self.wall_on_side(walls, LEFT_ORIENTATION)

    def wall_in_front(self, walls):
        return walls[self.direction]

    def fix_cell_and_resolve_next(self, next_x, next_y):
        self.x = next_x
        self.y = next_y
        self.resolve_next_cell()

    def update(self, frame, delta):
        self.remove(frame)
        self.total_time += delta

        next_cell_position = self.center_cell(self.next_cell)
        next_cell_x = next_cell_position[0]
        next_cell_y = next_cell_position[1]

        if self.direction == 'N':
            self.y = self.y - self.speed * delta
            if self.y <= next_cell_y:
                self.fix_cell_and_resolve_next(next_cell_x, next_cell_y)
        elif self.direction == 'S':
            self.y = self.y + self.speed * delta
            if self.y >= next_cell_y:
                self.fix_cell_and_resolve_next(next_cell_x, next_cell_y)
        elif self.direction == 'W':
            self.x = self.x - self.speed * delta
            if self.x <= next_cell_x:
                self.fix_cell_and_resolve_next(next_cell_x, next_cell_y)
        else:
            self.x = self.x + self.speed * delta
            if self.x >= next_cell_x:
                self.fix_cell_and_resolve_next(next_cell_x, next_cell_y)

    @staticmethod
    def center_cell(cell):
        x = Maze.west_boundary(cell[0]) + (Maze.east_boundary(cell[0]) - Maze.west_boundary(cell[0])) / 2
        y = Maze.north_boundary(cell[1]) + (Maze.south_boundary(cell[1]) - Maze.north_boundary(cell[1])) / 2
        return x, y
