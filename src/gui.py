import tkinter as tk
import time
import random

from canvas import MazeCanvas
from constants import *
from simulations.bacteria.constants import *
from maze import generate_maze
from simulations.bacteria.bacteria_simulation import BacteriaSimulation
from simulations.wallfollow.right_wall_follow_simulation import RightWallFollowSimulation
from simulations.wallfollow.left_wall_follow_simulation import LeftWallFollowSimulation
from simulations.randomwalk.random_walk_simulation import RandomWalkSimulation
from simulations.floodfill.flood_fill_simulation import FloodFillSimulation


class Gui:

    def __init__(self, root):
        # create maze canvas
        self.canvas = MazeCanvas(root, self.simulation_finished)

        # create panel
        self.panel = tk.Frame(root, width=CONTROL_PANEL_WIDTH, height=PANEL_HEIGHT)
        self.panel.grid(row=0, column=1, sticky=tk.N)

        # generate panel interface
        self.generate_options_interface()
        self.generate_info_interface()

        # initialize random maze
        self.change_maze()
        self.draw_maze()

        # start simulation
        self.running_simulation = False

    def generate_label_with_dropdown(self, panel, title, options, row, column, command=None):
        label = tk.Label(panel, text=title)
        label.grid(row=row, column=column, padx=PANEL_BORDER, pady=PANEL_BORDER)
        value = tk.StringVar(panel)
        value.set(options[0])
        if command:
            dropdown = tk.OptionMenu(panel, value, *options, command=command)
        else:
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
        self.generate_label_with_dropdown(options_panel, BACTERIA_TYPE, bacteria_options, 0, 4,
                                          command=self.generate_bacteria_parameters)

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
        self.info_panel = tk.Frame(self.panel, width=CONTROL_PANEL_WIDTH, height=350, background="black")
        self.info_panel.grid(row=1, column=0)

        self.total_time = 0
        self.timer = tk.Label(self.info_panel, text=self.retrieve_time(self.total_time), background="black")
        self.timer.configure(foreground="white")
        self.timer.place(relx=1, rely=0, anchor='ne')

        self.stats = tk.Label(self.info_panel, text="", justify=tk.LEFT, background="black")
        self.stats.configure(foreground="white")
        self.stats.place(relx=0, rely=0, anchor='nw')

    def generate_bacteria_parameters(self, value):
        if value == INPUT_TYPE:
            self.run_velocity.set(0)
            self.run_time.set(0)
            self.tumble_time.set(0)
            self.tumble_angular_velocity.set(0)
            self.tumble_velocity.set(0)
        elif value == ECOLI_TYPE:
            self.run_velocity.set(E_COLI_RUN_VELOCITY)
            self.run_time.set(E_COLI_RUN_TIME)
            self.tumble_time.set(E_COLI_TUMBLE_TIME)
            self.tumble_angular_velocity.set(E_COLI_ANGULAR_VELOCITY)
            self.tumble_velocity.set(E_COLI_TUMBLE_VELOCITY)
        else:
            self.run_velocity.set(M_MAR_RUN_VELOCITY)
            self.run_time.set(M_MAR_RUN_TIME)
            self.tumble_time.set(M_MAR_TUMBLE_TIME)
            self.tumble_angular_velocity.set(M_MAR_ANGULAR_VELOCITY)
            self.tumble_velocity.set(M_MAR_TUMBLE_VELOCITY)

    def change_maze(self):
        self.total_time = 0

        maze_type = self.maze_value.get()
        if maze_type == RANDOM_MAZE:
            self.maze = generate_maze(size=MAZE_DIMENSION, multipath=random.randint(0, 1))
        elif maze_type == SINGLE_PATH_MAZE:
            self.maze = generate_maze(size=MAZE_DIMENSION)
        elif maze_type == MULTI_PATH_MAZE:
            self.maze = generate_maze(size=MAZE_DIMENSION, multipath=True)

        self.draw_maze()
        self.canvas.stop_simulation()

    def draw_maze(self):
        self.canvas.draw_maze(self.maze)

    def simulation_finished(self, data):
        text = ""
        for k, v in data.items():
            text += str(k) + " : " + str(v) + "\n"

        self.stats['text'] = text

    def run(self, simulation_type=BACTERIA_SIMULATION):
        self.draw_maze()
        self.canvas.stop_simulation()
        self.total_time = 0

        run_velocity = float(self.run_velocity.get()) * PIXEL_UM_RATIO
        tumble_velocity = float(self.tumble_velocity.get()) * PIXEL_UM_RATIO
        tumble_angular_velocity = math.degrees(float(self.tumble_angular_velocity.get()))
        run_time = float(self.run_time.get())
        tumble_time = float(self.tumble_time.get())

        if simulation_type == BACTERIA_SIMULATION:
            simulation = BacteriaSimulation(self.maze, run_velocity, tumble_velocity, tumble_angular_velocity, run_time,
                                            tumble_time)
        elif simulation_type == RANDOM_WALK_SIMULATION:
            simulation = RandomWalkSimulation(self.maze)
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

        if self.canvas.simulation_running():
            self.total_time += delta

        self.timer['text'] = self.retrieve_time(self.total_time)

    @staticmethod
    def retrieve_time(time):
        total_seconds = int(time)
        ms = int((time - total_seconds) * 1000)
        minutes = int(total_seconds / 60)
        seconds = total_seconds % 60

        str_minutes = str(minutes)
        str_seconds = str(seconds)
        str_ms = str(ms)

        if minutes < 10:
            str_minutes = "0" + str_minutes
        if seconds < 10:
            str_secs = "0" + str_seconds
        if ms < 10:
            str_ms = "00" + str_ms
        elif ms < 100:
            str_ms = "0" + str_ms

        return str_minutes + ":" + str_seconds + ":" + str_ms


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
    window.configure(background="black")
    window.title("Bacteria Maze Simulation")
    gui = Gui(window)
    run(window, gui)
