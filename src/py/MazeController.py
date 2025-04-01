from MazeService import MazeService
from Maze import Maze


class MazeController:

    def __init__(self):
        self.service = MazeService()
        pass

    def create_maze(self, size: int, scarcity: float) -> Maze:
        return self.service.generate(size, scarcity)

    def solve_maze(self, maze: Maze) -> None:
        self.service.solve_maze(maze)
