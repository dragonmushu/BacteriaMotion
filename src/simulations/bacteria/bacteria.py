import math
import random

from src.simulations.bacteria.constants import *
from src.simulations.constants import *


class Bacteria:
    def __init__(self, run_velocity, tumble_velocity, tumble_angular_velocity, run_time, tumble_time):
        self.x = START_X
        self.y = START_Y
        self.radius = BACTERIA_RADIUS_PX

        self.run_velocity = run_velocity
        self.tumble_velocity = tumble_velocity
        self.tumble_angular_velocity = tumble_angular_velocity
        self.run_time = run_time
        self.tumble_time = tumble_time

        self.speed = tumble_velocity
        self.direction = self.random_value_range(0, 360)
        self.angular_velocity = self.random_value_range(-1 * tumble_angular_velocity, tumble_angular_velocity)

        self.total_motion_time = 0
        self.total_tumble_time = 0
        self.running = False

        self.path = [0]

    def remove(self, frame):
        frame.delete(self.id)

    def draw(self, frame):
        self.id = frame.create_oval(self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y +
                                    self.radius, outline="red", fill="red")

    def update_state(self, delta):
        if self.running and self.total_motion_time > self.run_time:
            self.running = False
            self.speed = self.tumble_velocity
            self.angular_velocity = self.random_value_range(-1 * self.tumble_angular_velocity,
                                                            self.tumble_angular_velocity)
            self.total_motion_time = 0
        elif not self.running and self.total_motion_time > self.tumble_time:
            self.running = True
            self.speed = self.run_velocity
            self.total_motion_time = 0
            self.total_tumble_time = 0
            self.angular_velocity = 0

        if not self.running:
            if self.total_tumble_time >= self.tumble_time / TUMBLE_DIRECTION_CHANGE_SPLIT:
                self.angular_velocity = self.random_value_range(-1 * self.tumble_angular_velocity,
                                                                self.tumble_angular_velocity)
                self.total_tumble_time = 0
            else:
                self.total_tumble_time += delta

    def update(self, delta, maze):
        self.total_motion_time += delta

        self.update_state(delta)

        self.direction = self.direction + self.angular_velocity * delta
        vx = math.cos(math.radians(self.direction)) * self.speed
        vy = math.sin(math.radians(self.direction)) * self.speed

        collision_y = False
        collision_x = False

        cell_width = MAZE_WIDTH / MAZE_DIMENSION
        cell_x = int((self.x - BORDER_SIZE) / cell_width)
        cell_y = int((self.y - BORDER_SIZE) / cell_width)
        cell = maze.cell_at(cell_x, cell_y)

        next_x = self.x + vx * delta
        next_y = self.y + vy * delta

        cell_left, cell_right, cell_up, cell_down = None, None, None, None
        if cell_x > 0:
            cell_left = maze.cell_at(cell_x - 1, cell_y)
        if cell_x < MAZE_DIMENSION - 1:
            cell_right = maze.cell_at(cell_x + 1, cell_y)
        if cell_y > 0:
            cell_up = maze.cell_at(cell_x, cell_y - 1)
        if cell_y < MAZE_DIMENSION - 1:
            cell_down = maze.cell_at(cell_x, cell_y + 1)

        if vy > 0:
            if cell.walls['S'] and next_y + self.radius >= maze.south_boundary(cell_y):
                self.y = maze.south_boundary(cell_y) - self.radius
                collision_y = True
            else:
                if next_x - self.radius <= maze.west_boundary(cell_x) and cell_left and cell_left.walls['S']:
                    a = next_x - maze.west_boundary(cell_x)
                    if next_x <= maze.west_boundary(cell_x):
                        b = self.radius
                    else:
                        b = math.sqrt(self.radius ** 2 - a ** 2)
                    if next_y + b >= maze.south_boundary(cell_y):
                        self.y = maze.south_boundary(cell_y) - b
                        collision_y = True
                if next_x + self.radius >= maze.east_boundary(cell_x) and cell_right and cell_right.walls['S']:
                    a = maze.east_boundary(cell_x) - next_x
                    if next_x >= maze.east_boundary(cell_x):
                        b = self.radius
                    else:
                        b = math.sqrt(self.radius ** 2 - a ** 2)
                    if next_y + b >= maze.south_boundary(cell_y):
                        self.y = maze.south_boundary(cell_y) - b
                        collision_y = True
        if vy < 0:
            if cell.walls['N'] and next_y - self.radius <= maze.north_boundary(cell_y):
                self.y = maze.north_boundary(cell_y) + self.radius
                collision_y = True
            else:
                if next_x - self.radius <= maze.west_boundary(cell_x) and cell_left and cell_left.walls['N']:
                    a = next_x - maze.west_boundary(cell_x)
                    if next_x <= maze.west_boundary(cell_x):
                        b = self.radius
                    else:
                        b = math.sqrt(self.radius ** 2 - a ** 2)
                    if next_y - b <= maze.north_boundary(cell_y):
                        self.y = maze.north_boundary(cell_y) + b
                        collision_y = True
                if next_x + self.radius >= maze.east_boundary(cell_x) and cell_right and cell_right.walls['N']:
                    a = maze.east_boundary(cell_x) - next_x
                    if next_x >= maze.east_boundary(cell_x):
                        b = self.radius
                    else:
                        b = math.sqrt(self.radius ** 2 - a ** 2)
                    if next_y - b <= maze.north_boundary(cell_y):
                        self.y = maze.north_boundary(cell_y) + b
                        collision_y = True
        if vx > 0:
            if cell.walls['E'] and next_x + self.radius >= maze.east_boundary(cell_x):
                self.x = maze.east_boundary(cell_x) - self.radius
                collision_x = True
            else:
                if next_y - self.radius <= maze.north_boundary(cell_y) and cell_up and cell_up.walls['E']:
                    a = next_y - maze.north_boundary(cell_y)
                    if next_y < maze.north_boundary(cell_y):
                        b = self.radius
                    else:
                        b = math.sqrt(self.radius ** 2 - a ** 2)
                    if next_x + b >= maze.east_boundary(cell_x):
                        self.x = maze.east_boundary(cell_x) - b
                        collision_x = True
                if next_y + self.radius >= maze.south_boundary(cell_y) and cell_down and cell_down.walls['E']:
                    a = maze.south_boundary(cell_y) - next_y
                    if next_y >= maze.south_boundary(cell_y):
                        b = self.radius
                    else:
                        b = math.sqrt(self.radius ** 2 - a ** 2)
                    if next_x + b >= maze.east_boundary(cell_x):
                        self.x = maze.east_boundary(cell_x) - b
                        collision_x = True
        if vx < 0:
            if cell.walls['W'] and next_x - self.radius <= maze.west_boundary(cell_x):
                self.x = maze.west_boundary(cell_x) + self.radius
                collision_x = True
            else:
                if next_y - self.radius <= maze.north_boundary(cell_y) and cell_up and cell_up.walls['E']:
                    a = next_y - maze.north_boundary(cell_y)
                    if next_y <= maze.north_boundary(cell_y):
                        b = self.radius
                    else:
                        b = math.sqrt(self.radius ** 2 - a ** 2)
                    if next_x - b <= maze.west_boundary(cell_x):
                        self.x = maze.west_boundary(cell_x) + b
                        collision_x = True
                if next_y + self.radius >= maze.south_boundary(cell_y) and cell_down and cell_down.walls['E']:
                    a = maze.south_boundary(cell_y) - next_y
                    if next_y >= maze.south_boundary(cell_y):
                        b = self.radius
                    else:
                        b = math.sqrt(self.radius ** 2 - a ** 2)
                    if next_x - b <= maze.west_boundary(cell_x):
                        self.x = maze.west_boundary(cell_x) + b
                        collision_x = True

        if not collision_y:
            self.y = next_y
        if not collision_x:
            self.x = next_x

        if self.path[-1] != cell_x * MAZE_DIMENSION + cell_y:
            self.path.append(cell_x * MAZE_DIMENSION + cell_y)

    @staticmethod
    def random_value_range(min_val, max_val):
        return random.random() * (max_val - min_val) + min_val
