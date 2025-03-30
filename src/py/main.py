from Menu import Menu
from MazeGen import MazeGen
from Plot import _plot
from Solver import solve_maze
import time


def main():
    menu = Menu()

    """ MAZE """
    maze_size, scarcity = menu.get_maze_params()
    maze = MazeGen(maze_size, scarcity)
    build_time = maze.generate()
    menu.visualize_maze(maze, build_time)

    """ PLOT """
    to_plot = menu.plot_maze()
    if to_plot == "y":
        _plot(maze)

    """ SOLVE """
    to_solve = menu.solve_maze()
    if to_solve == "y":
        solve_maze(maze.get_maze())


if __name__ == "__main__":
    main()
