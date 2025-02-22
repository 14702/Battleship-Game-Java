from abc import ABC, abstractmethod
import random


class FiringStrategy(ABC):
    def __init__(self, sample_set):
        self.sample_set = sample_set

    @abstractmethod
    def fire(self, current_player, battlefield, previous_point):
        pass


class RandomFiringStrategy(FiringStrategy):
    def __init__(self, sample_set):
        super().__init__(sample_set)

    def fire(self, current_player, battlefield, previous_point):
        index = random.randint(0, len(self.sample_set)-1)
        (i, j) = self.sample_set[index]
        point = battlefield.grid[i][j]

        while (point.assignedPlayer and point.assignedPlayer == current_player.id) or (i, j) == previous_point:
            index = random.randint(0, len(self.sample_set)-1)
            (i, j) = self.sample_set[index]
            point = battlefield.grid[i][j]

        return point
