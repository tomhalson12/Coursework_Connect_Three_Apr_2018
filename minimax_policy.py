import numpy as np
import copy
import random


class mm_policy:
    
    def __init__(self):
        self.other_player = {'o':'x','x':'o'}
        self.branches = 0      
        self.action=0
        
    def reset(self):
        self.branches = 0
        self.action=0
        self.depth = 20
        self.dep_dic = {}
    
    '''
    choosing action based off branch values
    '''
    def policy_choose_action(self, env):
        self.reset()
        e = copy.deepcopy(env)
        e.change_turn()
        val = self.minimax(e,-10000,10000, self.depth, True)[0]
        dept = 100
        inde = ()
        #chooses the option with the highest value and the shortest branches
        for st in self.dep_dic:
            if self.dep_dic[st]['val'] == val:
                dept = min(dept, self.dep_dic[st]['depth'])
                if self.dep_dic[st]['depth'] == dept:
                    inde = inde + (st-1,)
        num = len(inde)
        choice = random.randint(0,num-1)
        rand_choice = inde[choice]
        self.action = env.available_actions[rand_choice]
        return self.action
    
    '''
    converts state to string
    '''
    def as_string(self, state):
        string = ""
        for x in state:
            for y in x:
                if not (y == 'o' or y == 'x'):
                    string = string + "-"
                else:
                    string = string + y
        return string
    '''
    gets the all states for every move possible in the parent state
    '''
    def get_child_states(self, env):
        env.change_turn()
        avail = env.available_actions
        depths = ()
        for x in range(5):
            depths = depths + (env.lowest_free_rows[x],)
            
        children = ()
        for a in avail:
            child = copy.deepcopy(env)
            child.act(a)
            #child.change_turn()
            children = children + (child,)
        return children
    
    '''
    minimax algorithm
    '''
    def minimax(self, env, alpha, beta, depth, max_player):
        self.branches = self.branches+1
        if env.was_winning_move():
            if not max_player:
                return 1, copy.copy(depth)
            else:
                return -1, copy.copy(depth)
        elif env.grid_is_full():
            return 0, copy.copy(depth)
        
        if depth == self.depth:
            count = 0
        
        if max_player:
            children = self.get_child_states(env)
            for ch in children:
                val, dep = self.minimax(ch, alpha, beta, depth-1, False)
                if depth == self.depth:
                    count = count +1
                    self.dep_dic[count] = {'val':val, 'depth':(self.depth-dep)}
                    
                alpha = max(alpha, val)
                if alpha >= beta:
                    break
            return alpha, dep
        else:
            children = self.get_child_states(env)
            
            for ch in children:
                val,dep = self.minimax(ch, alpha, beta, depth-1, True)
                beta = min(beta, val)
                if alpha >= beta:
                    break       
            return beta, dep
    
    