from Menu import Menu
from MazeGen import Maze
from Plot import _plot
import time


def main():
    menu = Menu()

    """ MAZE """
    maze_size, scarcity = menu.get_maze_params()
    maze = Maze(maze_size, scarcity)
    build_time = maze.generate()
    menu.visualize_maze(maze, build_time)

    """ PLOT """
    to_plot = menu.plot_maze()
    if to_plot == "y":
        _plot(maze)


if __name__ == "__main__":
    main()
