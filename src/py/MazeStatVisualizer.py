import matplotlib.pyplot as plt
import seaborn as sns
from MazeStat import MazeStat

sns.set_style("darkgrid")


class MazeStatVisualizer:
    def __init__(self):
        pass

    def plot(self, stats: list[MazeStat]) -> None:
        sizes = [stat.size for stat in stats]
        build_times = [stat.build_time for stat in stats]
        maze_ids = list(range(1, len(stats) + 1))

        fig, axs = plt.subplots(1, 2, figsize=(12, 5))

        # Size vs Build Time
        sns.scatterplot(x=sizes, y=build_times, ax=axs[0], color="blue", alpha=0.7)
        axs[0].set_xlabel("Maze Size")
        axs[0].set_ylabel("Build Time (s)")
        axs[0].set_title("Maze Size vs. Build Time")

        # Histogram of Build Times
        bins = sns.histplot(
            build_times, bins=10, ax=axs[1], color="purple", kde=True, alpha=0.7
        )
        axs[1].set_xlabel("Build Time (s)")
        axs[1].set_ylabel("Frequency")
        axs[1].set_title("Distribution of Build Times")

        plt.tight_layout()
        plt.show()
