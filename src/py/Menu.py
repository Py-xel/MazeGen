from collections.abc import Callable
import time
import os
import sys
from MazeController import MazeController
from ValidationResult import ValidationResult
from MazeVisualizer import MazeVisualizer
from MazeStatVisualizer import MazeStatVisualizer
from Maze import Maze
from MazeStat import MazeStat
from FileReader import FileReader


class Menu:
    PATH = "../../src/data/random_mazes.csv"

    def __init__(self):
        self.controller = MazeController()
        self.visualizer = MazeVisualizer()
        self.stat_visualizer = MazeStatVisualizer()
        self.file_reader = FileReader()
        self.selections = {
            1: ["[1] Create a new maze", self._create_and_solve_selection],
            2: ["[2] Import from file", self._import_maze_selection],
            3: ["[3] Show a specific maze", self._display_maze_selection],
            4: ["[4] Show stats of mazes", self._display_maze_stats_selection],
            5: ["[5] Delete maze by id", self._delete_maze_selection],
            6: ["[6] Exit", self._exit],
        }

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

    def _int_validator(self, value: str) -> ValidationResult:
        try:
            validated = int(value)
            return ValidationResult(True, value=validated)
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

    def _display_maze(self, maze: Maze):
        """Clears the console and visualizes the maze."""
        # Clear console
        self._clear_console()

        time.sleep(0.2)  # Small delay to ensure clean slate

        stat = maze.stat
        # Format the stats
        maze_size_str = f"[ {maze.size} x {maze.size} ]"
        scarcity_str = f"Scarcity: {int(stat.scarcity * 100)}%"
        build_time_str = f"Build time: {stat.build_time}ms"
        solution_time_str = f"Solution time: {stat.solution_time}ms"
        num_of_solutions_str = f"Number of solutions: {stat.num_solutions}"

        # Calculate the total length of the stats line (including spaces)
        stats_line = f"{maze_size_str}     {scarcity_str}     {build_time_str}"
        if stat.solution_time != None:
            stats_line += f"     {solution_time_str}     {num_of_solutions_str}"
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

    def _is_plot_maze(self) -> bool:
        question = "Would you like to better visualize the maze? [y/n]: "
        return self._get_input(question, self._yes_no_validator)

    def _is_solve_maze(self) -> bool:
        question = "Would you like to solve the maze? [y/n]: "
        return self._get_input(question, self._yes_no_validator)

    def _clear_console(self):
        """Clears the console window."""
        if sys.platform == "win32":
            os.system("cls")  # Windows
        else:
            print("\033[H\033[3J", end="")  # Unix-based

    def _create_maze(self) -> Maze:
        maze_size = self._get_maze_size()
        scarcity = self._get_scarcity()

        maze = self.controller.create_maze(maze_size, scarcity)

        return maze

    def _show_maze(self, maze: Maze) -> None:
        self._display_maze(maze)
        if self._is_plot_maze():
            self.visualizer.plot_maze(maze)

    def _solve_maze(self, maze: Maze) -> None:
        if self._is_solve_maze():
            self.controller.solve_maze(maze)

    def _display_mazes(self, mazes: list[Maze]) -> None:
        """Clears the console and visualizes the maze."""
        # Clear console
        self._clear_console()
        time.sleep(0.2)  # Small delay to ensure clean slate
        for maze in mazes:
            stat = maze.stat
            # Format the stats
            id_str = f"ID: {maze.id}"
            maze_size_str = f"[ {maze.size} x {maze.size} ]"
            scarcity_str = f"Scarcity: {int(stat.scarcity * 100)}%"
            build_time_str = f"Build time: {stat.build_time}ms"
            solution_time_str = f"Solution time: {stat.solution_time}ms"
            num_of_solutions_str = f"Number of solutions: {stat.num_solutions}"

            # Calculate the total length of the stats line (including spaces)
            stats_line = (
                f"{id_str}    {maze_size_str}     {scarcity_str}     {build_time_str}"
            )
            if stat.solution_time != None:
                stats_line += f"     {solution_time_str}     {num_of_solutions_str}"
            """ FORMATTED DISPLAY """
            print(stats_line)
        print(f"Number of mazes: {len(mazes)}")

    def _load_from_file(self) -> list[Maze]:
        df = self.file_reader.read_from_csv(self.PATH)
        mazes = self.controller.import_mazes(df)
        self._display_mazes(mazes)
        return mazes

    def _select_maze_by_id(self) -> int:
        question = "Which maze would you like to see?: "
        return self._get_input(question, self._int_validator)

    def _delete_maze_by_id(self) -> int:
        question = "Which maze would you like to remove?: "
        return self._get_input(question, self._int_validator)

    def _display_maze_stats_selection(self) -> None:
        mazes = self.controller.find_all_mazes()
        stats: list[MazeStat] = list()
        for maze in mazes:
            if maze.stat is not None:
                stats.append(maze.stat)

        self.stat_visualizer.plot(stats)

    def _display_maze_selection(self) -> None:
        mazes = self.controller.find_all_mazes()
        self._display_mazes(mazes)
        id = self._select_maze_by_id()
        if 0 <= id <= len(mazes):
            maze = self.controller.find_maze_by_id(id)
            if maze is not None:
                self._show_maze(maze)

    def _import_maze_selection(self) -> None:
        mazes = self._load_from_file()
        id = self._select_maze_by_id()
        if 0 <= id <= len(mazes):
            maze = self.controller.find_maze_by_id(id)
            if maze is not None:
                self._show_maze(maze)

    def _create_and_solve_selection(self) -> None:
        maze = self._create_maze()
        self._show_maze(maze)
        self._solve_maze(maze)
        self._show_maze(maze)

    def _delete_maze_selection(self) -> None:
        mazes = self.controller.find_all_mazes()
        self._display_mazes(mazes)
        id = self._delete_maze_by_id()
        if 0 <= id <= len(mazes):
            maze = self.controller.remove_maze_by_id(id)
            if maze is not None:
                self._show_maze(maze)

    def _exit(self) -> None:
        exit

    def run(self) -> None:
        while True:
            self._clear_console()
            for value in self.selections.values():
                print(f"{value[0]}")

            print("-" * 30)  # Dashed line separator
            print("")  # Empty line after menu

            answer = int(input())
            if answer in self.selections:
                self.selections.get(answer)[1]()
            if answer == 6:
                break
        exit
