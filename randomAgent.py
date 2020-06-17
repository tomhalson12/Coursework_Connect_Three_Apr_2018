## Old development version
import numpy as np
import random

class Agent:
    '''
    chooses random action
    '''
    def policy_choose_action(self,env):
        avail = env.available_actions
        num = len(avail)
        choice = random.randint(0,num-1)
        return avail[choice]