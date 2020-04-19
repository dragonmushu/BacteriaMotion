from abc import ABC, abstractmethod


class Simulation(ABC):
    def __init__(self, maze):
        self.maze = maze
        self._finished = False

    def finished(self):
        return self._finished

    @abstractmethod
    def draw(self, frame, delta):
        pass

    @abstractmethod
    def update(self, frame, delta):
        pass
