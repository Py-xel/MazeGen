from Coordinate import Coordinate
from CellType import CellType


class Maze:
    def __init__(
        self, start: Coordinate, exit: Coordinate, layout: dict[Coordinate, CellType]
    ):
        self.start = start
        self.exit = exit
        self.size = int(pow(len(layout), 0.5))
        self.layout = layout
        self.memory: dict[Coordinate, int] = {start: 1}
        pass

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
