import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

import numpy as np


# class State(object):
#     def __init__(self, val, *args, **kwargs):
#         self.val = val
#         self.terminal = False

#     def set_terminal(self, terminal):
#         self.terminal = terminal

#     @property
#     def is_terminal(self):
#         return self.terminal

#     def __str__(self):
#         return self.state


# class Action(object):
#     def __init__(self, *args, **kwargs):
#         pass


class Policy(object):
    def __init__(self, states_space, actions_space, transit_matrix, *args, **kwargs):
        self.states_space = states_space
        self.n_states = len(self.states_space)

        self.actions_space = actions_space
        self.n_actions = len(self.actions_space)

        # self.transit_matrix = np.


    def next_action(self, s):
        # random policy
        return np.random.choice(list(range(self.n_actions)))

    def update(self, *args):
        pass


class MDP(object):
    def __init__(self, states_space, actions_space, probability_matrix, rewards, discount_factor=.9, *args, **kwargs):
        # states space
        self.states_space = states_space

        # actions space
        self.actions_space = actions_space

        # matrix
        self.probability_matrix = self._norm(probability_matrix)

        # rewards
        self.rewards = rewards

        # gamma in [0, 1]
        self.gamma = discount_factor
    
    def r(self, s, a, s_):
        """reward function r(s, a, s_)."""
        
        # simple example: if meets terminal return 1, else 0
        if self.check_states_space():
            if s_.is_terminal:
                return 1
            else:
                return 0
        else:
            raise Exception('invalid state: %s' % s_)

    def p(self, s, a):
        return 

    def v(self, s):
        """Bellman expectation equation of v_π(s).
        
        Expectation of G_t(s) using policy π, which is an accumulated G value with γ decay
        v_π(s) = E_π[ R_t+1 + γ * v_π(S_t+1) | S_t = s ]
        v_π(s) = E_π[ R_t+1 + γ * v_π(S_t+1) | S_t = s ]
        """
        # a = self.policy.next_action(s)
        # v_val = 
    
    def q(self, s, a):
        """Bellman expectation equation of q_π(s, a)."""

    def check_states_space(self, s):
        return s in self.states_space

    def check_actions_space(self, a):
        return a in self.actions_space
    
    def _norm(self, matrix):
        return matrix




if __name__ == "__main__":
    n_col, n_row = 3, 3
    states_space = ['(%d, %d)' % (i % n_col, i // n_col) for i in range(n_row * n_col)]
    actions_space = ['left', 'right', 'up', 'down']

    p_matrix = [
      # 00 10 20 01 11 21 02 12 22
        [1, 1, 0, 1, 0, 0, 0, 0, 0],    # (0, 0)
        [10, 1, 1, 0, 1, 0, 0, 0, 0],    # (1, 0)
        [0, 1, 1, 0, 0, 1, 0, 0, 0],    # (2, 0)
        [1, 0, 0, 1, 1, 0, 1, 0, 0],    # (0, 1)
        [0, 1, 0, 1, 0, 1, 0, 1, 0],    # (1, 1)
        [0, 0, 1, 0, 1, 1, 0, 0, 1],    # (2, 1)
        [0, 0, 0, 1, 0, 0, 1, 1, 0],    # (0, 2)
        [0, 0, 0, 0, 1, 0, 1, 1, 1],    # (1, 2)
        [0, 0, 0, 0, 0, 1, 0, 1, 1],    # (2, 2)
    ]
    # p_matrix = np.zeros((len(states_space), len(states_space)))
    p_matrix = np.matrix(p_matrix)
    p_matrix = p_matrix / p_matrix.mean(axis=1)

    # mdp = MDP()
    print(p_matrix)

    