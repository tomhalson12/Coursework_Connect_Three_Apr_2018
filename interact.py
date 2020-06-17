import numpy as np
import connect
import copy

class Interact:
    
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.env = connect.Connect(verbose=self.verbose)
        
    '''
    Game loop for the learn phase of the q-agent
    Continually plays games untill q-agent has n-interactions
    
    '''
    def learn_phase(self, interactions, a1,a2):
        player = 'o'
        self.env.reset(first_player='o')
        score = 0
        count = 0
        
        #Opponent plays first move in middle as specified in spec
        start_action = 2
        self.env.act(start_action)
        self.env.change_turn()

        while count < interactions:
            if(self.env.player_at_turn == 'o'):
                action = a1.policy_choose_action(self.env)
                self.env.act(action)
            else:
                action = a2.learn_choose_action(self.env)
                self.env.act(action)
                a2.learn_update(self.env,self.env.was_winning_move())
                count= count+1
            
            if(self.env.was_winning_move()):
                if(self.env.player_at_turn == 'o'):
                    score = score - 1
                else:
                    score = score + 1
                self.env.reset(first_player='o')
                self.env.act(start_action)
                self.env.change_turn()
            elif(self.env.grid_is_full()):
                self.env.reset(first_player='o')
                self.env.act(start_action)
                self.env.change_turn()
            else:
                self.env.change_turn()
        return a1, a2
            
    '''
    single game based off of agents policys
    '''
    def play_game(self, a1, a2):
        self.env.reset(first_player='o')
        loop = True
        #Opponent plays first move in middle as specified in spec
        action = 2
        self.env.perform_action(action)
        
        while(loop):
            if(self.env.player_at_turn == 'o'):
                action = a1.policy_choose_action(self.env)
            else:
                action = a2.policy_choose_action(self.env)

            loop = self.env.perform_action(action)
            outcome = 1
            if self.env.grid_is_full():
                loop = False
                outcome = 0
        
        if(outcome == 1):
            if(self.env.player_at_turn == 'x'):
                return 1
            else:
                return -1
        else:
            return 0
        
    '''
    play number of games
    '''
    def play_games(self, num_games, a1, a2):
        score = 0
        for x in range(num_games):
            score = score + self.play_game(a1,a2)
        return score