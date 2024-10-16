# Class to have a interface to PositionClass which will enable OpenAI Gym to use it for reinforcement learning
# See tutorials https://blog.paperspace.com/getting-started-with-openai-gym/
# https://gymnasium.farama.org/tutorials/gymnasium_basics/environment_creation/
# Laurence Smith
# 09/08/2022

import PositionClass

import gymnasium as gym
import random
import numpy as np
import pandas as pd
import sys
import io
import pickle

from gymnasium import Env, spaces
#import time

class OpenAiGymSolitaireClass(Env):
    metadata = {"render_modes": ["ansi",], "render_fps": 4} #TODO check this is right!

    def __init__(self, render_mode="ansi", verbose=True) -> None:
        #print("In __init__")
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
    
        
        # Define an action space 
        # 1st try had too many impossible moves: self.action_space = spaces.Discrete(16613,start=1), as per codes used for moves. 
        # Changed to enumerate all possibilities to remove all the numbers that aren't allowed.
        # import enumeration of moves to reduce number of impossible moves
        self.move_enumeration = pd.read_csv("move_enumeration.csv") # file containing columns "enumeration" and "move" where all possible solitaire move by numbers are enumerated
        #print(move_enumeration)
        self.action_space = spaces.Discrete(548, start=0)

        # Add Q-learning components
        self.q_table = {}
        self.learning_rate = 0.1
        self.discount_factor = 0.95
        self.epsilon = 0.1

        #set up the gaame
        self.pos = PositionClass.PositionClass()
        self.pos.setUp()
        self.reward = 0 # to keep the reward/score
        self.done = False # tell it when to stop
        #print(self.pos.gameStr())
        #print("Finished __init__")
        self.verbose = verbose
    #end __init__

    def reset(self):
        ''' resets the environment (i.e. solitaire game) and returns new initial position'''
        self.pos = PositionClass.PositionClass()
        self.pos.setUp()
        self.reward = 0 # to keep the reward/score
        self.done = False # tell it when to stop

        if self.verbose:
            print(self.pos.gameStr())
            print("reward = ", self.calculate_reward())

        return self.positionClass_to_observation()
    #end reset

    def step(self, action):
        ''' returns the result of doing an action 
        here, moving some cards around '''

        # Flag that marks the termination of an episode
        done = False
        
        # Assert that it is a valid action 
        assert self.action_space.contains(action), "Invalid Action"

        #convert action from enumeration to move-by-number
        move = self.move_enumeration["move"][action]
        print("action: ", action)
        print("move: ", move)

        try_action = self.pos.moveByNumber(move)
        if try_action == False:
            print("Move not recognised")
            done = True
            self.reward = -1000
        else:    
            print(self.pos.gameStr())
            self.reward = self.calculate_reward()

        print(self.reward)

        observation = self.positionClass_to_observation()
        reward = self.reward  # Change this line
        terminated = done
        truncated = False
        info = {} # TODO put things in print statements above into info so can choose whether to do something with them later and don't print every time

        return observation, reward, terminated, truncated, info # step must return these outputs, see https://gymnasium.farama.org/api/env/#gymnasium.Env.step
    #end step

    def positionClass_to_observation(self):
        ''' takes in variable of type positionClass which must have been set up
            and returns the matrix as per the observation space '''

        # set up return array
        ret = np.ones((13, 24), dtype=np.int32)  
        ret = ret * -2       # to set all to empty

        # put in foundations
        for i in range(4):
            for j in range(len(self.pos.foundationPiles[i].cards)):
                ret[i,j] = self.pos.foundationPiles[i].cards[j].id

        # put in stock
        for j in range(len(self.pos.stock.cards)):
            ret[4,j] = self.pos.stock.cards[j].id

        # put in waste
        for j in range(len(self.pos.waste.cards)):
            ret[5,j] = self.pos.waste.cards[j].id
        
        # put in tableau
        for i in range(7):
            for j in range(len(self.pos.tableauPiles[i].cards)):
                card = self.pos.tableauPiles[i].cards[j]
                if card.visible:
                    ret[i+6,j] = card.id
                else:
                    ret[i+6,j] = -1
        
        return ret
    #end positionClass_to_observation

    def calculate_reward(self):
        ''' takes in self and calculates reward from position
            1 point for each visible card in tableau
            5 points for each card in foundation piles
            1000 points if game won (i.e. all cards in foundation piles'''
        #ToDo do we need to have penalty here if try to do an illegal move?

        score = 0

        # check in tableau
        for i in range(7):
            for j in range(len(self.pos.tableauPiles[i].cards)):
                card = self.pos.tableauPiles[i].cards[j]
                if card.visible:
                    score += 1
        
        # check in foundation
        foundation_cards = 0
        for i in range(4):
            score += len(self.pos.foundationPiles[i].cards) * 5
            foundation_cards += len(self.pos.foundationPiles[i].cards)

        # if game won
        if foundation_cards == 52:
            score = 1000
        
        return score
    #end calculate_reward

    def get_state(self):
        # Convert the current game state to a hashable representation
        return tuple(map(tuple, self.positionClass_to_observation()))

    def get_action(self, state):
        if np.random.random() < self.epsilon:
            return self.action_space.sample()
        else:
            if state not in self.q_table:
                self.q_table[state] = np.zeros(self.action_space.n)
            return np.argmax(self.q_table[state])

    def update_q_table(self, state, action, reward, next_state):
        if state not in self.q_table:
            self.q_table[state] = np.zeros(self.action_space.n)
        if next_state not in self.q_table:
            self.q_table[next_state] = np.zeros(self.action_space.n)

        current_q = self.q_table[state][action]
        max_next_q = np.max(self.q_table[next_state])
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_next_q - current_q)
        self.q_table[state][action] = new_q

    def train(self, num_episodes):
        original_stdout = sys.stdout
        sys.stdout = io.StringIO()  # Redirect stdout to a string buffer

        for episode in range(num_episodes):
            state = self.get_state()
            total_reward = 0
            done = False

            while not done:
                action = self.get_action(state)
                observation, reward, terminated, truncated, _ = self.step(action)
                next_state = self.get_state()
                total_reward = reward

                self.update_q_table(state, action, reward, next_state)

                state = next_state
                done = terminated or truncated

            if episode % 100 == 0:
                sys.stdout = original_stdout  # Temporarily restore stdout
                print(f"Episode {episode}, Total Reward: {total_reward}")
                sys.stdout = io.StringIO()  # Redirect stdout back to string buffer

            self.reset()

        sys.stdout = original_stdout  # Restore stdout
        print("Training completed.")

    def save_model(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)
        print(f"Model saved to {filename}")

    def load_model(self, filename):
        with open(filename, 'rb') as f:
            self.q_table = pickle.load(f)
        print(f"Model loaded from {filename}")
