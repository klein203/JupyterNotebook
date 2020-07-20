from mdp import MarkovDecisionProcess


class ValueIterationAgent(object):
    def __init__(mdp):
        self.threshold = 1e-5
