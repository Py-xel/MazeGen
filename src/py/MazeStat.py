class MazeStat:
    def __init__(self, size: int, scarcity: float, build_time: float):
        self.size = size
        self.scarcity = scarcity
        self.build_time = build_time
        self.solution_time: float | None = None
        self.num_solutions: int | None = None

    def set_solution_time(self, time: float) -> None:
        self.solution_time = time

    def set_num_solutions(self, value: int) -> None:
        self.num_solutions = value
