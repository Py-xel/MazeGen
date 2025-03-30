from enum import StrEnum


class CellType(StrEnum):
    Start = "S"
    Exit = "E"
    Wall = "#"
    Path = "."
