from src.simulations.wallfollow.wall_follow_simulation import WallFollowSimulation
from src.simulations.wallfollow.constants import LEFT_ORIENTATION


class LeftWallFollowSimulation(WallFollowSimulation):
    def __init__(self, maze):
        super().__init__(maze, LEFT_ORIENTATION)
