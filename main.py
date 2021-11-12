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


def main():
    g = Game(size=10)

    # some simple testing
    g.current_state[0][0] = '*'
    print(g.is_valid(1, 0))
    g.draw_board()


if __name__ == '__main__':
    main()
