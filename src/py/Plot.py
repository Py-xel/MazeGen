import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches


def _plot(maze):
    size = maze.size
    grid = maze.grid

    # Convert maze to array
    maze_array = np.zeros((size, size, 3), dtype=int)

    # Map the characters to colors
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

    fig, ax = plt.subplots()

    # Plot the maze image
    ax.imshow(maze_array)
    ax.axis("off")

    # TITLE
    plt.title("Maze", fontsize=14)

    # LEGEND
    lightblue_patch = mpatches.Patch(
        color=[35 / 255, 129 / 255, 214 / 255, 1], label="Start"
    )
    red_patch = mpatches.Patch(color=[193 / 255, 59 / 255, 50 / 255, 1], label="Exit")
    plt.legend(handles=[lightblue_patch, red_patch], bbox_to_anchor=(1.3, 1.1))

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
    canvas = fig.canvas
    canvas.manager.window.title("Maze")
    plt.show()
