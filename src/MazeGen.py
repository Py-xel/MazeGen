from collections import deque
import random
import time


class Maze:
    def __init__(self, size, scarcity):
        self.size = size
        self.scarcity = scarcity
        self.grid = [
            ["#" for _ in range(size)] for _ in range(size)
        ]  # Walls by default
        self.start = (size - 1, 1)  # Shift start cell to right by one.
        self.exit = (0, size - 2)  # Shift exit cell to left by one.
        self.visited = [[False for _ in range(size)] for _ in range(size)]
        self._generate_maze()

    def _generate_maze(self):
        """Generates the maze and ensures it is solvable."""
        while True:
            # Reset the grid and visited cells
            self.grid = [["#" for _ in range(self.size)] for _ in range(self.size)]
            self.visited = [[False for _ in range(self.size)] for _ in range(self.size)]

            # Generate the maze (marked for matplotlib)
            self._recursive_backtrack(self.start[0], self.start[1])
            self.grid[self.start[0]][self.start[1]] = "S"
            self.grid[self.exit[0]][self.exit[1]] = "E"
            self._convert_random_walls()

            # Check if the maze is solvable with only right or up movements
            if self._is_solvable():
                break  # Exit if solvable
            print("Maze is unsolvable, regenerating...")

    def _recursive_backtrack(self, x, y):
        """Carve a path recursively with backtracking."""
        self.visited[x][y] = True
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        random.shuffle(directions)  # Randomize directions for maze randomness

        for dx, dy in directions:
            nx, ny = x + dx * 2, y + dy * 2  # Move two cells in that direction

            # Check if the next cell is within bounds and unvisited
            if (
                0 < nx < self.size - 1
                and 0 < ny < self.size - 1
                and not self.visited[nx][ny]
            ):
                # Carve a path to the next cell
                self.grid[nx][ny] = "."
                self.grid[x + dx][
                    y + dy
                ] = "."  # Carve between the current and next cell
                self._recursive_backtrack(nx, ny)  # Recursively visit the next cell

    def _convert_random_walls(self):
        """Randomly adds walls to the maze based on scarcity."""
        for i in range(1, self.size - 1):  # Avoid outer walls
            for j in range(1, self.size - 1):  # Avoid outer walls
                if (i, j) == self.start or (i, j) == self.exit:
                    continue
                if self.grid[i][j] == "#" and random.random() < self.scarcity:
                    self.grid[i][j] = "."  # Change to path if within scarcity range

    def _is_solvable(self):
        """Checks if there is a path from start to exit using Breadth-First Search (BFS)."""
        start_x, start_y = self.start
        exit_x, exit_y = self.exit

        # BFS setup
        queue = deque([(start_x, start_y)])
        self.visited = [
            [False for _ in range(self.size)] for _ in range(self.size)
        ]  # Reset visited array
        self.visited[start_x][start_y] = True

        while queue:
            x, y = queue.popleft()

            if (x, y) == (exit_x, exit_y):
                return True

            # Check neighbours up and right
            for dx, dy in [(-1, 0), (0, 1)]:
                nx, ny = x + dx, y + dy
                if (
                    0 <= nx < self.size
                    and 0 <= ny < self.size
                    and not self.visited[nx][ny]
                    and self.grid[nx][ny] != "#"
                ):
                    queue.append((nx, ny))
                    self.visited[nx][ny] = True

        return False

    def generate(self):
        start_time = time.time()
        self._generate_maze()
        end_time = time.time()
        build_time = round((end_time - start_time) * 1000, 2)  # Convert to milliseconds
        return build_time

    def display_maze(self):
        for x in range(self.size):
            for y in range(self.size):
                self._display_cell(x, y)
            print()  # Newline after each row

    def _display_cell(self, x, y):
        """Handles the display of individual cells with color coding."""
        if (x, y) == self.start:
            print("\033[34mS\033[0m", end=" ")  # START: blue 'S'
        elif (x, y) == self.exit:
            print("\033[31mE\033[0m", end=" ")  # END: red 'E'
        else:
            print(self.grid[x][y], end=" ")  # PATH: '.' or WALL: '#'
