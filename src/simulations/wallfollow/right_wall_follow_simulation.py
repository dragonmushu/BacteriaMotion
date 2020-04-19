from src.simulations.wallfollow.wall_follow_simulation import WallFollowSimulation
from src.simulations.wallfollow.constants import RIGHT_ORIENTATION


class RightWallFollowSimulation(WallFollowSimulation):
    def __init__(self, maze):
        super().__init__(maze, RIGHT_ORIENTATION)
