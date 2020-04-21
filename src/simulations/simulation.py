from abc import ABC, abstractmethod


class Simulation(ABC):
    def __init__(self, maze):
        self.maze = maze

    @abstractmethod
    def initialize(self, frame):
        pass

    @abstractmethod
    def finished(self):
        pass

    @abstractmethod
    def statistics(self):
        pass

    @staticmethod
    def retrieve_path(self):
        pass

    @abstractmethod
    def draw(self, frame, delta):
        pass

    @abstractmethod
    def update(self, frame, delta):
        pass
