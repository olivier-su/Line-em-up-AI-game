from game import Game
import heuristics

def run_customized_game():
    size=input("Please enter the board size[3-10]: ")
    goal=input('Please enter the wining line-up size[3-size]: ')
    print('Please enter the mode you want: ')
    print('1.Human to Human')
    print('2.Human to AI')
    print('3.AI to Human')
    print('4.AI to AI')
    mode=input('Your choice: ')
    alphabeta=Game.MINIMAX
    time_allowed='5'
    player_X=Game.HUMAN
    player_Y=Game.HUMAN
    if mode==2 or mode == 3 or mode ==4:
        alphabeta_choice=input('Would you like to use alpha-beta for AI(s)? (y/n)')
        if alphabeta_choice=='y':
            alphabeta=Game.ALPHABETA
        time_allowed=input('Please enter the maximum allowed toime for AI(s): ')
    depth1=0
    if mode==3 or mode ==4:
        player_X=Game.AI
        depth1=input('Please enter the maximum searching depth for AI X:')
    depth2=0
    if mode==2 or mode==4:
        player_Y=Game.AI
        depth2=input('Please enter the maximum searching depth for AI O:')


    block_count=input('Please enter how may blocks do you want[0-2*size]: ')
    game= Game(size=size,goal=goal,block_count=block_count,maximum_depth_player_X=depth1,
               maximum_depth_player_O=depth2, search_time=time_allowed)
    place_randomly=input('Would you like to please blocks randomly? (y/n)')
    if place_randomly=='n':
        while game.block_count>0:
            block_index=input('Please enter where do you want to put the block by index(A1,B2 etc.): ')
            index_x=ord(block_index[0])
            index_y=int(blokc_index[1])
            if game.put_block(index_x,index_y):
                print('Placement success!')
            else:
                print('Placement fail')
    else:
        game.put_random_blocks()

    game.play(algo=alphabeta,player_x=player_X,player_y=player_Y)


def run_preset_experiments():
    pass

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
    if choice =='1':
        run_customized_game()
    elif choice =='2':
        run_preset_experiments()
    else:
        print('Invalid input, will run preset experiments')
        run_preset_experiments()







if __name__ == '__main__':
    main()
