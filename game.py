import random
import heuristics as Heuristic
import time


class Game:
    MINIMAX = 0
    ALPHABETA = 1
    HUMAN = 2
    AI = 3

    def __init__(self, recommend=True, size=3, goal=3, block_count=0, maximum_depth_player_X=0,
                 maximum_depth_player_O=0, search_time=5):
        self.size = size
        self.initialize_game()
        self.recommend = recommend
        self.goal = goal
        self.block_count = block_count
        self.remain_blocks = block_count
        self.heuristic = None
        self.max_depth_player_X = maximum_depth_player_X
        self.max_depth_player_O = maximum_depth_player_O
        self.search_time = search_time * 1000

    def set_heuristic(self, heuristic: Heuristic.HeuristicStrategy):
        self.heuristic = heuristic

    def evaluate_state(self):
        return self.heuristic.evaluate_state(self.current_state, self.size, self.goal)

    def get_winning_score(self):
        return self.heuristic.get_wining_score()

    def initialize_game(self):
        self.current_state = [["."] * self.size for i in range(self.size)]
        # Player X always plays first
        self.player_turn = 'X'

    def put_block(self, px, py):
        if self.remain_blocks == 0:
            return False
        if self.current_state[px][py] != '.':
            return False
        self.current_state[px][py] = '*'
        self.remain_blocks = self.remain_blocks - 1
        return True

    def put_random_blocks(self):
        while self.remain_blocks > 0:
            self.put_block(random.randrange(self.size), random.randrange(self.size))

    def draw_board(self):
        print()
        print(" +", end="")
        for i in range(self.size):
            print(chr(ord('A') + i), end="")
        print()
        for y in range(0, self.size):
            print(f"{y}|", end="")
            for x in range(0, self.size):
                print(F'{self.current_state[x][y]}', end="")
            print()
        print()

    def is_valid(self, px, py):
        if px < 0 or px > self.size - 1 or py < 0 or py > self.size - 1:
            return False
        elif self.current_state[px][py] != '.':
            return False
        else:
            return True

    # help to check the given diagonal
    # px and py are index of the start node of the diagonal, shuold use left end
    def check_diagonal(self, px, py):
        # if (px + self.goal > self.size) or (py + self.goal > self.size):
        #     return None
        length = self.size
        if px > 0:
            length -= px
        else:
            length -= py
        if length < self.goal:
            return None
        for j in range(length - self.goal + 1):  # -goal for border
            should_continue = False;
            for x in range(self.goal - 1):
                if (self.current_state[px + j][py + j] == '.' or self.current_state[px + j][py + j] == "*" or
                        self.current_state[px + j][py + j] !=
                        self.current_state[px + 1 + x + j][py + 1 + x + j]):
                    should_continue = True
                    break
            if not should_continue:
                return self.current_state[px + j][py + j]
        return None

    # similar to the above function. Left and down nodes are start nodes
    def check_back_diagonal(self, px, py):
        length = self.size
        if px == 0:
            length = py + 1
        else:
            length -= px
        if length < self.goal:
            return None
        for j in range(length - self.goal + 1):  # -goal for border
            should_continue = False;
            for x in range(self.goal - 1):
                if (self.current_state[px + j][py - j] == '.' or self.current_state[px + j][py - j] == "*" or
                        self.current_state[px + j][py - j] !=
                        self.current_state[px + 1 + x + j][py - 1 - x - j]):
                    should_continue = True
                    break
            if not should_continue:
                return self.current_state[px + j][py - j]
        return None

    def check_end(self):
        self.result = self.is_end()
        # Printing the appropriate message if the game has ended
        if self.result is not None:
            if self.result == 'X':
                print('The winner is X!')
            elif self.result == 'O':
                print('The winner is O!')
            elif self.result == '.':
                print("It's a tie!")
            self.initialize_game()
        return self.result

    def input_move(self):
        while True:
            print(F'Player {self.player_turn}, enter your move:')
            px = int(input('enter the x coordinate: '))
            py = int(input('enter the y coordinate: '))
            if self.is_valid(px, py):
                return (px, py)
            else:
                print('The move is not valid! Try again.')

    def switch_player(self):
        if self.player_turn == 'X':
            self.player_turn = 'O'
        elif self.player_turn == 'O':
            self.player_turn = 'X'
        return self.player_turn

    def is_end(self):
        # Horizontal win
        for i in range(0, self.size):
            for j in range(self.size - self.goal + 1):  # -goal for border
                should_continue = False;
                for x in range(self.goal - 1):
                    if self.current_state[j][i] == '.' or self.current_state[j][i] == "*" or self.current_state[j][i] != \
                            self.current_state[j + 1 + x][i]:
                        should_continue = True
                        break
                if not should_continue:
                    return self.current_state[j][i]

        # # Vertical win
        for j in range(0, self.size):
            for i in range(self.size - self.goal + 1):  # -goal for border
                should_continue = False;
                for x in range(self.goal - 1):
                    if self.current_state[j][i] == '.' or self.current_state[j][i] == "*" or self.current_state[j][i] != \
                            self.current_state[j][i + 1 + x]:
                        should_continue = True
                        break
                if not should_continue:
                    return self.current_state[j][i]

        # Main diagonal win
        # first half
        for i in range(self.size):
            result = self.check_diagonal(i, 0)
            if result is not None:
                return result
        # second half
        for i in range(1, self.size):
            result = self.check_diagonal(0, i)
            if result is not None:
                return result

        # Second diagonal win
        # first half
        for i in range(self.size):
            result = self.check_back_diagonal(0, i)
            if result is not None:
                return result
        # second half
        for i in range(1, self.size):
            result = self.check_back_diagonal(i, self.size - 1)
            if result is not None:
                return result

        # Is whole board full?
        for i in range(0, self.size):
            for j in range(0, self.size):
                # There's an empty field, we continue the game
                if self.current_state[i][j] == '.':
                    return None

        # It's a tie!
        return '.'

    def minimax(self,start_time, max=False, current_depth=0):
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -1 - win for 'X'
        # 0  - a tie
        # 1  - loss for 'X'
        # We're initially setting it to 2 or -2 as worse than the worst case:
        maximum_depth = self.max_depth_player_X
        value = 2
        if max:
            value = -2
            maximum_depth = self.max_depth_player_O
        x = None
        y = None
        result = self.is_end()
        if result == 'X':
            return (-1, x, y)
        elif result == 'O':
            return (1, x, y)
        elif result == '.':
            return (0, x, y)
        if (time.time()-start_time)*1000 >= self.search_time*0.9:
            return (self.evaluate_state(),x,y)
        if current_depth == maximum_depth:
            return (self.evaluate_state(), x, y)
        for i in range(0, 3):
            for j in range(0, 3):
                if self.current_state[i][j] == '.':
                    if max:
                        self.current_state[i][j] = 'O'
                        (v, _, _) = self.minimax(max=False, current_depth=current_depth + 1)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 'X'
                        (v, _, _) = self.minimax(max=True, current_depth=current_depth + 1)
                        if v < value:
                            value = v
                            x = i
                            y = j
                    self.current_state[i][j] = '.'
        return (value, x, y)

    def alphabeta(self,start_time, alpha=-2, beta=2, max=False, current_depth=0):
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -1 - win for 'X'
        # 0  - a tie
        # 1  - loss for 'X'
        # We're initially setting it to 2 or -2 as worse than the worst case:
        maximum_depth = self.max_depth_player_X
        value = 2
        if max:
            value = -2
            maximum_depth = self.max_depth_player_O
        x = None
        y = None
        result = self.is_end()
        if result == 'X':
            return (-1, x, y)
        elif result == 'O':
            return (1, x, y)
        elif result == '.':
            return (0, x, y)
        if (time.time()-start_time)*1000 >= self.search_time*0.9:
            return (self.evaluate_state(),x,y)
        if current_depth == maximum_depth:
            return (self.evaluate_state(), x, y)
        for i in range(0, 3):
            for j in range(0, 3):
                if self.current_state[i][j] == '.':
                    if max:
                        self.current_state[i][j] = 'O'
                        (v, _, _) = self.alphabeta(alpha, beta, max=False, current_depth=current_depth + 1)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 'X'
                        (v, _, _) = self.alphabeta(alpha, beta, max=True, current_depth=current_depth + 1)
                        if v < value:
                            value = v
                            x = i
                            y = j
                    self.current_state[i][j] = '.'
                    if max:
                        if value >= beta:
                            return (value, x, y)
                        if value > alpha:
                            alpha = value
                    else:
                        if value <= alpha:
                            return (value, x, y)
                        if value < beta:
                            beta = value
        return (value, x, y)

    def play(self, algo=None, player_x=None, player_o=None):
        if algo == None:
            algo = self.ALPHABETA
        if player_x == None:
            player_x = self.HUMAN
        if player_o == None:
            player_o = self.HUMAN
        while True:
            self.draw_board()
            if self.check_end():
                return
            start = time.time()
            if algo == self.MINIMAX:
                if self.player_turn == 'X':
                    (_, x, y) = self.minimax(max=False,start_time=start)
                else:
                    (_, x, y) = self.minimax(max=True, start_time=start)
            else:  # algo == self.ALPHABETA
                if self.player_turn == 'X':
                    (m, x, y) = self.alphabeta(max=False)
                else:
                    (m, x, y) = self.alphabeta(max=True)
            end = time.time()
            if (self.player_turn == 'X' and player_x == self.HUMAN) or (
                    self.player_turn == 'O' and player_o == self.HUMAN):
                if self.recommend:
                    print(F'Evaluation time: {round(end - start, 7)}s')
                    print(F'Recommended move: x = {x}, y = {y}')
                (x, y) = self.input_move()
            if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
                print(F'Evaluation time: {round(end - start, 7)}s')
                print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
            self.current_state[x][y] = self.player_turn
            self.switch_player()
