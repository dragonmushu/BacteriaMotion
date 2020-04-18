import tkinter as tk
import time
from canvas import MazeCanvas
from constants import *
from maze import generate_maze
from bacteria_simulation import Bacteria_Simulation
from floodfill_simulation import FloodFill_Simulation


class Gui:

    def __init__(self, root):
        # create maze canvas
        self.canvas = MazeCanvas(root)

        # create panel
        self.panel = tk.Frame(root, width=CONTROL_PANEL_WIDTH, height=1000)
        self.panel.grid(row=0, column=1, sticky=tk.N)

        # generate panel interface
        self.generate_options_interface()
        self.generate_info_interface()

        # initialize random maze
        self.draw_maze()

    def generate_label_with_dropdown(self, panel, title, options, row, column):
        label = tk.Label(panel, text=title)
        label.grid(row=row, column=column, padx=PANEL_BORDER, pady=PANEL_BORDER)
        value = tk.StringVar(panel)
        value.set(options[0])
        dropdown = tk.OptionMenu(panel, value, *options)
        dropdown.grid(row=row, column=column + 1, padx=PANEL_BORDER, pady=PANEL_BORDER)
        return value

    def generate_label_with_entry(self, panel, title, initial_value, row, column):
        label = tk.Label(panel, text=title)
        label.grid(row=row, column=column, padx=PANEL_BORDER, pady=PANEL_BORDER)
        value = tk.StringVar(panel)
        value.set(str(initial_value))
        entry = tk.Entry(panel, textvariable=value, width=10)
        entry.grid(row=row, column=column + 1, padx=PANEL_BORDER, pady=PANEL_BORDER)
        return value

    def generate_options_interface(self):
        # create options panel
        options_panel = tk.Frame(self.panel, width=CONTROL_PANEL_WIDTH, height=OPTIONS_INTERFACE_HEIGHT)
        options_panel.grid(row=0, column=0, sticky=tk.N)

        # maze type
        maze_options = MAZE_OPTIONS
        self.maze_value = self.generate_label_with_dropdown(options_panel, MAZE_TYPE, maze_options, 0, 0)

        # run type
        run_type_options = ["Bacteria", "Random Walk", "Wall Follow"]
        self.run_value = self.generate_label_with_dropdown(options_panel, "Run: ", run_type_options, 0, 2)

        # bacteria type
        bacteria_options = ["E. coli", "M. marinus"]
        self.bacteria_value = self.generate_label_with_dropdown(options_panel, "Bacteria Type: ", bacteria_options, 0, 4)

        # run velocity
        self.run_velocity = self.generate_label_with_entry(options_panel, "Run Velocity: ", 0.0, 1, 0)

        # tumble velocity
        self.tumble_velocity = self.generate_label_with_entry(options_panel, "Tumble Velocity: ", 0.0, 1, 2)

        # wall angle
        self.wall_angle = self.generate_label_with_entry(options_panel, "Wall Bounce Angle: ", 0.0, 1, 4)

        # memory
        self.memory = self.generate_label_with_entry(options_panel, "Cell Memory: ", 0, 2, 0)

        # Energy
        self.energy = self.generate_label_with_entry(options_panel, "Energy: ", 0.0, 2, 2)

        # simulation run
        run = tk.Button(options_panel, text="Run Simulation", command=self.run_simulation)

        # floodfill simulation run
        floodfill = tk.Button(options_panel, text="Flood Fill", command=self.run_floodfill)

        run.grid(row=3, column=5, padx=5 * PANEL_BORDER, pady=PANEL_BORDER * 10)
        floodfill.grid(row=3, column=3, padx=5 * PANEL_BORDER, pady=PANEL_BORDER * 10)

    def generate_info_interface(self):
        info_panel = tk.Frame(self.panel, width=CONTROL_PANEL_WIDTH, height=INFO_INTERFACE_HEIGHT, background="red")
        info_panel.grid(row=1, column=0)

    def read_stored_mazes(self):
        pass

    def draw_maze(self, index=-1, multipath=False):
        if index == -1:
            self.maze = generate_maze(size=MAZE_DIMENSION, multipath=multipath)
        self.canvas.draw_maze(self.maze)

    def run(self, floodfill=False):
        maze_type = self.maze_value.get()
        if maze_type == RANDOM_MAZE:
            self.draw_maze()
        elif maze_type == MULTI_PATH_MAZE:
            self.draw_maze(multipath=True)

        run_velocity = float(self.run_velocity.get())
        tumble_velocity = float(self.tumble_velocity.get())

        if floodfill:
            simulation = FloodFill_Simulation(self.maze)
        else:
            simulation = Bacteria_Simulation(self.maze, run_velocity, tumble_velocity)

        self.canvas.setup_simulation(simulation)

    def run_simulation(self, type="bacteria"):
        self.run()

    def run_floodfill(self):
        self.run(floodfill=True)

    def update(self, delta):
        self.canvas.update(delta)

def run(window, frame):
    delta = 0
    while True:
        start_time = time.time()

        frame.update(delta)
        window.update()

        elapsed_time = time.time() - start_time
        if elapsed_time < 1 / FPS:
            sleep_time = 1 / FPS - elapsed_time
            time.sleep(sleep_time)
        delta = time.time() - start_time


if __name__ == '__main__':
    window = tk.Tk()
    window.title("Bacteria Maze Simulation")
    gui = Gui(window)
    run(window, gui)
