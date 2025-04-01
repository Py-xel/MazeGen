from LegendType import LegendType
from Coordinate import Coordinate


class MazeData:

    def __init__(
        self,
        size,
        maze_array,
        legends: dict[LegendType, list[float]],
        solutions: dict[Coordinate, int],
    ):
        self.size = size
        self.maze_array = maze_array
        self.legends = legends
        self.solutions = solutions
        if solutions is None:
            self.title = "Maze"
        else:
            self.title = "Maze Solutions"
