import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches


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


def adjust_color_based_on_visits(base_color, num_visits, max_visits, num_solutions):
    """Darkens the color based on the number of visits, with a consistent gradient scaling."""

    # If there is only one solution, return the original base color
    if num_solutions == 1:
        return base_color

    # Convert the base color to array
    base_rgb = np.array(base_color)

    # Normalize the number of visits to a range between 0 and 1
    normalized_visits = num_visits / max_visits

    darken_factor = normalized_visits * 255  # Scale between RGB values of 0 and 255

    # Darken the color by subtracting the darken_factor from each RGB component
    darkened_rgb = np.maximum(
        base_rgb - darken_factor, 0
    )  # Ensure no value goes below 0
    darkened_rgb = np.minimum(darkened_rgb, 255)  # Ensure no value goes above 255

    # Set a minimum so the darkest spots aren't pitch black.
    min_threshold = np.array([0, 100, 0])

    # Ensure the darkened color does not go below the minimum threshold
    darkened_rgb = np.maximum(darkened_rgb, min_threshold)

    return darkened_rgb


def plot_solutions(maze, solutions):
    """Plots the maze and highlights the solution paths in different shades of green,
    with shared paths being darker and unique ones brighter."""
    size = maze.size
    grid = maze.grid
    maze_array = np.zeros((size, size, 3), dtype=int)

    # Count the number of times each cell appears in any of the solutions
    cell_counts = np.zeros((size, size), dtype=int)
    for solution in solutions:
        for x, y in solution:
            if (x, y) != maze.start and (x, y) != maze.exit:
                cell_counts[x, y] += 1

    # Convert maze to color array
    for i in range(size):
        for j in range(size):
            if grid[i][j] == "#":
                maze_array[i, j] = [68, 1, 84]  # WALL: purple
            elif grid[i][j] == ".":
                maze_array[i, j] = [253, 231, 37]  # PATH: yellow
            elif grid[i][j] == "S":
                maze_array[i, j] = [35, 129, 214]  # START: lightblue
            elif grid[i][j] == "E":
                maze_array[i, j] = [193, 59, 50]  # END: red

    # Highlight all solution paths with adjusted colors based on visits
    num_solutions = len(solutions)
    for i, solution in enumerate(solutions):
        for x, y in solution:
            if (x, y) != maze.start and (x, y) != maze.exit:
                # Adjust color based on the number of times the cell is visited
                darkened_color = adjust_color_based_on_visits(
                    base_color=(52, 250, 112),  # Original color: #34FA70
                    num_visits=cell_counts[x, y],
                    max_visits=num_solutions,
                    num_solutions=num_solutions,  # Pass number of solutions here
                )
                maze_array[x, y] = darkened_color  # Apply the darkened color

    fig, ax = plt.subplots()
    ax.imshow(maze_array)
    ax.axis("off")

    # Title and legend
    plt.title("Maze Solutions", fontsize=14)
    start_patch = mpatches.Patch(
        color=[35 / 255, 129 / 255, 214 / 255, 1], label="Start"
    )
    exit_patch = mpatches.Patch(color=[193 / 255, 59 / 255, 50 / 255, 1], label="Exit")
    solution_patch = mpatches.Patch(
        color=[52 / 255, 250 / 255, 112 / 255, 1], label="Solution Path"
    )  # Updated color
    plt.legend(
        handles=[start_patch, exit_patch, solution_patch], bbox_to_anchor=(1.3, 1.1)
    )

    # Display the number of visits for each cell in the center of each cell
    for i in range(size):
        for j in range(size):
            if cell_counts[i, j] >= 1:  # Display number on visits on visited cells.
                ax.text(
                    j,  # x-coordinate
                    i,  # y-coordinate
                    str(cell_counts[i, j]),  # Display the number of visits
                    ha="center",
                    va="center",  # Center the text
                    fontsize=10,
                    color="black",
                    weight="bold",
                )

    # GRID LINES
    # Shift the grid by 0.5 units left and up
    shift = 0.5

    # Horizontal lines (Shifted)
    for i in range(size + 1):
        ax.plot(
            [0 - shift, size - shift],
            [i - shift, i - shift],
            color="gray",
            linewidth=1,
            alpha=0.5,
        )

    # Vertical lines (Shifted)
    for j in range(size + 1):
        ax.plot(
            [j - shift, j - shift],
            [0 - shift, size - shift],
            color="gray",
            linewidth=1,
            alpha=0.5,
        )

    # Display the plot
    plt.show()


def solve_maze(maze):
    """Solves the maze using DFS and visualizes all unique paths."""
    solutions = dfs_find_paths(maze)
    if solutions:
        print(f"Found {len(solutions)} solution(s)!")

        if len(solutions) == 10000:
            print(
                f"\033[1m" + "Maximum number of solutions of 10000 exceeded!"
            )  # \033[1m = BOLD

        plot_solutions(maze, solutions)
    else:
        print("No solution found.")
