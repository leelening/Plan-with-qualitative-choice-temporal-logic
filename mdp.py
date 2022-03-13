__author__ = "Jie Fu and Lening Li"
__email__ = "fujie@ufl.edu and lli4@wpi.edu"
__version__ = "0.0.1"
__maintainer__ = "Jie Fu and Lening Li"
__description__ = "This code defines a class of Markov Decision Process."

import numpy as np
import yaml
from collections import defaultdict
import pandas as pd
from tabulate import tabulate


class MDP(object):
    """
    A Markov Decision Process defined by
     1. an initial state,
     2. transition model --- the probability transition matrix implemented as a dictionary: prob[s][a][s'] is the probability of going from s to s' with action a,
     3. reward function.
     4. gamma value, for use by algorithms
     5. AP: a set of atomic propositions implemented as a list: Each proposition is identified by an index between 0-N.
     6. L: the labeling function implemented as a dictionary: L[s]: a subset of AP.
     7. sink: a list of terminal states
    We keep track of the possible actions for state s: prob[s].keys() and possible next states with action a: prob[s][a].keys()
    """

    def __init__(self, **kwargs):
        """If file path is not empty, initialize from the file"""
        if "file_path" in kwargs:
            # Read YAML file
            with open(kwargs["file_path"], "r") as stream:
                data_loaded = yaml.safe_load(stream)

            # directly assign the values to the variables in the yaml files besides "P"
            for key in data_loaded:
                if key != "P":
                    setattr(self, key, data_loaded[key])
            # process specifically for the transition probabilities
            self.prob = defaultdict(lambda: defaultdict(dict))
            for x in data_loaded["P"]:
                s, a, ns, p = x
                self.prob[s][a][ns] = p
            # call to validate the transition probabilities
            self.validate()
            return

        """ Empty initialization """
        self.init = kwargs.pop("init", None)
        self.actlist = kwargs.pop("actlist", [])
        self.states = kwargs.pop("states", [])
        self.gamma = kwargs.pop("gamma", 0.9)
        self.reward = kwargs.pop("reward", {})
        self.prob = kwargs.pop("prob", defaultdict)
        self.AP = kwargs.pop("AP", [])
        self.L = kwargs.pop("L", {})
        self.validate()

    def step(self, state, action, num=1):
        """Sample the next state according to the current state, the action, and the transition probability."""
        assert action in self.actlist
        assert state in self.states
        # Note that only one element is chosen from the array, which is the output by random.choice
        possible_next_states_probabilities = self.prob[state][action]
        possible_next_states = list(possible_next_states_probabilities.keys())
        nest_state = possible_next_states[
            np.random.choice(
                len(possible_next_states),
                num,
                p=list(possible_next_states_probabilities.values()),
            )[0]
        ]
        return nest_state

    def __str__(self):
        """Print the information about the defined Markov Decision Process."""
        t = {"Description": [], "Value": []}
        for attr in dir(self):
            if not callable(getattr(self, attr)) and not attr.startswith("__"):
                t["Description"].append(attr)
                t["Value"].append(getattr(self, attr))
        df = pd.DataFrame(t)
        return tabulate(df, showindex=False, headers=df.columns)

    def validate(self):
        for state in self.states:
            for action in self.prob[state]:
                try:
                    assert abs(sum(self.prob[state][action].values()) - 1) < 1e-6
                except Exception as e:
                    raise ValueError(
                        "Error: {} for state: {}, action: {}.".format(e, state, action)
                    )
