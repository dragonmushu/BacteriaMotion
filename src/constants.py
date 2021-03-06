# GUI DIMENSIONS #
BORDER_SIZE = 5
PANEL_HEIGHT = 500
MAZE_WIDTH = 500

# CONTROL PANEL DIMENSIONS #
CONTROL_PANEL_WIDTH = 750
OPTIONS_INTERFACE_HEIGHT = 300
INFO_INTERFACE_HEIGHT = 200
PANEL_BORDER = 2
BUTTON_WIDTH = 10

# CONTROL PANEL OPTIONS #
MAZE_TYPE = "Maze"
RANDOM_MAZE = "Random"
SINGLE_PATH_MAZE = "Single Path"
MULTI_PATH_MAZE = "Multi Path"
MAZE_OPTIONS = [RANDOM_MAZE, SINGLE_PATH_MAZE, MULTI_PATH_MAZE]

RUN_TYPE = "Simulation"
BACTERIA_SIMULATION = "Bacteria"
RANDOM_WALK_SIMULATION = "Random Walk"
LEFT_WALL_FOLLOW_SIMULATION = "Left Wall Follow"
RIGHT_WALL_FOLLOW_SIMULATION = "Right Wall Follow"
RUN_OPTIONS = [BACTERIA_SIMULATION, RANDOM_WALK_SIMULATION, LEFT_WALL_FOLLOW_SIMULATION, RIGHT_WALL_FOLLOW_SIMULATION]

BACTERIA_TYPE = "Bacteria"
INPUT_TYPE = "Input"
ECOLI_TYPE = "E. coli"
MARINUS_TYPE = "M. marinus"
BACTERIA_OPTIONS = [INPUT_TYPE, ECOLI_TYPE]

RUN_VELOCITY = "Run Velocity (um/s)"
TUMBLE_VELOCITY = "Tumble Velocity (um/s)"
WALL_BOUNCE = "Wall Bounce (rad)"
RUN_TIME = "Run Time (s)"
TUMBLE_TIME = "Tumble Time (s)"
TUMBLE_ANGULAR_VELOCITY = "Angular Velocity (rad/s)"

RUN_SIMULATION = "Run"
FLOOD_FILL = "BFS"
CHANGE_MAZE = "Change Maze"

# MAZE CONSTANTS #
MAZE_DIMENSION = 20
WALL_WIDTH = 2
CHANNEL_WIDTH_PX = (MAZE_WIDTH - 2 * BORDER_SIZE) / MAZE_DIMENSION - WALL_WIDTH
CHANNEL_WIDTH = 6  # um
PIXEL_UM_RATIO = CHANNEL_WIDTH_PX / CHANNEL_WIDTH

# GUI FPS #
FPS = 60

# FINAL PATH #
FINAL_PATH_SPEED = 0.1