#end OpenAiGymSolitaireClass

if __name__ == "__main__":

    ############################################################################################
    # Try random actions
    ############################################################################################


    # env = OpenAiGymSolitaireClass()
    # print(env.reset())

    # while True:
    #     # Take a random action
    #     action = env.action_space.sample()
    #     obs, reward, terminated, truncated, info = env.step(action)
        
        
    #     if (terminated == True) or (truncated == True):
    #         break
    # env.close()

    # testing spaces
    #x = spaces.Box(low=-2, high=51, shape=(13, 24), dtype=np.int32) 
    #print(x.sample())                        

    #x = spaces.Discrete(2,start=0)
    #print(x.sample())    

    ############################################################################################
    # Training code
    ############################################################################################

    # Train the model
    env = OpenAiGymSolitaireClass()
    env.train(num_episodes=100000)

    # Save the trained model
    env.save_model("solitaire_model.pkl")

    # Test the trained agent
    state = env.reset()
    state = env.get_state()
    total_reward = 0
    done = False

    while not done:
        action = env.get_action(state)
        observation, reward, terminated, truncated, _ = env.step(action)
        next_state = env.get_state()
        total_reward = reward

        state = next_state
        done = terminated or truncated

    print(f"Test game completed. Total Reward: {total_reward}")
    env.close()

# End if __name__ == "__main__":                    

