import random


class Game:
    MINIMAX = 0
    ALPHABETA = 1
    HUMAN = 2
    AI = 3

    def __init__(self, recommend=True, size=3, goal=3,block_count=0):
        self.size = size
        self.initialize_game()
        self.recommend = recommend
        self.goal = goal
        self.block_count=block_count
        self.remain_blocks=block_count

    def initialize_game(self):
        self.current_state = [["."] * self.size for i in range(self.size)]
        # Player X always plays first
        self.player_turn = 'X'

    def put_block(self,px,py):
        if self.remain_blocks ==0:
            return False
        if self.current_state[px][py]!='.':
            return False
        self.current_state[px][py]='*'
        self.remain_blocks=self.remain_blocks-1
        return True

    def put_random_blocks(self):
        while self.remain_blocks>0:
            self.put_block(random.randrange(self.size),random.randrange(self.size))

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

def main():
    g = Game(size=5,block_count=5)
    g.put_random_blocks()
    # some simple testing
    # g.current_state[0][4] = 'o'
    # g.current_state[1][3] = 'x'
    # g.current_state[2][2] = 'x'
    # g.current_state[3][1] = "x"
    # g.current_state[4][0] = "o"


    print(g.is_end())
    print(g.check_back_diagonal(0, 4))
    # print(g.current_state[1][0])
    g.draw_board()


if __name__ == '__main__':
    main()
