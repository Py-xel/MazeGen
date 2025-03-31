from Coordinate import Coordinate
from Maze import Maze
from MazeVisualizer import MazeVisualizer


def _recursive_solve_maze(
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
                _recursive_solve_maze(new_pos, maze)


def _solve_maze_linear(maze: Maze) -> None:
    for j in range(maze.size - 1):
        for i in range(maze.size):
            if j > 0 and j < maze.size - 1 and i > 0 and i < maze.size:
                current = Coordinate(maze.size - 1 - j, i)
                if maze.is_blockade(current) == False:
                    maze.memory[current] = _calculate_memory_value(current, maze)
    maze.memory[maze.exit] = maze.memory.get(maze.exit.__add__(Coordinate(1, 0)))


def _calculate_memory_value(current: Coordinate, maze: Maze) -> int:
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


def dfs_find_paths(maze, max_solutions=10000):
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
        if len(paths) >= max_solutions:  # Stop searching once we hit the solution limit
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


def solve_maze(maze: Maze):
    if maze.size < 15:
        _recursive_solve_maze(maze.start, maze)
    else:
        _solve_maze_linear(maze)

    visualizer = MazeVisualizer(maze)
    visualizer.plot_solutions()
