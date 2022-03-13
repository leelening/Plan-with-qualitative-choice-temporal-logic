__authors__ = ["Jie Fu", "Lening Li"]
__emails__ = ["fujie@ufl.edu", "lli4@wpi.edu"]
__copyright__ = "Copyright 2022, The Qualitative Logic + Temporal Logic Project"
__date__ = "2022-03-12"

__license__ = "GPL"
__version__ = "0.0.1"
__description__ = "This code defines a class of Markov Decision Process."
__status__ = "Production"

import numpy as np
import yaml
from collections import defaultdict
import pandas as pd
from tabulate import tabulate
from pprint import pformat


class MDP(object):
    """
    A Markov Decision Process defined by
     1. an initial state,
     2. transition model --- the probability transition matrix implemented as a dictionary: prob[s][a][s'] is the probability of going from s to s' with action a,
     3. reward function.
     4. gamma value, for use by algorithms
     5. AP: a set of atomic propositions implemented as a list: Each proposition is identified by an index between 0-N.
     6. L: the labeling function implemented as a dictionary: L[s]: a subset of AP.
     7. obstacles: a list of terminal states
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
        self.obstacles = kwargs.pop("obstacles", [])
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

    def get_mdp_info(self):
        """Print the information about the defined Markov Decision Process."""
        t = {"Description": [], "Value": []}
        for attr in dir(self):
            if not callable(getattr(self, attr)) and not attr.startswith("__"):
                t["Description"].append(attr)
                if isinstance(getattr(self, attr), defaultdict):
                    t["Value"].append(pformat(dict(getattr(self, attr))))
                else:
                    t["Value"].append(pformat(getattr(self, attr)))

        df = pd.DataFrame(t)
        return df

    def __str__(self):
        """return a string of MDP information."""
        df = self.get_mdp_info()
        return tabulate(df, showindex=False, headers=df.columns)

    def save(self):
        """save the MDP information."""
        df = self.get_mdp_info()
        df.to_csv("{}.csv".format(type(self).__name__))

    def validate(self):
        for state in self.states:
            possible_next_states = set()
            for action in self.prob[state]:
                possible_next_states.update(set(self.prob[state][action].keys()))

                # check if the sum of probabilities is equal to 1
                try:
                    assert abs(sum(self.prob[state][action].values()) - 1) < 1e-6
                except AssertionError:
                    raise AssertionError(
                        "Error in transition probability for state: {}, action: {}.".format(
                            state, action
                        )
                    )

                # check if the obstacles are valid
                if state in self.obstacles:
                    try:
                        assert abs(self.prob[state][action][state] - 1) < 1e-6
                    except AssertionError:
                        raise AssertionError(
                            "Error in obstacles for state: {}, action: {}.".format(
                                state, action
                            )
                        )

            # check if the state not in obstacles should go out. NOTE that product mdp does not have obstacles, so we
            # add len(self.obstacles) > 0 into the condition
            if state not in self.obstacles and len(self.obstacles) > 0:
                possible_next_states = list(possible_next_states)
                try:
                    assert not possible_next_states.count(
                        possible_next_states[0]
                    ) == len(possible_next_states)
                except AssertionError:
                    raise AssertionError(
                        "Error in transition probability for state: {}, possible next states: {}."
                        "Any state not in obstacles should go out of itself.".format(
                            state, possible_next_states
                        )
                    )
