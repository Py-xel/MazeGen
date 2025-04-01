from collections.abc import Callable
import time
import os
import sys
from MazeController import MazeController
from ValidationResult import ValidationResult
from MazeVisualizer import MazeVisualizer
from Maze import Maze


class Menu:
    def __init__(self):
        self.controller = MazeController()
        self.visualizer = MazeVisualizer()

    def _get_input(self, question: str, validator: Callable[[str], ValidationResult]):
        while True:
            answer = input(question)
            result = validator(answer)
            if result.valid:
                return result.value
            else:
                print(result.error_msg)

    def _maze_size_validator(self, value: str) -> ValidationResult:
        try:
            validated = int(value)
            # Due to the walls, no maze under 2x2 can be generated.
            if validated >= 2:
                return ValidationResult(True, value=validated)
            else:
                return ValidationResult(
                    False, error_msg="Please enter a positive integer larger than 1."
                )
        except ValueError:
            return ValidationResult(
                False, error_msg="Invalid input. Please enter a number."
            )

    def _scarcity_validator(self, value: str) -> ValidationResult:
        try:
            validated = float(value)
            if 0.1 <= validated <= 0.9:
                return ValidationResult(True, value=validated)
            else:
                return ValidationResult(
                    False, error_msg="Please enter a value between 0.1 and 0.9!"
                )
        except ValueError:
            return ValidationResult(
                False,
                error_msg="Invalid input. Please enter a number between 0.1 and 0.9!",
            )

    def _yes_no_validator(self, value: str) -> ValidationResult:
        lower_value = value.lower()
        if lower_value == "y":
            return ValidationResult(True, value=True)
        elif lower_value == "n":
            return ValidationResult(True, value=False)
        else:
            return ValidationResult(False, error_msg="Please enter either 'n' or 'y'!")

    def _display_maze(self, maze: Maze, build_time, scarcity):
        """Clears the console and visualizes the maze."""
        # Clear console
        self._clear_console()

        time.sleep(0.2)  # Small delay to ensure clean slate

        # Format the stats
        maze_size_str = f"[ {maze.size} x {maze.size} ]"
        scarcity_str = f"Scarcity: {int(scarcity * 100)}%"
        build_time_str = f"Build time: {build_time}ms"

        # Calculate the total length of the stats line (including spaces)
        stats_line = f"{maze_size_str}     {scarcity_str}     {build_time_str}"
        total_length = len(stats_line)

        """ FORMATTED DISPLAY """
        print("-" * total_length)
        print(stats_line)
        print("\n")
        self.visualizer.display_maze(maze)
        print("\n")
        print("-" * total_length)

    def _get_maze_size(self) -> int:
        question = "Enter maze size (n): "
        answer = self._get_input(question, self._maze_size_validator)
        # We add 2 because the permanent walls reduce the maze's true size.
        return int(answer) + 2

    def _get_scarcity(self) -> float:
        question = "Enter scarcity of walls (0.1 - 0.9): "
        return self._get_input(question, self._scarcity_validator)

    def _plot_maze(self) -> bool:
        question = "Would you like to better visualize the maze? [y/n]: "
        return self._get_input(question, self._yes_no_validator)

    def _solve_maze(self) -> bool:
        question = "Would you like to solve the maze? [y/n]: "
        return self._get_input(question, self._yes_no_validator)

    def _clear_console(self):
        """Clears the console window."""
        if sys.platform == "win32":
            os.system("cls")  # Windows
        else:
            print("\033[H\033[3J", end="")  # Unix-based

    def run(self) -> None:
        maze_size = self._get_maze_size()
        scarcity = self._get_scarcity()

        start_time = time.time()
        maze = self.controller.create_maze(maze_size, scarcity)
        end_time = time.time()
        build_time = round((end_time - start_time) * 1000, 2)  # Convert to milliseconds
        self._display_maze(maze, build_time, scarcity)

        if self._plot_maze():
            self.visualizer.plot_maze(maze)

        if self._solve_maze():
            self.controller.solve_maze(maze)
            self.visualizer.plot_maze(maze)
