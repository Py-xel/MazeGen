from Maze import Maze


class MazeRepository:
    def __init__(self):
        self.mazes: dict[int, Maze] = dict()

    def save_or_update_maze(self, maze: Maze) -> Maze:
        if maze.id == None:
            maze.id = len(self.mazes)

        self.mazes[maze.id] = maze
        return maze

    def remove_maze(self, id: int) -> None:
        if id in self.mazes:
            self.mazes.pop(id)

    def get_maze(self, id: int) -> Maze:
        return self.mazes.get(id)

    def get_all_mazes(self) -> list[Maze]:
        return self.mazes.values()
