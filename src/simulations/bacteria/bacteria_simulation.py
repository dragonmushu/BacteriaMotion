from src.simulations.simulation import Simulation
from src.simulations.bacteria.constants import *
from src.simulations.bacteria.bacteria import Bacteria


class BacteriaSimulation(Simulation):
    def __init__(self, maze, run_velocity, tumble_velocity, tumble_angular_velocity, run_time, tumble_time):
        super().__init__(maze)

        self.bacteria = [Bacteria(run_velocity, tumble_velocity, tumble_angular_velocity, run_time, tumble_time)
                         for i in range(0, NUMBER_BACTERIA)]

    def initialize(self, frame):
        for bacterium in self.bacteria:
            bacterium.draw(frame)

    def finished(self):
        pass

    def draw(self, frame, delta):
        # draw  object
        for bacterium in self.bacteria:
            bacterium.draw(frame)

    def update(self, frame, delta):
        # delete objects
        for bacterium in self.bacteria:
            bacterium.remove(frame)
        # update bacteria
        for bacterium in self.bacteria:
            bacterium.update(delta, self.maze)
