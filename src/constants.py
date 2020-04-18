import random

#### GUI DIMENSIONS ####
BORDER_SIZE = 5
PANEL_HEIGHT = 500
MAZE_WIDTH = 500

#### CONTROL PANEL DIMENSIONS ####
CONTROL_PANEL_WIDTH = 700
OPTIONS_INTERFACE_HEIGHT = 300
INFO_INTERFACE_HEIGHT = 200
PANEL_BORDER = 2


#### CONTROL PANEL OPTIONS ####
MAZE_TYPE = "Maze"
RANDOM_MAZE = "Random"
SINGLE_PATH_MAZE = "Single Path"
MULTI_PATH_MAZE = "Multi Path"
MAZE_OPTIONS = [RANDOM_MAZE, SINGLE_PATH_MAZE, MULTI_PATH_MAZE]

#### MAZE CONSTANTS ####
MAZE_DIMENSION = 20
WALL_WIDTH = 2

#### BIOLOGICAL DIMENSIONS ####
AVG_BACTERIA_RADIUS = 1 # microns
CHANNEL_WIDTH = 3 # microns
CHANNEL_WIDTH_PX = (MAZE_WIDTH - 2 * BORDER_SIZE) / MAZE_DIMENSION - WALL_WIDTH
BACTERIA_RADIUS_PX = AVG_BACTERIA_RADIUS * CHANNEL_WIDTH_PX / CHANNEL_WIDTH

#### AGENT CONSTANTS ####
START_X = (MAZE_WIDTH - 2 * BORDER_SIZE) / MAZE_DIMENSION / 2 + BORDER_SIZE
START_Y = (MAZE_WIDTH - 2 * BORDER_SIZE) / MAZE_DIMENSION / 2 + BORDER_SIZE


#### GUI FPS ####
FPS = 60


#### BACTERIA SIMULATION ####
NUMBER_BACTERIA = 50
BACTERIA_RUN_VELOCITY_MIN = 30
BACTERIA_RUN_VELOCITY_MAX = 100

BACTERIA_MOTION_TIME_MIN = 0.5
BACTERIA_MOTION_TIME_MAX = 3

BACTERIA_TUMBLE_ROTATION_MIN = -100
BACTERIA_TUMBLE_ROTATION_MAX = 100

BACTERIA_TUMBLE_VELOCITY_MIN = 15
BACTERIA_TUMBLE_VELOCITY_MAX = 50


#### FLOOD FILL AL

def random_value_range(min, max):
    return random.random() * (max - min) + min
