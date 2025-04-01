import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
from MazeData import MazeData
from MazeService import MazeService
from Maze import Maze
from CellType import CellType
from Coordinate import Coordinate


class MazeController:
    GRID_SHIFT = 0.5
    NORMAL_FORM_THRESHOLD = 1000
    CONSOLE_COLOURS = {
        CellType.Start: "\033[34mS\033[0m",
        CellType.Exit: "\033[31mE\033[0m",
    }

    def __init__(self):
        self.service = MazeService()
        pass

    def _recursive_calculate_normal_form(self, num: int, pow: int = 0):
        if 1 <= abs(num) < 10:
            return num, pow
        elif 0 <= abs(num) < 1:
            return self._recursive_calculate_normal_form(num * 10, pow - 1)
        elif num == 0:
            return 0, 0
        return self._recursive_calculate_normal_form(num / 10, pow + 1)

    def _display_cell(self, grid: dict[Coordinate, CellType], current: Coordinate):
        """Handles the display of individual cells with color coding."""
        if current in grid:
            cell_value = grid.get(current)
            if cell_value in self.CONSOLE_COLOURS:
                print(self.CONSOLE_COLOURS.get(cell_value), end=" ")
            else:
                print(cell_value, end=" ")

    def plot_maze(self, data: MazeData):
        """Plots the maze and highlights the solution paths in different shades of green,
        with shared paths being darker and unique ones brighter."""

        fig, ax = plt.subplots()
        ax.imshow(data.maze_array)
        ax.axis("off")

        # Title and legend
        patches: list[mpatches.Patch] = list()
        for key, value in data.legends.items():
            patch = mpatches.Patch(color=value, label=key)
            patches.append(patch)

        plt.title(data.title, fontsize=14)
        plt.legend(handles=patches, bbox_to_anchor=(1.3, 1.1))

        # Display the number of visits for each cell in the center of each cell
        if data.solutions != None:
            for key, value in data.solutions.items():
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
        for i in range(data.size + 1):
            ax.plot(
                [0 - self.GRID_SHIFT, data.size - self.GRID_SHIFT],
                [i - self.GRID_SHIFT, i - self.GRID_SHIFT],
                color="gray",
                linewidth=1,
                alpha=0.5,
            )

        # Vertical lines (Shifted)
        for j in range(data.size + 1):
            ax.plot(
                [j - self.GRID_SHIFT, j - self.GRID_SHIFT],
                [0 - self.GRID_SHIFT, data.size - self.GRID_SHIFT],
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
                self._display_cell(maze.layout, current)
            print()  # Newline after each row

    def create_maze(self, size, scarcity) -> Maze:
        return self.service.generate(size, scarcity)

    def solve_maze(self, maze) -> None:
        self.service.solve_maze(maze)
