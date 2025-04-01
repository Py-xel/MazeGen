from Coordinate import Coordinate
from CellType import CellType
from MazeStat import MazeStat


class Maze:
    def __init__(
        self, start: Coordinate, exit: Coordinate, layout: dict[Coordinate, CellType]
    ):
        self.id: int | None = None
        self.start = start
        self.exit = exit
        self.size = int(pow(len(layout), 0.5))
        self.layout = layout
        self.memory: dict[Coordinate, int] = {start: 1}
        self.stat = None

    def is_blockade(self, coord: Coordinate) -> bool:
        if coord in self.layout:
            return self.layout.get(coord) == CellType.Wall
        else:
            return None

    def get_memory_value(self, coord: Coordinate) -> int:
        if coord in self.memory:
            return self.memory.get(coord)
        else:
            return 0

    def update_solution_stat(self, time: float) -> None:
        self.stat.set_num_solutions(self.memory.get(self.exit))
        self.stat.set_solution_time(time)

    def set_stat(self, stat: MazeStat) -> None:
        self.stat = stat
