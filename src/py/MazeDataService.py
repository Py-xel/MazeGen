from Maze import Maze
from CellType import CellType
from MazeData import MazeData
from LegendType import LegendType
import numpy as np


class MazeDataService:
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

    def create_maze_data(self, maze: Maze) -> MazeData:
        maze_array = self._create_maze_array_from_maze(maze)
        solutions = None
        legends = {
            LegendType.Start: self.LEGEND_LABEL_COLOURS.get(LegendType.Start),
            LegendType.End: self.LEGEND_LABEL_COLOURS.get(LegendType.End),
        }
        if len(maze.memory) > 1:
            self._update_display_maze_by_solutions(maze_array, maze)
            legends[LegendType.Solution] = self.LEGEND_LABEL_COLOURS.get(LegendType.Solution)
            solutions = maze.memory

        return MazeData(maze.size,maze_array,legends,solutions)
