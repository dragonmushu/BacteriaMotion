from src.simulations.simulation import Simulation
from src.simulations.bacteria.constants import *
from src.simulations.bacteria.bacteria import Bacteria
from src.maze import Maze
from src.constants import MAZE_DIMENSION


class BacteriaSimulation(Simulation):
    def __init__(self, maze, run_velocity, tumble_velocity, tumble_angular_velocity, run_time, tumble_time):
        super().__init__(maze)

        self.bacteria = [Bacteria(run_velocity, tumble_velocity, tumble_angular_velocity, run_time, tumble_time)
                         for i in range(0, NUMBER_BACTERIA)]

        self.total_time = 0
        self.cells_covered = {(0, 0)}
        self.new_cells_covered = [(0, 0)]

    def initialize(self, frame):
        for bacterium in self.bacteria:
            bacterium.draw(frame)

    def retrieve_path(self):
        fastest_path_distance = -1
        final_path = []

        for bacterium in self.bacteria:
            path = bacterium.retrieve_path()
            if bacterium.completed_maze:
                if fastest_path_distance == -1 or len(path) < fastest_path_distance:
                    fastest_path_distance = len(path)
                    final_path = path

        return final_path

    def write_statistics(self):
        count = 0
        for bacterium in self.bacteria:
            if bacterium.completed_maze:
                path = bacterium.retrieve_path()
                print("Bacteria ", count)
                print("Total Time: ", bacterium.total_time)
                print("Route Distance: ", len(path))
                print("Cells Visited: ", len(set(path)))
                count += 1
                print("\n")

    def statistics(self):
        self.write_statistics()

        number_bacteria_completed = 0

        avg_time = 0
        avg_route_distance = 0
        avg_number_cells_visited = 0

        fastest_path_distance = -1
        fastest_time = -1

        for bacterium in self.bacteria:
            path = bacterium.retrieve_path()
            if bacterium.completed_maze:
                number_bacteria_completed += 1
                avg_route_distance += len(path)
                avg_time += bacterium.total_time
                if fastest_path_distance == -1 or len(path) < fastest_path_distance:
                    fastest_path_distance = len(path)
                if fastest_time == -1 or bacterium.total_time < fastest_time:
                    fastest_time = bacterium.total_time

            avg_number_cells_visited += len(set(path))

        if number_bacteria_completed == 0:
            number_bacteria_completed = 1

        avg_number_cells_visited = avg_number_cells_visited / NUMBER_BACTERIA

        return {"Success Rate (%)": number_bacteria_completed / NUMBER_BACTERIA * 100,
                "Average Successful Total Time (s)": avg_time / number_bacteria_completed,
                "Average Successful Path Distance (cells)": avg_route_distance / number_bacteria_completed,
                "Average Cells Explored (cells)": avg_number_cells_visited,
                "Average Percent Exploration (all bacteria) (%)": avg_number_cells_visited / (MAZE_DIMENSION * MAZE_DIMENSION) * 100,
                "Shortest Path Distance (cells)": fastest_path_distance,
                "Fastest Time (s)": fastest_time}

    def finished(self):
        return self.total_time >= SIMULATION_TIME

    def draw(self, frame, delta):
        while self.new_cells_covered:
            current_cell = self.new_cells_covered.pop()
            frame.create_rectangle(*Maze.__get_rectangle_coords__(current_cell), fill="green", outline="green")
        # draw  object
        for bacterium in self.bacteria:
            bacterium.draw(frame)

    def update(self, frame, delta):
        self.total_time += delta

        # delete objects
        for bacterium in self.bacteria:
            bacterium.remove(frame)
        # update bacteria
        for bacterium in self.bacteria:
            bacterium.update(delta, self.maze)
        for bacterium in self.bacteria:
            path = bacterium.retrieve_path()
            if not path[-1] in self.cells_covered:
                self.new_cells_covered.append(path[-1])
                self.cells_covered.add(path[-1])
