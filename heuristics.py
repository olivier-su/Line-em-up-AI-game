import game as Game
from abc import ABC, abstractmethod
import re


class HeuristicStrategy(ABC):
    max_target = 'O'
    min_target = 'X'

    @abstractmethod
    def evaluate_state(self, state, size, goal):
        pass

    @abstractmethod
    def get_winning_score(self):
        pass

    @abstractmethod
    def get_type(self):
        pass


def is_in_valid_range(size, x, y):
    if 0 <= x < size and 0 <= y < size:
        return True
    return False


def check_empty_around(state, size, x, y):
    counter = 0

    for i in range(-1, 2):
        for j in range(-1, 2):
            if is_in_valid_range(size, x + i, y + j):
                if state[x + i][y + j] == '.':
                    counter = counter + 1
    return counter


class HeuristicE1(HeuristicStrategy):
    # count empty space around pieces and substruct pieces of another player
    # should be faster
    def evaluate_state(self, state, size, goal):
        score = 0
        for x in range(size):
            for y in range(size):
                if state[x][y] == self.max_target:
                    score += check_empty_around(state, size, x, y)
                if state[x][y] == self.min_target:
                    score -= check_empty_around(state, size, x, y)
        return score

    def get_winning_score(self):
        return 1000

    def get_type(self):
        return "e1"


# get that direction to a string, i and j indicate the direciton
# x y are starting node
def get_string_by_direction(state, size, x, y, i, j):
    row_str = ''
    while is_in_valid_range(size, x, y):
        row_str += state[x][y]
        x += i
        y += j
    return row_str


class HeuristicE2(HeuristicStrategy):

    def get_score_from_string(self, line_string, goal):
        score = 0
        # a reguler expression for searching
        # meaning: find countinues '.' or max_tartget or combination of both
        if re.search(f"[{self.max_target}.]{{{goal}}}", line_string):
            score += 1
            if re.search(f"\.{self.max_target}{{{goal-1}}}", line_string) or re.search(f"{self.max_target}{{{goal-1}}}\.", line_string):
                score+=10
        if re.search(f"[{self.min_target}.]{{{goal}}}", line_string):
            score -= 1
            if re.search(f"\.{self.min_target}{{{goal-1}}}", line_string) or re.search(f"{self.min_target}{{{goal-1}}}\.", line_string):
                score-=10
        return score

    def evaluate_state(self, state, size, goal):
        score = 0
        #check rows
        for x in range(size):
            line_string = get_string_by_direction(state,size,x,0,0,1)
            score += self.get_score_from_string(line_string, goal)
        #check columns
        for y in range(size):
            line_string=get_string_by_direction(state,size,0,y,1,0)
            score+=self.get_score_from_string(line_string,goal)
        #check '\' direction:
        for x in range(size):
            line_string = get_string_by_direction(state, size, x, 0, 1, 1)
            score += self.get_score_from_string(line_string, goal)
        for y in range(size):
            line_string=get_string_by_direction(state,size,0,y,1,1)
            score+=self.get_score_from_string(line_string,goal)

        #check '/' direction:
        for x in range(size):
            line_string = get_string_by_direction(state, size, x, size-1, 1, -1)
            score += self.get_score_from_string(line_string, goal)
        for y in range(size):
            line_string=get_string_by_direction(state,size,0,y,1,-1)
            score+=self.get_score_from_string(line_string,goal)

        return score

    def get_winning_score(self):
        return 1000

    def get_type(self):
        return "e2"
