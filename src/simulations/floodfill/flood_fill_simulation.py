from collections import deque

from src.simulations.simulation import Simulation
from src.simulations.floodfill.constants import *
from src.constants import *
from src.maze import Maze


class FloodFillSimulation(Simulation):
    def __init__(self, maze):
        super().__init__(maze)

        self.total_time = 0
        self.queue = deque()
        self.visited_cells = set()
        self.connected_graph = [[(0, 0) for i in range(0, MAZE_DIMENSION)] for i in range(0, MAZE_DIMENSION)]
        self.cells_to_draw = []
        self.update_final_path = False
        self.previous_cell = (MAZE_DIMENSION - 1, MAZE_DIMENSION - 1)
        self.last_cell_drawn = False

    def initialize(self, frame):
        self.queue.append((0, 0))
        self.cells_to_draw = [(0, 0)]
        self.visited_cells.add((0, 0))

    def finished(self):
        return self.last_cell_drawn

    def draw(self, frame, delta):
        while self.cells_to_draw:
            current_cell = self.cells_to_draw.pop()

            if self.update_final_path:
                frame.create_rectangle(*self.__get_rectangle_coords__(current_cell), fill="blue", outline="blue")

                if current_cell[0] == 0 and current_cell[1] == 0:
                    self.last_cell_drawn = True
            else:
                frame.create_rectangle(*self.__get_rectangle_coords__(current_cell), fill="green", outline="green")

                if current_cell[0] == MAZE_DIMENSION - 1 and current_cell[1] == MAZE_DIMENSION - 1:
                    self.update_final_path = True
                    self.cells_to_draw = [(MAZE_DIMENSION - 1, MAZE_DIMENSION - 1)]

    def update(self, frame, delta):
        self.total_time += delta

        if self.update_final_path and self.total_time >= SOLUTION_TIME:
            cell_x = self.previous_cell[0]
            cell_y = self.previous_cell[1]
            next_cell = self.connected_graph[cell_x][cell_y]

            self.cells_to_draw.append(next_cell)
            self.previous_cell = next_cell

            self.total_time = 0
        elif not self.update_final_path and self.total_time >= FILL_TIME:
            new_cells = deque()
            while self.queue:
                current_cell = self.queue.popleft()
                x = current_cell[0]
                y = current_cell[1]
                walls = self.maze.cell_at(x, y).walls
                if not walls['N'] and y - 1 >= 0 and (x, y - 1) not in self.visited_cells:
                    new_cells.append((x, y - 1))
                    self.connected_graph[x][y - 1] = (x, y)
                if not walls['S'] and y + 1 < MAZE_DIMENSION and (x, y + 1) not in self.visited_cells:
                    new_cells.append((x, y + 1))
                    self.connected_graph[x][y + 1] = (x, y)
                if not walls['W'] and x - 1 >= 0 and (x - 1, y) not in self.visited_cells:
                    new_cells.append((x - 1, y))
                    self.connected_graph[x - 1][y] = (x, y)
                if not walls['E'] and x + 1 < MAZE_DIMENSION and (x + 1, y) not in self.visited_cells:
                    new_cells.append((x + 1, y))
                    self.connected_graph[x + 1][y] = (x, y)

            while new_cells:
                cell = new_cells.popleft()
                self.queue.append(cell)
                self.cells_to_draw.append(cell)
                self.visited_cells.add(cell)

            self.total_time = 0

    @staticmethod
    def __get_rectangle_coords__(cell):
        cell_x = cell[0]
        cell_y = cell[1]
        x1 = Maze.west_boundary(cell_x) + 1
        y1 = Maze.north_boundary(cell_y) + 1
        x2 = Maze.east_boundary(cell_x) - 1
        y2 = Maze.south_boundary(cell_y) - 1
        return x1, y1, x2, y2
