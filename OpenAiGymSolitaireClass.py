# Class to have a interface to PositionClass which will enable OpenAI Gym to use it for reinforcement learning
# See tutorials https://blog.paperspace.com/getting-started-with-openai-gym/
# https://blog.paperspace.com/creating-custom-environments-openai-gym/
# Laurence Smith
# 09/08/2022

import PositionClass

import gym
import random
import numpy as np

from gym import Env, spaces
#import time

class OpenAiGymSolitaireClass(Env):
    def __init__(self) -> None:
        super(OpenAiGymSolitaireClass, self).__init__()

        # Define a 2-D observation space
        # represent each place as a position in a matrix as per gameStr
        # foundStr0 = "Foundation Clubs: "   # max len 13
        # foundStr1 = "Foundation Diamonds: " # max len 13
        # foundStr2 = "Foundation Hearts: "  # max len 13
        # foundStr3 = "Foundation Spades: "  # max len 13
        # stockStr = "Stock: "               # max len 24
        # wasteStr = "Waste: "               # max len 24
        # tableauStr = "Tableau:\n"  *7        # max len 20
        

        # max length of any pile is 24 and 13 piles
        # each card represented by a number from 0 to 51, use -1 to be a card where can only see the back so visible=false, use -2 to be an empty space
        self.observation_space = spaces.Box(low=-2, high=51, shape=(13, 24), dtype=np.int32)        
    
        
        # Define an action space ranging from 0 to 4
        self.action_space = spaces.Discrete(16613,start=1) # as per codes used for moves ToDo should we enumerate all possibilities to remove all the numbers that aren't allowed - would probably make AI much quicker


# testing spaces
#x = spaces.Box(low=-2, high=51, shape=(13, 24), dtype=np.int32) 
#print(x.sample())                        

#x = spaces.Discrete(16613,start=1)
#print(x.sample())                        