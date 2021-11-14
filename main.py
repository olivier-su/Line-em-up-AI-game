from game import Game


def main():
    g = Game(size=5, block_count=5)
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
