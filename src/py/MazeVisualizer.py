import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
from Maze import Maze
from CellType import CellType
from Coordinate import Coordinate
from LegendType import LegendType


class MazeVisualizer:
    GRID_SHIFT = 0.5
    NORMAL_FORM_THRESHOLD = 1000
    CONSOLE_COLOURS = {
        CellType.Start: "\033[34mS\033[0m",
        CellType.Exit: "\033[31mE\033[0m",
    }
    CELL_TYPE_COLOURS = {
        # WALL: purple
        CellType.Wall: [68, 1, 84],
        # PATH: yellow
        CellType.Path: [253, 231, 37],
        # START: lightblue
        CellType.Start: [35, 129, 214],
        # END: red
        CellType.Exit: [193, 59, 50],
    }
    LEGEND_LABEL_COLOURS = {
        LegendType.Start: [35 / 255, 129 / 255, 214 / 255, 1],
        LegendType.End: [193 / 255, 59 / 255, 50 / 255, 1],
        LegendType.Solution: [52 / 255, 250 / 255, 112 / 255, 1],
    }

    def __init__(self):
        pass

    def _create_maze_array_from_maze(self, maze: Maze):
        maze_array = np.zeros((maze.size, maze.size, 3), dtype=int)

        # Convert maze to color array
        for key, value in maze.layout.items():
            if value in self.CELL_TYPE_COLOURS:
                maze_array[key.x, key.y] = self.CELL_TYPE_COLOURS.get(value)

        return maze_array

    def _update_display_maze_by_solutions(self, maze_array, maze: Maze):
        solutions = maze.memory
        for key, value in solutions.items():
            if key != maze.start and key != maze.exit:
                # Adjust color based on the number of times the cell is visited
                darkened_color = self._adjust_color_based_on_visits(
                    base_color=(52, 250, 112),  # Original color: #34FA70
                    num_visits=value,
                    num_solutions=len(solutions),  # Pass number of solutions here
                )
                maze_array[key.x, key.y] = darkened_color  # Apply the darkened color

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

    def _recursive_calculate_normal_form(self, num: int, pow: int = 0):
        if 1 <= abs(num) < 10:
            return num, pow
        elif 0 <= abs(num) < 1:
            return self._recursive_calculate_normal_form(num * 10, pow - 1)
        elif num == 0:
            return 0, 0
        return self._recursive_calculate_normal_form(num / 10, pow + 1)

    def _display_cell(
        self,
        grid: dict[Coordinate, CellType],
        solution: dict[Coordinate, int],
        current: Coordinate,
    ):
        """Handles the display of individual cells with color coding."""
        if current in grid:
            cell_value = grid.get(current)
            if len(solution) > 1 and solution.get(current) != None:
                cell_value = solution.get(current)
            if cell_value in self.CONSOLE_COLOURS:
                print(self.CONSOLE_COLOURS.get(cell_value), end=" ")
            else:
                print(cell_value, end=" ")

    def plot_maze(self, maze: Maze):
        """Plots the maze and highlights the solution paths in different shades of green,
        with shared paths being darker and unique ones brighter."""
        maze_array = self._create_maze_array_from_maze(maze)
        legends = {
            LegendType.Start: self.LEGEND_LABEL_COLOURS.get(LegendType.Start),
            LegendType.End: self.LEGEND_LABEL_COLOURS.get(LegendType.End),
        }
        title = "Maze"
        if len(maze.memory) > 1:
            self._update_display_maze_by_solutions(maze_array, maze)
            legends[LegendType.Solution] = self.LEGEND_LABEL_COLOURS.get(
                LegendType.Solution
            )
            title = "Maze Solutions"

        fig, ax = plt.subplots()
        ax.imshow(maze_array)
        ax.axis("off")

        # Title and legend
        patches: list[mpatches.Patch] = list()
        for key, value in legends.items():
            patch = mpatches.Patch(color=value, label=key)
            patches.append(patch)

        plt.title(title, fontsize=14)
        plt.legend(handles=patches, bbox_to_anchor=(1.3, 1.1))

        # Display the number of visits for each cell in the center of each cell
        if len(maze.memory) > 1:
            for key, value in maze.memory.items():
                display_value = str(value)
                display_size = 10
                if value >= self.NORMAL_FORM_THRESHOLD:
                    new_value, power = self._recursive_calculate_normal_form(value)
                    display_value = f"{round(new_value,2)}E{power}"
                    display_size = 5

                if value >= 1:
                    ax.text(
                        key.y,  # x-coordinate
                        key.x,  # y-coordinate
                        display_value,  # Display the number of visits
                        ha="center",
                        va="center",  # Center the text
                        fontsize=display_size,
                        color="black",
                        weight="bold",
                    )

        # GRID LINES
        # Shift the grid by 0.5 units left and up
        # Horizontal lines (Shifted)
        for i in range(maze.size + 1):
            ax.plot(
                [0 - self.GRID_SHIFT, maze.size - self.GRID_SHIFT],
                [i - self.GRID_SHIFT, i - self.GRID_SHIFT],
                color="gray",
                linewidth=1,
                alpha=0.5,
            )

        # Vertical lines (Shifted)
        for j in range(maze.size + 1):
            ax.plot(
                [j - self.GRID_SHIFT, j - self.GRID_SHIFT],
                [0 - self.GRID_SHIFT, maze.size - self.GRID_SHIFT],
                color="gray",
                linewidth=1,
                alpha=0.5,
            )

        # Display the plot
        plt.show()

    def display_maze(self, maze: Maze):
        for x in range(maze.size):
            for y in range(maze.size):
                current = Coordinate(x, y)
                self._display_cell(maze.layout, maze.memory, current)

            print()  # Newline after each row
