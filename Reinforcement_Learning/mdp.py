import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

import numpy as np


class MarkovDecisionProcess(object):
    def __init__(self, states_space, actions_space, p_matrix, r_matrix, discount_factor=0.9):
        self.states_space = states_space
        self.actions_space = actions_space
        self.p_matrix = p_matrix
        self.r_matrix = r_matrix
        self.discount_factor = discount_factor

    def get_states_space(self):
        """
        () -> []
        return list of all states
        """
        logging.DEBUG('states space: %s' % self.states_space)
        return self.states_space

    def get_actions_space(self):
        """
        () -> []
        return list of all actions
        """
        logging.DEBUG('actions space: %s' % self.actions_space)
        return self.actions_space

    def get_possible_actions(self, state):
        """
        (s) -> []
        """
        logging.DEBUG('possible actions: %s' % self.actions_space)
        return self.actions_space

    def get_reward(self, state, action, next_state):
        """
        (s, a, s_) -> r
        """
        pass

    def get_discount_factor(self):
        """
        () -> discount_factor
        return discount_factor
        """
        return self.discount_factor
    
    def is_terminal(self, state):
        """
        (state) -> bool
        """
        return state == self.states_space[-1]


if __name__ == "__main__":
    states_space = ['S%d' % i for i in range(1, 6)]
    actions_space = ['Facebook', 'Quit', 'Sleep', 'Study', 'Pub']

    p_matrix = np.matrix([
        [.5, .5, .0, .0, .0],
        [.5, .0, .5, .0, .0],
        [.0, .0, .0, .5, .5],
        [.0, .1, .2, .2, .5],
        [.0, .0, .0, .0, .0],
    ])

    r_matrix = np.matrix([
        [-0.5],
        [-1.5],
        [-1.0],
        [ 5.5],
        [ 0.0],
    ])

    mdp = MarkovDecisionProcess(states_space, actions_space, p_matrix, r_matrix, discount_factor=1)

