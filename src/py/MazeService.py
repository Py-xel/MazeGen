from collections import (
    deque,
)  # Double ended queue for better stack managing | https://www.geeksforgeeks.org/deque-in-python/
from Maze import Maze
from Coordinate import Coordinate
from CellType import CellType
from MazeRepository import MazeRepository
import random
import sys

sys.setrecursionlimit(10_000)  # Increase recursion limit


class MazeService:
    def __init__(self):
        self.repo = MazeRepository()
        pass

    def _generate_maze(self, size: int, scarcity: float):
        """Generates the maze and ensures it is solvable."""
        while True:
            # Reset the grid and visited cells
            grid = [["#" for _ in range(size)] for _ in range(size)]
            visited = [[False for _ in range(size)] for _ in range(size)]
            start = (size - 1, 1)  # Shift start cell to right by one.
            exit = (0, size - 2)  # Shift exit cell to left by one.

            # Generate the maze (marked for matplotlib)
            self._recursive_backtrack(grid, visited, size, start[0], start[1])
            grid[start[0]][start[1]] = "S"
            grid[exit[0]][exit[1]] = "E"
            self._convert_random_walls(grid, scarcity)

            # Check if the maze is solvable with only right or up movements
            if self._is_solvable(start, exit, grid):
                break  # Exit if solvable
            print("Maze is unsolvable, regenerating...")
        return grid

    def _recursive_backtrack(self, grid, visited, size, x, y):
        """Carve a path recursively with backtracking."""
        visited[x][y] = True
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        random.shuffle(directions)  # Randomize directions for maze randomness

        for dx, dy in directions:
            nx, ny = x + dx * 2, y + dy * 2  # Move two cells in that direction

            # Check if the next cell is within bounds and unvisited
            if 0 < nx < size - 1 and 0 < ny < size - 1 and not visited[nx][ny]:
                # Carve a path to the next cell
                grid[nx][ny] = "."
                grid[x + dx][y + dy] = "."  # Carve between the current and next cell
                self._recursive_backtrack(
                    grid, visited, size, nx, ny
                )  # Recursively visit the next cell

    def _convert_random_walls(self, grid, scarcity):
        """Randomly adds walls to the maze based on scarcity."""
        size = len(grid[0])
        for i in range(1, size - 1):  # Avoid outer walls
            for j in range(1, size - 1):  # Avoid outer walls
                if grid[i][j] == "#" and random.random() < scarcity:
                    grid[i][j] = "."  # Change to path if within scarcity range

    def _is_solvable(self, start, exit, grid):
        """Checks if there is a path from start to exit using Breadth-First Search (BFS)."""
        start_x, start_y = start
        exit_x, exit_y = exit
        size = len(grid[0])
        # BFS setup
        queue = deque([(start_x, start_y)])
        visited = [
            [False for _ in range(size)] for _ in range(size)
        ]  # Reset visited array
        visited[start_x][start_y] = True

        while queue:
            x, y = queue.popleft()

            if (x, y) == (exit_x, exit_y):
                return True

            # Check neighbours up and right
            for dx, dy in [(-1, 0), (0, 1)]:
                nx, ny = x + dx, y + dy
                if (
                    0 <= nx < size
                    and 0 <= ny < size
                    and not visited[nx][ny]
                    and grid[nx][ny] != "#"
                ):
                    queue.append((nx, ny))
                    visited[nx][ny] = True

        return False

    def _recursive_solve_maze(
        self,
        current_pos: Coordinate,
        maze: Maze,
    ) -> None:
        movement_vectors: set[Coordinate] = {Coordinate(-1, 0), Coordinate(0, 1)}
        for movement in movement_vectors:
            new_pos: Coordinate = current_pos.__add__(movement)
            if maze.is_blockade(new_pos) == False:
                if new_pos in maze.memory:
                    new_value: int = maze.memory.get(new_pos) + 1
                    maze.memory[new_pos] = new_value
                else:
                    maze.memory[new_pos] = maze.memory.get(current_pos)
                if new_pos != maze.exit:
                    self._recursive_solve_maze(new_pos, maze)

    def _solve_maze_linear(self, maze: Maze) -> None:
        for j in range(maze.size - 1):
            for i in range(maze.size):
                if j > 0 and j < maze.size - 1 and i > 0 and i < maze.size:
                    current = Coordinate(maze.size - 1 - j, i)
                    if maze.is_blockade(current) == False:
                        maze.memory[current] = self._calculate_memory_value(
                            current, maze
                        )
        maze.memory[maze.exit] = maze.memory.get(maze.exit.__add__(Coordinate(1, 0)))

    def _calculate_memory_value(self, current: Coordinate, maze: Maze) -> int:
        left_neighbour = current.__add__(Coordinate(0, -1))
        down_neighbour = current.__add__(Coordinate(1, 0))
        left_value = maze.get_memory_value(left_neighbour)
        down_value = maze.get_memory_value(down_neighbour)
        if (
            maze.is_blockade(left_neighbour) == False
            and maze.is_blockade(down_neighbour) == False
        ):
            return left_value + down_value
        elif maze.is_blockade(down_neighbour) == False:
            return down_value
        elif maze.is_blockade(left_neighbour) == False:
            return left_value
        else:
            return 0

    def _get_start_pos(self, grid) -> tuple:
        size = len(grid[0])
        return (size - 1, 1)

    def _get_exit_pos(self, grid) -> tuple:
        size = len(grid[0])
        return (0, size - 2)

    def _create_maze_from_grid(self, grid) -> Maze:
        size = len(grid[0])
        start_pos = self._get_start_pos(grid)
        exit_pos = self._get_exit_pos(grid)
        start = Coordinate(start_pos[0], start_pos[1])
        exit = Coordinate(exit_pos[0], exit_pos[1])
        layout: dict[Coordinate, CellType] = {
            start: CellType.Start,
            exit: CellType.Exit,
        }
        for i in range(size):
            for j in range(size):
                current_coord = Coordinate(i, j)
                if grid[i][j] == "#":
                    layout[current_coord] = CellType.Wall
                elif grid[i][j] == ".":
                    layout[current_coord] = CellType.Path

        return Maze(start, exit, layout)

    def dfs_find_paths(self, maze, max_solutions=10000):
        """Uses DFS (Depth-First Search) to find paths from start to exit, moving only UP or RIGHT.
        Limits the number of solutions to max_solutions."""
        size = maze.size
        start = maze.start
        exit = maze.exit

        paths = []
        visited = [
            [False for _ in range(size)] for _ in range(size)
        ]  # Visited cells for all paths

        def dfs(x, y, path):
            """Recursive DFS function to explore the maze."""
            if (
                len(paths) >= max_solutions
            ):  # Stop searching once we hit the solution limit
                return

            if (x, y) == exit:
                paths.append(path[:])  # Add the found path to the solutions
                return

            # Mark the current cell as visited
            visited[x][y] = True
            path.append((x, y))

            # Explore possible movements (Up, Right)
            for dx, dy in [(-1, 0), (0, 1)]:  # Only UP or RIGHT
                nx, ny = x + dx, y + dy
                if (
                    0 <= nx < size
                    and 0 <= ny < size
                    and not visited[nx][ny]
                    and maze.grid[nx][ny] != "#"
                ):
                    dfs(nx, ny, path)

            # Backtrack
            path.pop()
            visited[x][y] = False

        # Start DFS from the start cell
        dfs(start[0], start[1], [])

        return paths

    def generate(self, size: int, scarcity: float) -> Maze:
        grid = self._generate_maze(size, scarcity)

        return self._create_maze_from_grid(grid)

    def solve_maze(self, maze: Maze):
        if maze.size < 15:
            self._recursive_solve_maze(maze.start, maze)
        else:
            self._solve_maze_linear(maze)
        return maze

    def save_or_update_maze(self, maze: Maze) -> Maze:
        return self.repo.save_or_update_maze(maze)

    def get_all_mazes(self) -> list[Maze]:
        return self.repo.get_all_mazes()

    def get_maze_by_id(self, id: int) -> Maze:
        return self.repo.get_maze(id)
