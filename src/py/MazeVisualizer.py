import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
from Maze import Maze
from CellType import CellType


class MazeVisualizer:
    def __init__(self, maze: Maze):
        self.maze = maze
        pass

    def _adjust_color_based_on_visits(self, base_color, num_visits, num_solutions):
        """Darkens the color based on the number of visits, with a consistent gradient scaling."""

        # If there is only one solution, return the original base color
        if num_solutions == 1:
            return base_color

        # Convert the base color to array
        base_rgb = np.array(base_color)

        # Normalize the number of visits to a range between 0 and 1
        normalized_visits = num_visits / num_solutions

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

    def plot_solutions(self):
        """Plots the maze and highlights the solution paths in different shades of green,
        with shared paths being darker and unique ones brighter."""
        size = self.maze.size
        solutions = self.maze.memory
        maze_array = np.zeros((size, size, 3), dtype=int)

        # Convert maze to color array
        for key, value in self.maze.layout.items():
            i = key.x
            j = key.y
            if value == CellType.Wall:
                maze_array[i, j] = [68, 1, 84]  # WALL: purple
            elif value == CellType.Path:
                maze_array[i, j] = [253, 231, 37]  # PATH: yellow
            elif value == CellType.Start:
                maze_array[i, j] = [35, 129, 214]  # START: lightblue
            elif value == CellType.Exit:
                maze_array[i, j] = [193, 59, 50]  # END: red

        # Highlight all solution paths with adjusted colors based on visits
        num_solutions = len(solutions)
        for key, value in solutions.items():
            if key != self.maze.start and key != self.maze.exit:
                # Adjust color based on the number of times the cell is visited
                darkened_color = self._adjust_color_based_on_visits(
                    base_color=(52, 250, 112),  # Original color: #34FA70
                    num_visits=value,
                    num_solutions=num_solutions,  # Pass number of solutions here
                )
                maze_array[key.x, key.y] = darkened_color  # Apply the darkened color

        fig, ax = plt.subplots()
        ax.imshow(maze_array)
        ax.axis("off")

        # Title and legend
        plt.title("Maze Solutions", fontsize=14)
        start_patch = mpatches.Patch(
            color=[35 / 255, 129 / 255, 214 / 255, 1], label="Start"
        )
        exit_patch = mpatches.Patch(
            color=[193 / 255, 59 / 255, 50 / 255, 1], label="Exit"
        )
        solution_patch = mpatches.Patch(
            color=[52 / 255, 250 / 255, 112 / 255, 1], label="Solution Path"
        )  # Updated color
        plt.legend(
            handles=[start_patch, exit_patch, solution_patch], bbox_to_anchor=(1.3, 1.1)
        )

        # Display the number of visits for each cell in the center of each cell
        for key, value in solutions.items():
            if value >= 1:
                ax.text(
                    key.y,  # x-coordinate
                    key.x,  # y-coordinate
                    str(value),  # Display the number of visits
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
