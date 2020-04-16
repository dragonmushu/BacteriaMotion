from constants import *
from bacteria import Bacteria


class Bacteria_Simulation():

    def __init__(self, maze, run_velocity, tumble_velocity):
        self.maze = maze
        self.bacteria = [Bacteria(run_velocity, tumble_velocity, 0.8, 5) for i in range(0, NUMBER_BACTERIA)]

    def initialize(self, frame):
        for bacterium in self.bacteria:
            bacterium.draw(frame)

    def update(self, frame, delta):
        # delete objects
        for bacterium in self.bacteria:
            bacterium.remove(frame)
        # update bacteria
        for bacterium in self.bacteria:
            bacterium.update(delta, self.maze)
        # draw  object
        for bacterium in self.bacteria:
            bacterium.draw(frame)