from constants import *
from collections import deque
from maze import Maze

class FloodFill_Simulation():

    def __init__(self, maze):
        self.maze = maze
        self.queue = deque()

        self.update_time = 0.2
        self.backwards_update_time = 0.1

        self.total_time = 0
        self.cells_to_update = []
        self.visited_cells = set()
        self.connected = [[(0, 0) for i in range(0, MAZE_DIMENSION)] for i in range(0, MAZE_DIMENSION)]
        self.update_final_path = False

    def initialize(self, frame):
        self.queue.append((0, 0))
        self.cells_to_update = [(0, 0)]
        self.visited_cells.add((0, 0))
        self.ended = False
        self.current_backward_cell = (MAZE_DIMENSION - 1, MAZE_DIMENSION - 1)

    def simulation_ended(self):
        return self.ended

    def draw(self, frame, delta):
        if self.update_final_path and self.current_backward_cell is not None:
            cell_x = self.current_backward_cell[0]
            cell_y = self.current_backward_cell[1]
            x1 = Maze.west_boundary(cell_x)
            y1 = Maze.north_boundary(cell_y)
            x2 = Maze.east_boundary(cell_x)
            y2 = Maze.south_boundary(cell_y)
            frame.create_rectangle(x1, y1, x2, y2, fill="blue", outline="blue")
        else:
            while self.cells_to_update:
                current_cell = self.cells_to_update.pop()
                cell_x = current_cell[0]
                cell_y = current_cell[1]
                x1 = Maze.west_boundary(cell_x)
                y1 = Maze.north_boundary(cell_y)
                x2 = Maze.east_boundary(cell_x)
                y2 = Maze.south_boundary(cell_y)
                frame.create_rectangle(x1 + 1, y1 + 1, x2 - 1, y2 - 1, fill="green", outline="green")

                if cell_x == MAZE_DIMENSION - 1 and cell_y == MAZE_DIMENSION - 1:
                    self.update_final_path = True
                    cell_x = self.current_backward_cell[0]
                    cell_y = self.current_backward_cell[1]
                    x1 = Maze.west_boundary(cell_x)
                    y1 = Maze.north_boundary(cell_y)
                    x2 = Maze.east_boundary(cell_x)
                    y2 = Maze.south_boundary(cell_y)
                    frame.create_rectangle(x1, y1, x2, y2, fill="blue", outline="blue")



    def update(self, frame, delta):

        self.total_time += delta

        if self.update_final_path and self.total_time >= self.backwards_update_time:
            cell_x = self.current_backward_cell[0]
            cell_y = self.current_backward_cell[1]
            self.current_backward_cell = self.connected[cell_x][cell_y]
            self.total_time = 0
        elif not self.update_final_path and self.total_time >= self.update_time:
            new_q = deque()
            while self.queue:
                current_cell = self.queue.popleft()
                x = current_cell[0]
                y = current_cell[1]
                walls = self.maze.cell_at(x, y).walls
                if not walls['N'] and y - 1 >= 0 and (x, y-1) not in self.visited_cells:
                    new_q.append((x, y - 1))
                    self.connected[x][y - 1] = (x, y)
                if not walls['S'] and y + 1 < MAZE_DIMENSION and (x, y+1) not in self.visited_cells:
                    new_q.append((x, y + 1))
                    self.connected[x][y + 1] = (x, y)
                if not walls['W'] and x - 1 >= 0 and (x - 1, y) not in self.visited_cells:
                    new_q.append((x - 1, y))
                    self.connected[x - 1][y] = (x, y)
                if not walls['E'] and x + 1 < MAZE_DIMENSION and (x + 1, y) not in self.visited_cells:
                    new_q.append((x + 1, y))
                    self.connected[x + 1][y] = (x, y)

            while new_q:
                cell = new_q.popleft()
                self.queue.append(cell)
                self.cells_to_update.append(cell)
                self.visited_cells.add(cell)

            self.total_time = 0
