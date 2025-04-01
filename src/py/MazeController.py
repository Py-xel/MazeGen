from MazeService import MazeService
from Maze import Maze
from MazeStat import MazeStat
import pandas as pd
import time


class MazeController:

    def __init__(self):
        self.service = MazeService()
        pass

    def create_maze(self, size: int, scarcity: float) -> Maze | None:
        start_time = time.time()
        maze = self.service.generate(size, scarcity)
        end_time = time.time()
        # Convert to milliseconds
        build_time = round((end_time - start_time) * 1000, 2)
        if maze is not None:
            stat = MazeStat(size, scarcity, build_time)
            maze.set_stat(stat)
            return self.service.save_or_update_maze(maze)

    def update_maze(self, maze: Maze) -> Maze:
        if maze is not None:
            return self.service.save_or_update_maze(maze)

    def solve_maze(self, maze: Maze) -> Maze | None:
        if maze is not None:
            start_time = time.time()
            solved_maze = self.service.solve_maze(maze)
            end_time = time.time()
            # Convert to milliseconds
            solve_time = round((end_time - start_time) * 1000, 2)
            maze.update_solution_stat(solve_time)
            return self.service.save_or_update_maze(solved_maze)

    def find_maze_by_id(self, id: int) -> Maze:
        found = self.service.get_maze_by_id(id)
        if found != None:
            return found

    def find_all_mazes(self) -> list[Maze]:
        return self.service.get_all_mazes()

    def remove_maze_by_id(self, id: int) -> None:
        return self.service.remove_maze_by_id(id)

    def import_mazes(self, df: pd.DataFrame) -> list[Maze]:
        result: list[Maze] = list()
        for values in df.to_numpy():
            if len(values) == 2:
                try:
                    size = int(values[0])
                    value_str = str(values[1]).replace(",", ".")
                    scarcity = float(value_str)
                    maze = self.create_maze(size, scarcity)
                    if maze is not None:
                        self.solve_maze(maze)
                        result.append(maze)
                except ValueError as e:
                    print(e)

        return result
