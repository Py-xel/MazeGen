from Menu import Menu
from MazeController import MazeController
from MazeDataService import MazeDataService
import time


def main():
    menu = Menu()
    data_service = MazeDataService()

    """ MAZE """
    maze_size, scarcity = menu.get_maze_params()
    # maze = MazeGen(maze_size, scarcity)
    # build_time = maze.generate()
    controller = MazeController()
    maze = controller.create_maze(maze_size, scarcity)
    controller.display_maze(maze)
    # menu.visualize_maze(maze, build_time)

    """ PLOT """
    to_plot = menu.plot_maze()
    if to_plot == "y":
        data = data_service.create_maze_data(maze)
        controller.plot_maze(data)

    """ SOLVE """
    to_solve = menu.solve_maze()
    if to_solve == "y":
        controller.solve_maze(maze)
        data = data_service.create_maze_data(maze)
        controller.plot_maze(data)


if __name__ == "__main__":
    main()
