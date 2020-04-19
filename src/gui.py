import tkinter as tk
import time
import random
import math

from src.canvas import MazeCanvas
from src.constants import *
from src.maze import generate_maze
from src.simulations.bacteria.bacteria_simulation import BacteriaSimulation
from src.simulations.wallfollow.right_wall_follow_simulation import RightWallFollowSimulation
from src.simulations.wallfollow.left_wall_follow_simulation import LeftWallFollowSimulation
from src.simulations.floodfill.flood_fill_simulation import FloodFillSimulation


class Gui:

    def __init__(self, root):
        # create maze canvas
        self.canvas = MazeCanvas(root)

        # create panel
        self.panel = tk.Frame(root, width=CONTROL_PANEL_WIDTH, height=PANEL_HEIGHT)
        self.panel.grid(row=0, column=1, sticky=tk.N)

        # generate panel interface
        self.generate_options_interface()
        self.generate_info_interface()

        # initialize random maze
        self.change_maze()
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

    def generate_button(self, panel, title, callback, row, column):
        button = tk.Button(panel, text=title, command=callback, width=BUTTON_WIDTH)
        button.grid(row=row, column=column, padx=PANEL_BORDER, pady=PANEL_BORDER)

    def generate_options_interface(self):
        # create options panel
        options_panel = tk.Frame(self.panel, width=CONTROL_PANEL_WIDTH, height=OPTIONS_INTERFACE_HEIGHT)
        options_panel.grid(row=0, column=0, sticky=tk.N)

        # maze type
        maze_options = MAZE_OPTIONS
        self.maze_value = self.generate_label_with_dropdown(options_panel, MAZE_TYPE, maze_options, 0, 0)

        # run type
        run_type_options = RUN_OPTIONS
        self.run_value = self.generate_label_with_dropdown(options_panel, RUN_TYPE, run_type_options, 0, 2)

        # bacteria type
        bacteria_options = BACTERIA_OPTIONS
        self.bacteria_value = self.generate_label_with_dropdown(options_panel, BACTERIA_TYPE, bacteria_options, 0, 4)

        # run velocity
        self.run_velocity = self.generate_label_with_entry(options_panel, RUN_VELOCITY, 0.0, 1, 0)

        # tumble velocity
        self.tumble_velocity = self.generate_label_with_entry(options_panel, TUMBLE_VELOCITY, 0.0, 1, 2)

        # wall angle
        self.wall_angle = self.generate_label_with_entry(options_panel, WALL_BOUNCE, 0.0, 1, 4)

        # run time
        self.run_time = self.generate_label_with_entry(options_panel, RUN_TIME, 0.0, 2, 0)

        # tumble time
        self.tumble_time = self.generate_label_with_entry(options_panel, TUMBLE_TIME, 0.0, 2, 2)

        # tumble angular velocity
        self.tumble_angular_velocity = self.generate_label_with_entry(options_panel, TUMBLE_ANGULAR_VELOCITY, 0.0, 2, 4)

        # simulation run
        self.generate_button(options_panel, RUN_SIMULATION, self.run_simulation, 3, 5)

        # floodfill simulation run
        self.generate_button(options_panel, FLOOD_FILL, self.run_flood_fill, 3, 3)

        # change maze
        self.generate_button(options_panel, CHANGE_MAZE, self.change_maze, 3, 1)

    def generate_info_interface(self):
        info_panel = tk.Frame(self.panel, width=CONTROL_PANEL_WIDTH, height=INFO_INTERFACE_HEIGHT, background="red")
        info_panel.grid(row=1, column=0)

    def change_maze(self):
        self.canvas.stop_simulation()

        maze_type = self.maze_value.get()
        if maze_type == RANDOM_MAZE:
            self.maze = generate_maze(size=MAZE_DIMENSION, multipath=random.randint(0, 1))
        elif maze_type == SINGLE_PATH_MAZE:
            self.maze = generate_maze(size=MAZE_DIMENSION)
        elif maze_type == MULTI_PATH_MAZE:
            self.maze = generate_maze(size=MAZE_DIMENSION, multipath=True)

        self.draw_maze()

    def draw_maze(self):
        self.canvas.draw_maze(self.maze)

    def run(self, simulation_type=BACTERIA_SIMULATION):
        self.draw_maze()

        run_velocity = float(self.run_velocity.get())
        tumble_velocity = float(self.tumble_velocity.get())
        tumble_angular_velocity = math.degrees(float(self.tumble_angular_velocity.get()))
        run_time = float(self.run_time.get())
        tumble_time = float(self.tumble_time.get())

        if simulation_type == BACTERIA_SIMULATION:
            simulation = BacteriaSimulation(self.maze, run_velocity, tumble_velocity, tumble_angular_velocity, run_time,
                                            tumble_time)
        elif simulation_type == RANDOM_WALK_SIMULATION:
            pass
        elif simulation_type == LEFT_WALL_FOLLOW_SIMULATION:
            simulation = LeftWallFollowSimulation(self.maze)
        elif simulation_type == RIGHT_WALL_FOLLOW_SIMULATION:
            simulation = RightWallFollowSimulation(self.maze)
        else:
            simulation = FloodFillSimulation(self.maze)

        self.canvas.setup_simulation(simulation)

    def run_simulation(self):
        self.run(simulation_type=self.run_value.get())

    def run_flood_fill(self):
        self.run(simulation_type=FLOOD_FILL)

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
