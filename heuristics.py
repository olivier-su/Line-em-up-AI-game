import game as Game
from abc import ABC, abstractmethod


class HeuristicStrategy(ABC):

    @abstractmethod
    def evaluate_state(self, state, size, goal):
        pass


class HeuristicE1(HeuristicStrategy):

    def evaluate_state(self, state, size, goal):
        print('e1')


class HeuristicE2(HeuristicStrategy):

    def evaluate_state(self, state, size, goal):
        print('e2')
