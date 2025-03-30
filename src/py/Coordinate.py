class Coordinate:

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __add__(self, other) -> any:
        if not isinstance(other, Coordinate):
            return NotImplemented
        return Coordinate(self.x + other.x, self.y + other.y)

    def __eq__(self, other) -> bool:
        if isinstance(other, Coordinate):
            return other.x == self.x and other.y == self.y
        return False

    def __hash__(self):
        return hash(7 * self.x * self.y)

    def __str__(self) -> str:
        return "({},{})".format(self.x, self.y)
