import tkinter as tk
import math
from constants import *


class MazeCanvas:

    def __init__(self, root):
        self.canvas = tk.Canvas(root, width=MAZE_WIDTH + 2 * BORDER_SIZE, height=PANEL_HEIGHT + 2 * BORDER_SIZE, background="black")
        self.canvas.grid(row=0, column=0)
        self.simulation = None

    def draw_maze(self, maze):
        # delete all
        self.canvas.delete("all")

        # size of maze
        maze_size = MAZE_DIMENSION  # TODO
        cell_width = MAZE_WIDTH / maze_size

        # draw border
        self.canvas.create_rectangle(BORDER_SIZE, BORDER_SIZE, BORDER_SIZE + MAZE_WIDTH + WALL_WIDTH,
                                     BORDER_SIZE + WALL_WIDTH, fill="red", outline="red")
        self.canvas.create_rectangle(BORDER_SIZE, BORDER_SIZE, BORDER_SIZE + WALL_WIDTH,
                                     BORDER_SIZE + MAZE_WIDTH + WALL_WIDTH, fill="red", outline="red")
        self.canvas.create_rectangle(BORDER_SIZE + MAZE_WIDTH, BORDER_SIZE, BORDER_SIZE + MAZE_WIDTH + WALL_WIDTH,
                                     BORDER_SIZE + MAZE_WIDTH + WALL_WIDTH, fill="red", outline="red")
        self.canvas.create_rectangle(BORDER_SIZE, BORDER_SIZE + MAZE_WIDTH, BORDER_SIZE + MAZE_WIDTH + WALL_WIDTH,
                                     BORDER_SIZE + MAZE_WIDTH + WALL_WIDTH, fill="red", outline="red")

        # draw vertical walls
        for r in range(1, maze_size):
            x = r * cell_width + BORDER_SIZE
            for c in range(maze_size):
                y = c * cell_width + BORDER_SIZE
                cell = maze.cell_at(r, c)
                if cell.walls['W']:
                    self.canvas.create_rectangle(x, y + WALL_WIDTH, x + WALL_WIDTH, y + cell_width, fill="red",
                                                 outline="red")

        # draw horizontal walls
        y = BORDER_SIZE + WALL_WIDTH
        for c in range(1, maze_size):
            y = c * cell_width + BORDER_SIZE
            for r in range(maze_size):
                x = r * cell_width + BORDER_SIZE
                cell = maze.cell_at(r, c)
                if cell.walls['N']:
                    self.canvas.create_rectangle(x + WALL_WIDTH, y, x + cell_width, y + WALL_WIDTH, fill="red",
                                                 outline="red")

        # draw pegs
        for r in range(1, maze_size):
            x = r * cell_width + BORDER_SIZE
            for c in range(1, maze_size):
                y = c * cell_width + BORDER_SIZE
                self.canvas.create_rectangle(x, y, x + WALL_WIDTH, y + WALL_WIDTH, fill="red",
                                             outline="red")

    def setup_simulation(self, simulation):
        self.simulation = simulation
        self.simulation.initialize(self.canvas)

    def update(self, delta):
        self.canvas.update()
        if self.simulation:
            self.simulation.update(self.canvas, delta)
            self.simulation.draw(self.canvas, delta)
