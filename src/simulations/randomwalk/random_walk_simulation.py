from simulations.bacteria.bacteria_simulation import BacteriaSimulation
from simulations.randomwalk.constants import *


class RandomWalkSimulation(BacteriaSimulation):
    def __init__(self, maze):
        super().__init__(maze, RUN_VELOCITY, TUMBLE_VELOCITY, TUMBLE_ANGULAR_VELOCITY, RUN_TIME, TUMBLE_TIME)
