class Game:
    MINIMAX = 0
    ALPHABETA = 1
    HUMAN = 2
    AI = 3

    def __init__(self, recommend=True, size=3, goal=3):
        self.size = size
        self.initialize_game()
        self.recommend = recommend
        self.goal = goal

    def initialize_game(self):
        self.current_state = [["."] * self.size for i in range(self.size)]
        # Player X always plays first
        self.player_turn = 'X'

    def draw_board(self):
        print()
        print(" +", end="")
        for i in range(self.size):
            print(chr(ord('A')+i),end="")
        print()
        for y in range(0, self.size):
            print(f"{y}|",end="")
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

    def is_end(self):
        # Horizontal win
        for i in range(0, self.size):
            for j in range(self.size-self.goal+1):#-goal for border
                should_continue = False;
                for x in range(self.goal-1):
                    if(self.current_state[j][i] == '.'or self.current_state[j][i] == "*" or self.current_state[j][i]!=self.current_state[j+1+x][i]):
                        should_continue=True
                        break
                if not should_continue:
                    return self.current_state[j][i]

        # # Vertical win
        for j in range(0, self.size):
            for i in range(self.size-self.goal+1):#-goal for border
                should_continue = False;
                for x in range(self.goal-1):
                    if(self.current_state[j][i] == '.'or self.current_state[j][i] == "*" or self.current_state[j][i]!=self.current_state[j][i+1+x]):
                        should_continue=True
                        break
                if not should_continue:
                    return self.current_state[j][i]


        # # Horizontal win
        # for i in range(0, 3):
        #     if (self.current_state[i] == ['X', 'X', 'X']):
        #         return 'X'
        #     elif (self.current_state[i] == ['O', 'O', 'O']):
        #         return 'O'
        # # Main diagonal win
        # if (self.current_state[0][0] != '.' and
        #         self.current_state[0][0] == self.current_state[1][1] and
        #         self.current_state[0][0] == self.current_state[2][2]):
        #     return self.current_state[0][0]
        # # Second diagonal win
        # if (self.current_state[0][2] != '.' and
        #         self.current_state[0][2] == self.current_state[1][1] and
        #         self.current_state[0][2] == self.current_state[2][0]):
        #     return self.current_state[0][2]
        # # Is whole board full?
        # for i in range(0, 3):
        #     for j in range(0, 3):
        #         # There's an empty field, we continue the game
        #         if (self.current_state[i][j] == '.'):
        #             return None

        # It's a tie!
        return '.'

def main():
    g = Game(size=5)

    # some simple testing
    g.current_state[1][0] = 'o'
    g.current_state[1][1] = 'o'
    g.current_state[1][2] = 'x'
    g.current_state[1][3] = "x"
    g.current_state[1][4] = "x"

    print(g.is_end())
    #print(g.current_state[1][0])
    g.draw_board()


if __name__ == '__main__':
    main()
