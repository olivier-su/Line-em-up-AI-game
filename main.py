import game
from game import *
import heuristics as Heuristic
from statistics import mean


def run_customized_game():
    size = int(input("Please enter the board size[3-10]: "))
    goal = int(input('Please enter the wining line-up size[3-size]: '))
    print('Please enter the mode you want: ')
    print('1.Human to Human')
    print('2.Human to AI')
    print('3.AI to Human')
    print('4.AI to AI')
    mode = int(input('Your choice: '))
    alphabeta_x = Game.MINIMAX
    alphabeta_y = Game.MINIMAX
    time_allowed = '5'
    player_X = Game.HUMAN
    player_Y = Game.HUMAN
    if mode == 2 or mode == 3 or mode == 4:
        time_allowed = int(input('Please enter the maximum allowed time for AI(s): '))
    depth1 = 0
    if mode == 3 or mode == 4:
        alphabeta_choice = input('Would you like to use alpha-beta for AI X? (y/n)')
        if alphabeta_choice == 'y':
            alphabeta_x = Game.ALPHABETA
        player_X = Game.AI
        depth1 = int(input('Please enter the maximum searching depth for AI X:'))
    depth2 = 0
    if mode == 2 or mode == 4:
        alphabeta_choice = input('Would you like to use alpha-beta for AI Y? (y/n)')
        if alphabeta_choice == 'y':
            alphabeta_y = Game.ALPHABETA
        player_Y = Game.AI
        depth2 = int(input('Please enter the maximum searching depth for AI O:'))

    block_count = int(input('Please enter how may blocks do you want[0-2*size]: '))
    game = Game(size=size, goal=goal, block_count=block_count, maximum_depth_player_X=depth1,
                maximum_depth_player_O=depth2, search_time=time_allowed)
    place_randomly = input('Would you like to place blocks randomly? (y/n)')
    if place_randomly == 'n':
        while game.remain_blocks > 0:
            block_index = input('Please enter where do you want to put the block by index(A1,B2 etc.): ')
            index_x = ord(block_index[0]) - ord('A')
            index_y = int(block_index[1])
            if game.put_block(index_x, index_y):
                print('Placement success!')
            else:
                print('Placement fail')
    else:
        game.put_random_blocks()

    game.play(algo_x=alphabeta_x, algo_o=alphabeta_y, player_x=player_X, player_o=player_Y)


def run_games(n, b, s, t, d1, d2, a1, a2, block_position, repeat_times):

    #score_board = open(f"scoreboard-{n}{b}{s}{t}.txt", "a")
    score_board = open(f"scoreboard.txt", "a")
    score_board.write(f"n={n} b={b} s={s} t={t}\n")
    score_board.write(f"For player 1: d={d1}\t a={a1}\n")
    score_board.write(f"For player 2: d={d2}\t a={a2}\n\n")
    score_board.write(f'{repeat_times}*2 Games\n\n')
    e1_win_count=0
    e2_win_count=0
    algo_x = Game.MINIMAX
    algo_y = Game.MINIMAX
    if a1:
        algo_x = Game.ALPHABETA
    if a2:
        algo_y = Game.ALPHABETA
    for i in range(repeat_times):
        g = Game(size=n, block_count=b, goal=s, search_time=t, maximum_depth_player_X=d1,
                 maximum_depth_player_O=d2)
        g.set_heuristic_X(Heuristic.HeuristicE1())
        g.set_heuristic_O(Heuristic.HeuristicE2())
        if block_position is None:
            g.put_random_blocks()
        else:
            for block in block_position:
                g.put_block(block[0], block[1])
        result=g.play(algo_x=algo_x, algo_o=algo_y, player_x=Game.AI, player_o=Game.AI)
        if result=='X':
            e1_win_count+=1
        elif result=='O':
            e2_win_count+=1

        g = Game(size=n, block_count=b, goal=s, search_time=t, maximum_depth_player_X=d2,
                 maximum_depth_player_O=d1)
        g.set_heuristic_X(Heuristic.HeuristicE2())
        g.set_heuristic_O(Heuristic.HeuristicE1())
        if block_position is None:
            g.put_random_blocks()
        else:
            for block in block_position:
                g.put_block(block[0], block[1])
        result=g.play(algo_x=algo_y, algo_o=algo_x, player_x=Game.AI, player_o=Game.AI)
        if result=='X':
            e2_win_count+=1
        elif result=='O':
            e1_win_count+=1
    score_board.write(f'Total wins for heuristic e1: {e1_win_count} {e1_win_count/20*100}%\n' )
    score_board.write(f'Total wins for heuristic e2: {e2_win_count} {e2_win_count / 20 * 100}%\n\n')
    score_board.write(f'i   Average evaluation time: {mean(game.global_evaluation_time)}\n')
    score_board.write(f'ii  Total heuristic evaluations: {game.global_heuristic_evaluation}\n')
    score_board.write(f'iii Evaluations by depth: {game.global_heuristic_evaluation_depth}\n')
    score_board.write(f'iv  Average evaluation depth: {mean(game.global_evaluation_depth)}\n')

    score_board.write(f'vi  Average moves per game: {mean(game.global_step_count)}\n\n')

def run_preset_experiments():
    # the position given in the requirement is out of the bound (4) so used 3 to avoid it
    # 1. game4435
    block_position = [[0, 0], [0, 3], [3, 0], [3, 3]]
    run_games(4, 4, 3, 5, 6, 6, False, False, block_position, 10)
    # 2. game4431
    run_games(4, 4, 3, 1, 6, 6, True, True, block_position, 10)
    # 3. game5441
    run_games(5, 4, 4, 1, 2, 6, True, True, None, 10)
    # 4. game5445
    run_games(5, 4, 4, 5, 6, 6, True, True, None, 10)
    # 5. game8551
    run_games(8, 5, 5, 1, 2, 6, True, True, None, 10)
    # 6. game8555
    run_games(8, 5, 5, 5, 2, 6, True, True, None, 10)
    # 7. game8651
    run_games(8, 6, 5, 1, 6, 6, True, True, None, 10)
    # 8. game8655
    run_games(8, 6, 5, 5, 6, 6, True, True, None, 10)


def main():
    # some code for testing purpose
    # g = Game(size=5, block_count=5)
    # g.set_heuristic(heuristics.HeuristicE2())
    # g.put_random_blocks()
    # # some simple testing
    # g.current_state[0][4] = 'O'
    # g.current_state[1][3] = 'X'
    # g.current_state[2][2] = 'O'
    # g.current_state[3][1] = "O"
    # g.current_state[4][0] = "O"
    #
    # print(g.is_end())
    # print(g.evaluate_state())
    # # print(g.current_state[1][0])
    # g.draw_board()
    print("Welcome to Line 'em Up game!")
    print('What you want to do now?')
    print('1. Run a customized game')
    print('2. Run preset experiments')
    choice = input('Your choice:')
    if choice == '1':
        run_customized_game()
    elif choice == '2':
        run_preset_experiments()
    elif choice == '3':
        run_games(5,2,3,6,6,6,True,True,None,1)
    else:
        print('Invalid input, will run preset experiments')
        run_preset_experiments()


if __name__ == '__main__':
    main()
