import numpy as np
import random
import copy
import operator

class Agent:
    
    def __init__(self, q={}):
        self.q = q
        self.new = True
        self.upd = False
    
    def reset(self):
        self.q = {}
        self.new = True
        self.upd = False
    
    '''
    checks if state already visited
    '''
    def in_q(self,state):
        if state in self.q:
            return True
        else:
            return False
        
    #adds state
    def add_state_q(self, state):
        self.q[state] = {0:0, 1:0, 2:0, 3:0, 4:0}
    
    '''
    returns max q_val of a state
    '''
    def max_q_value(self, state, avail):
        state_vals = self.q[state]
        vals = {}
        for a in avail:
            vals[a] = state_vals[a]
        
        ans = max(vals.items(), key=operator.itemgetter(1))
        
        return ans[0], ans[1]
            
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
    chooses an action based on q -values
    '''
    def choose_action(self):
        num = len(self.avail)
        choice = random.randint(0,num-1)
        rand_choice = self.avail[choice]
        
        ep = random.randint(0,100)
        
        if(ep <= 10):
            self.action = rand_choice
            self.q_val = self.q[self.state_string][self.action]
        else:
            self.action, self.q_val = self.max_q_value(self.state_string, self.avail)
            if(self.q_val == 0):
                self.action = rand_choice
    '''
    choose action option during learning phase
    adds new states to the policy
    '''
    def learn_choose_action(self,envs):
        env = copy.copy(envs)
        state = env.grid
        self.state_string = self.as_string(state)
        self.avail = env.available_actions 

        if(not self.in_q(self.state_string)):
            self.add_state_q(self.state_string)
            
        self.choose_action()
  
        return self.action
    
    '''
    after choosing a move, the q-values are updated based on the reward
    '''
    def learn_update(self, env, win):
        if self.new == False:
            self.upd = True
            old = self.prev
        state = env.grid
        st_string = self.as_string(state)
        self.prev = st_string
        avails = env.available_actions

        if(not self.in_q(st_string)):
            self.add_state_q(st_string)
            
        if(env.grid_is_full()):
            max_q_val = 0
        else:
            act, max_q_val = self.max_q_value(st_string, avails)
        
        if(win):
            self.q[st_string] = {0:100, 1:100, 2:100, 3:100, 4:100}
            max_q_val = 100
            self.q[self.state_string][self.action] = self.q_val + (100 + 0.80 *(max_q_val - self.q_val ))
        else:
            self.q[self.state_string][self.action] = self.q_val + 0.8 * (max_q_val - self.q_val)
            self.new = False
            
        if self.upd == True:
            self.q[old] = self.q[self.state_string]
  
    '''
    choosing an action based on the policy and not learning
    '''
    def policy_choose_action(self,env):
        state = env.grid
        self.state_string = self.as_string(state)
        self.avail = env.available_actions
        
        if(not self.in_q(self.state_string)):
            num = len(self.avail)
            choice = random.randint(0,num-1)
            return self.avail[choice]
            
        self.choose_action()
        return self.action
    