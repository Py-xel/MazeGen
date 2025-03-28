import time
import os
import sys


class Menu:
    def __init__(self):
        self.maze_size = self.get_maze_size()
        self.scarcity = self.set_wall_scarcity()

    def get_maze_size(self):
        while True:
            try:
                size = int(input("Enter maze size (n): "))
                if size > 0:
                    return size
                else:
                    print("Please enter a positive integer.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def set_wall_scarcity(self):
        while True:
            try:
                scarcity = float(input("Enter scarcity of walls (0.1 - 0.9): "))
                if 0.1 <= scarcity <= 0.9:
                    return scarcity
                else:
                    print("Please enter a value between 0.1 and 0.9!")
            except ValueError:
                print("Invalid input. Please enter a number between 0.1 and 0.9!")

    def plot_maze(self):
        while True:
            try:
                to_plot_str = input(
                    "Would you like to better visualize the maze? [y/n]: "
                )
                if to_plot_str == "y":
                    return "y"
                elif to_plot_str == "n":
                    return "n"
                else:
                    print("Please enter either 'n' or 'y'!")
            except ValueError:
                print("Invalid input. Please enter either 'n' or 'y'!")

    def get_maze_params(self):
        return self.maze_size, self.scarcity

    def clear_console(self):
        """Clears the console window."""
        if sys.platform == "win32":
            os.system("cls")  # Windows
        else:
            print("\033[H\033[3J", end="")  # Unix-based

    def solve_maze(self):
        while True:
            try:
                to_plot_str = input("Would you like to solve the maze? [y/n]: ")
                if to_plot_str == "y":
                    return "y"
                elif to_plot_str == "n":
                    return "n"
                else:
                    print("Please enter either 'n' or 'y'!")
            except ValueError:
                print("Invalid input. Please enter either 'n' or 'y'!")

    def visualize_maze(self, maze, build_time):
        """Clears the console and visualizes the maze."""
        # Clear console
        self.clear_console()

        time.sleep(0.2)  # Small delay to ensure clean slate

        # Format the stats
        maze_size_str = f"[ {maze.size} x {maze.size} ]"
        scarcity_str = f"Scarcity: {int(self.scarcity * 100)}%"
        build_time_str = f"Build time: {build_time}ms"

        # Calculate the total length of the stats line (including spaces)
        stats_line = f"{maze_size_str}     {scarcity_str}     {build_time_str}"
        total_length = len(stats_line)

        """ FORMATTED DISPLAY """
        print("-" * total_length)
        print(stats_line)
        print("\n")
        maze.display_maze()
        print("\n")
        print("-" * total_length)
