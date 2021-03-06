import random
import heuristics as Heuristic
import time

global_evaluation_time = []
global_heuristic_evaluation = 0
global_heuristic_evaluation_depth = {}
global_evaluation_depth = []
global_step_count=[]
global_recursion_depth=[]


class Game:
    MINIMAX = 0
    ALPHABETA = 1
    HUMAN = 2
    AI = 3

    def __init__(self, recommend=True, size=3, goal=3, block_count=0, maximum_depth_player_X=0,
                 maximum_depth_player_O=0, search_time=5):
        self.size = size
        self.block_count = block_count
        self.initialize_game()
        self.recommend = recommend
        self.goal = goal
        self.heuristic_X = Heuristic.HeuristicE1()
        self.heuristic_O = Heuristic.HeuristicE2()
        self.maximum_depth_player_X = maximum_depth_player_X
        self.maximum_depth_player_O = maximum_depth_player_O
        self.search_time = search_time
        self.blocks_coordinates = []
        self.trace_file = open(f"gameTrace-{self.size}{self.block_count}{self.goal}{self.search_time}.txt", "w")
        self.trace_file.write(f"n={self.size} b={self.block_count} s={self.goal} t={self.search_time}\n")

        self.step_depth_counter_X = {}
        self.step_depth_counter_O = {}

    def initialize_game(self):
        self.current_state = [["."] * self.size for i in range(self.size)]
        # Player X always plays first
        self.player_turn = 'X'
        self.remain_blocks = self.block_count
        self.evaluation_time_X = []
        self.evaluation_time_O = []
        self.total_heuristic_x = 0
        self.total_heuristic_o = 0
        self.total_heuristic_depth_x = {}
        self.total_heuristic_depth_o = {}
        self.evaluation_depth_x = []
        self.evaluation_depth_o = []
        self.step_count = 0
        self.recusion_depth_x=[]
        self.recusion_depth_o=[]

    def set_heuristic_X(self, heuristic: Heuristic.HeuristicStrategy):
        self.heuristic_X = heuristic

    def set_heuristic_O(self, heuristic: Heuristic.HeuristicStrategy):
        self.heuristic_O = heuristic

    def evaluate_state(self, player):
        if player == 'X':
            return self.heuristic_X.evaluate_state(self.current_state, self.size, self.goal)
        else:
            return self.heuristic_O.evaluate_state(self.current_state, self.size, self.goal)

    # def evaluate_state_O(self):
    #     return self.heuristic_O.evaluate_state(self.current_state, self.size, self.goal)

    def get_winning_score(self, player):
        if player == 'X':
            return self.heuristic_X.get_winning_score()
        else:
            return self.heuristic_O.get_winning_score()

    # def get_winning_score_O(self):
    #     return self.heuristic_O.get_wining_score()

    def put_block(self, px, py):
        if self.remain_blocks == 0:
            return False
        if self.current_state[px][py] != '.':
            return False
        self.current_state[px][py] = '*'
        coordinates = (px, py)
        self.blocks_coordinates.append(coordinates)
        self.remain_blocks = self.remain_blocks - 1
        return True

    def put_random_blocks(self):
        while self.remain_blocks > 0:
            self.put_block(random.randrange(self.size), random.randrange(self.size))
        self.trace_file.write(f"blocs={self.blocks_coordinates}\n")

    def draw_board(self):
        print()
        print(" +", end="")
        self.trace_file.write(" +")
        for i in range(self.size):
            print(chr(ord('A') + i), end="")
            self.trace_file.write(chr(ord('A') + i))
        print()
        self.trace_file.write("\n")
        for y in range(0, self.size):
            print(f"{y}|", end="")
            self.trace_file.write(f"{y}|")
            for x in range(0, self.size):
                print(F'{self.current_state[x][y]}', end="")
                self.trace_file.write(F'{self.current_state[x][y]}')
            print()
            self.trace_file.write("\n")
        print()
        self.trace_file.write("\n")

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

    def out_trace_result(self):
        self.trace_file.write(f"\nFor X:\n")
        evaluation_time_sum = 0
        for t in self.evaluation_time_X:
            evaluation_time_sum += t
        evaluation_time_x = evaluation_time_sum / len(self.evaluation_time_X)
        global_evaluation_time.append(evaluation_time_x)
        self.trace_file.write(f"6(b)i   Average evaluation time: {evaluation_time_x}\n")
        self.trace_file.write(f'6(b)ii  Total heuristic evaluations: {self.total_heuristic_x}\n')
        global global_heuristic_evaluation
        global_heuristic_evaluation+= self.total_heuristic_x
        for key in self.total_heuristic_depth_x:
            if key in global_heuristic_evaluation_depth:
                global_heuristic_evaluation_depth[key]+=self.total_heuristic_depth_x[key]
            else:
                global_heuristic_evaluation_depth[key]=self.total_heuristic_depth_x[key]

        self.trace_file.write(f'6(b)iii Evaluations by depth: {self.total_heuristic_depth_x}\n')
        evaluation_depth_sum = 0
        for d in self.evaluation_depth_x:
            evaluation_depth_sum += d
        evaluation_depth_x = evaluation_depth_sum / len(self.evaluation_depth_x)
        self.trace_file.write(f'6(b)iv  Average evaluation depth: {evaluation_depth_x}\n')
        global_evaluation_depth.append(evaluation_depth_x)

        recursion_depth=sum(self.recusion_depth_x)/len(self.recusion_depth_x)
        self.trace_file.write(f'6(b)v   Average recursion depth: {recursion_depth}\n')
        global_recursion_depth.append(recursion_depth)

        self.trace_file.write(f'6(b)vi  Total moves: {self.step_count}\n')
        global_step_count.append(self.step_count)



        self.trace_file.write(f"\nFor Y:\n")
        evaluation_time_sum = 0
        for t in self.evaluation_time_O:
            evaluation_time_sum += t
        evaluation_time_o = evaluation_time_sum / len(self.evaluation_time_O)
        global_evaluation_time.append(evaluation_time_o)
        self.trace_file.write(f"6(b)i   Average evaluation time: {evaluation_time_o}\n")
        self.trace_file.write(f'6(b)ii  Total heuristic evaluations: {self.total_heuristic_o}\n')

        global_heuristic_evaluation += self.total_heuristic_o
        for key in self.total_heuristic_depth_o:
            if key in global_heuristic_evaluation_depth:
                global_heuristic_evaluation_depth[key] += self.total_heuristic_depth_o[key]
            else:
                global_heuristic_evaluation_depth[key] = self.total_heuristic_depth_o[key]

        self.trace_file.write(f'6(b)iii Evaluations by depth: {self.total_heuristic_depth_o}\n')
        evaluation_depth_sum = 0
        for d in self.evaluation_depth_o:
            evaluation_depth_sum += d
        evaluation_depth_o = evaluation_depth_sum / len(self.evaluation_depth_o)
        self.trace_file.write(f'6(b)iv  Average evaluation depth: {evaluation_depth_o}\n')
        global_evaluation_depth.append(evaluation_depth_o)

        recursion_depth_o = sum(self.recusion_depth_o) / len(self.recusion_depth_o)
        self.trace_file.write(f'6(b)v   Average recursion depth: {recursion_depth_o}\n')
        global_recursion_depth.append(recursion_depth_o)

        #step should only show once
        # self.trace_file.write(f'6(b)vi  Total moves: {self.step_count}')
        # global_step_count.append(self.step_count)
    def check_end(self):
        self.result = self.is_end()
        # Printing the appropriate message if the game has ended
        if self.result is not None:
            if self.result == 'X':
                print('The winner is X!')
                self.trace_file.write('The winner is X!\n')
            elif self.result == 'O':
                print('The winner is O!')
                self.trace_file.write('The winner is O!\n')
            elif self.result == '.':
                print("It's a tie!")
                self.trace_file.write("It's a tie!\n")
            self.out_trace_result()
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

    def add_step_counter(self, current_player, current_depth):
        if current_player == 'X':
            if current_depth in self.step_depth_counter_X:
                self.step_depth_counter_X[current_depth] += 1
            else:
                self.step_depth_counter_X[current_depth] = 1
            if current_depth in self.total_heuristic_depth_x:
                self.total_heuristic_depth_x[current_depth] += 1
            else:
                self.total_heuristic_depth_x[current_depth] = 1
        if current_player == 'O':
            if current_depth in self.step_depth_counter_O:
                self.step_depth_counter_O[current_depth] += 1
            else:
                self.step_depth_counter_O[current_depth] = 1
            if current_depth in self.total_heuristic_depth_o:
                self.total_heuristic_depth_o[current_depth] += 1
            else:
                self.total_heuristic_depth_o[current_depth] = 1

    def minimax(self, start_time, current_player, max=False, current_depth=0):
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -1 - win for 'X'
        # 0  - a tie
        # 1  - loss for 'X'
        # We're initially setting it to 2 or -2 as worse than the worst case:

        winning_score = self.get_winning_score('O')
        maximum_depth = self.maximum_depth_player_O

        if current_player == 'X':
            winning_score = self.get_winning_score('X')
            maximum_depth = self.maximum_depth_player_X
        value = winning_score * 2
        if max:
            value = -value
        x = None
        y = None
        result = self.is_end()
        if result == 'X':
            self.add_step_counter(current_player, current_depth)
            return (-winning_score, x, y,current_depth)
        elif result == 'O':
            self.add_step_counter(current_player, current_depth)
            return (winning_score, x, y,current_depth)
        elif result == '.':
            self.add_step_counter(current_player, current_depth)
            return (0, x, y,current_depth)
        current_time=time.time()
        if ( current_time- start_time)  >= self.search_time * 0.9:
            self.add_step_counter(current_player, current_depth)
            return (self.evaluate_state(current_player), x, y,current_depth)
        if current_depth == maximum_depth:
            self.add_step_counter(current_player, current_depth)
            return (self.evaluate_state(current_player), x, y,current_depth)
        previous_depth=[]
        for i in range(0, self.size):
            for j in range(0, self.size):
                if self.current_state[i][j] == '.':
                    depth=0
                    if max:
                        self.current_state[i][j] = 'O'
                        (v, _, _,depth) = self.minimax(start_time, current_player, max=False, current_depth=current_depth + 1)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 'X'
                        (v, _, _,depth) = self.minimax(start_time, current_player, max=True, current_depth=current_depth + 1)
                        if v < value:
                            value = v
                            x = i
                            y = j
                    self.current_state[i][j] = '.'
                    previous_depth.append(depth)
        return (value, x, y,sum(previous_depth)/len(previous_depth))

    def alphabeta(self, start_time, current_player, alpha=-2, beta=2, max=False, current_depth=0):
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -1 - win for 'X'
        # 0  - a tie
        # 1  - loss for 'X'
        # We're initially setting it to 2 or -2 as worse than the worst case:
        winning_score = self.get_winning_score('O')
        maximum_depth = self.maximum_depth_player_O

        if current_player == 'X':
            winning_score = self.get_winning_score('X')
            maximum_depth = self.maximum_depth_player_X
        value = winning_score * 2
        if max:
            value = -value
        x = None
        y = None
        result = self.is_end()
        if result == 'X':
            self.add_step_counter(current_player, current_depth)
            return (-winning_score, x, y,current_depth)
        elif result == 'O':
            self.add_step_counter(current_player, current_depth)
            return (winning_score, x, y,current_depth)
        elif result == '.':
            self.add_step_counter(current_player, current_depth)
            return (0, x, y,current_depth)
        current_time=time.time()
        if (current_time - start_time) >= self.search_time * 0.9:
            self.add_step_counter(current_player, current_depth)
            return (self.evaluate_state(current_player), x, y,current_depth)
        if current_depth == maximum_depth:
            self.add_step_counter(current_player, current_depth)
            return (self.evaluate_state(current_player), x, y,current_depth)
        previous_depth=[]
        for i in range(0, self.size):
            for j in range(0, self.size):
                if self.current_state[i][j] == '.':
                    depth=0
                    if max:
                        self.current_state[i][j] = 'O'
                        (v, _, _,depth) = self.alphabeta(start_time, current_player, alpha, beta, max=False,
                                                   current_depth=current_depth + 1)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 'X'
                        (v, _, _,depth) = self.alphabeta(start_time, current_player, alpha, beta, max=True,
                                                   current_depth=current_depth + 1)
                        if v < value:
                            value = v
                            x = i
                            y = j
                    self.current_state[i][j] = '.'
                    previous_depth.append(depth)
                    if max:
                        if value >= beta:
                            return (value, x, y,sum(previous_depth)/len(previous_depth))
                        if value > alpha:
                            alpha = value
                    else:
                        if value <= alpha:
                            return (value, x, y,sum(previous_depth)/len(previous_depth))
                        if value < beta:
                            beta = value
        return (value, x, y,sum(previous_depth)/len(previous_depth))

    def play(self, algo_x=None, algo_o=None, player_x=None, player_o=None):
        heuristic_count_x_last_time = 0
        heuristic_count_o_last_time = 0
        if algo_x == None:
            algo_x = self.ALPHABETA
        if algo_o == None:
            algo_o = self.ALPHABETA
        if player_x == None:
            player_x = self.HUMAN
        if player_o == None:
            player_o = self.HUMAN
        self.trace_file.write(
            f"\nPlayer 1: {player_x} d={self.maximum_depth_player_X} a={algo_x == self.ALPHABETA} {self.heuristic_X.get_type()}\n")
        self.trace_file.write(
            f"Player 2: {player_o} d={self.maximum_depth_player_O} a={algo_x == self.ALPHABETA} {self.heuristic_O.get_type()}\n\n")
        average_recursion_depth=0.0
        while True:
            self.draw_board()
            result = self.check_end()
            if result:
                return result
            start = time.time()
            if algo_x == self.MINIMAX:
                if self.player_turn == 'X':
                    (_, x, y,average_recursion_depth) = self.minimax(max=False, start_time=start, current_player=self.player_turn)
            elif algo_x == self.ALPHABETA:  # algo == self.ALPHABETA
                if self.player_turn == 'X':
                    (m, x, y,average_recursion_depth) = self.alphabeta(max=False, start_time=start, current_player=self.player_turn)
            if algo_o == self.MINIMAX:
                if self.player_turn == 'O':
                    (_, x, y,average_recursion_depth) = self.minimax(max=True, start_time=start, current_player=self.player_turn)
            elif algo_o == self.ALPHABETA:  # algo == self.ALPHABETA
                if self.player_turn == 'O':
                    (m, x, y,average_recursion_depth) = self.alphabeta(max=True, start_time=start, current_player=self.player_turn)
            end = time.time()
            current_player_type = "Human"
            if (self.player_turn == 'X' and player_x == self.HUMAN) or (
                    self.player_turn == 'O' and player_o == self.HUMAN):
                if self.recommend:
                    print(F'Evaluation time: {round(end - start, 7)}s')
                    print(F'Recommended move: x = {x}, y = {y}')
                (x, y) = self.input_move()
            if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
                current_player_type = "AI"
                print(F'Evaluation time: {round(end - start, 7)}s')
                print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
            self.current_state[x][y] = self.player_turn
            self.step_count += 1
            self.trace_file.write(f'Move{self.step_count}\n')
            self.trace_file.write(
                f"Player {self.player_turn} under {current_player_type} control plays: {chr(ord('A') + x)}{y}\n")
            self.trace_file.write(f"i   Evaluation time: {end - start}s\n")
            heuristic_count = 0
            depth_counter = {}

            if self.player_turn == 'X':
                # heuristic_count = self.heuristic_X.evaluation_count - heuristic_count_x_last_time
                heuristic_count_x_last_time = self.heuristic_X.evaluation_count
                depth_counter = self.step_depth_counter_X
                self.step_depth_counter_X = {}
                self.evaluation_time_X.append(end - start)

            else:
                # heuristic_count = self.heuristic_O.evaluation_count - heuristic_count_o_last_time
                heuristic_count_o_last_time = self.heuristic_O.evaluation_count
                depth_counter = self.step_depth_counter_O
                self.step_depth_counter_O = {}
                self.evaluation_time_O.append(end - start)
            denominator = 0
            numerator = 0
            for key in depth_counter:
                denominator += key * depth_counter[key]
                numerator += depth_counter[key]
            average_depth = denominator / numerator
            if self.player_turn == 'X':
                self.total_heuristic_x += numerator
                self.evaluation_depth_x.append(average_depth)
                self.recusion_depth_x.append(average_recursion_depth)
            else:
                self.total_heuristic_o += numerator
                self.evaluation_depth_o.append(average_depth)
                self.recusion_depth_o.append(average_recursion_depth)
            self.trace_file.write(f"ii  Heuristic evaluations: {numerator}\n")
            self.trace_file.write(f"iii Evaluations by depth: {depth_counter}\n")
            self.trace_file.write(f'iv  Average evaluation depth: {average_depth}\n')
            self.trace_file.write(f'v   Average recursion depth: {average_recursion_depth}\n\n\n')
            self.switch_player()
