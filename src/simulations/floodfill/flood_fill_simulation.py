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
        self.last_cell_drawn = False

        self.simulation_time = 0

    def initialize(self, frame):
        self.queue.append((0, 0))
        self.cells_to_draw = [(0, 0)]
        self.visited_cells.add((0, 0))

    def finished(self):
        return self.last_cell_drawn

    def statistics(self):
        return {"Total Time (s)": self.simulation_time,
                "Number Cells Explored (cells)": len(self.visited_cells),
                "Percent Exploration (%)": len(self.visited_cells) / (MAZE_DIMENSION * MAZE_DIMENSION) * 100,
                "Route Distance": len(self.retrieve_path())}

    def retrieve_path(self):
        if not self.finished():
            return []

        path = [(MAZE_DIMENSION - 1, MAZE_DIMENSION - 1)]
        current_cell = path[-1]
        while current_cell[0] != 0 or current_cell[1] != 0:
            path.append(self.connected_graph[current_cell[0]][current_cell[1]])
            current_cell = path[-1]

        return list(reversed(path))

    def draw(self, frame, delta):
        while self.cells_to_draw:
            current_cell = self.cells_to_draw.pop()
            frame.create_rectangle(*Maze.__get_rectangle_coords__(current_cell), fill="green", outline="green")

            if current_cell[0] == MAZE_DIMENSION - 1 and current_cell[1] == MAZE_DIMENSION - 1:
                self.last_cell_drawn = True
                break

    def update(self, frame, delta):
        self.simulation_time += delta
        self.total_time += delta

        if self.total_time >= FILL_TIME:
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
