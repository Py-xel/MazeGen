from MazeService import MazeService
from Maze import Maze


class MazeController:

    def __init__(self):
        self.service = MazeService()
        pass

    def create_maze(self, size: int, scarcity: float) -> Maze:
        maze = self.service.generate(size, scarcity)
        return self.service.save_or_update_maze(maze)

    def update_maze(self, maze: Maze) -> Maze:
        return self.service.save_or_update_maze(maze)

    def solve_maze(self, maze: Maze) -> None:
        solved_maze = self.service.solve_maze(maze)
        return self.service.save_or_update_maze(solved_maze)

    def find_maze_by_id(self, id: int) -> Maze:
        found = self.service.get_maze_by_id(id)
        if found != None:
            return found

    def find_all_mazes(self) -> list[Maze]:
        return self.service.get_all_mazes()
