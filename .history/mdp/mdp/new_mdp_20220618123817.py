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
from itertools import product
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
     7. obstacles: a list of terminal states
    We keep track of the possible actions for state s: prob[s].keys() and possible next states with action a: prob[s][a].keys()
    """

    def __init__(self, **kwargs):
        if "file_path" in kwargs:
            with open(kwargs["file_path"], "r") as stream:
                data_loaded = yaml.load(stream, Loader=yaml.FullLoader)

            for key in data_loaded:
                setattr(self, key, data_loaded[key])

            self.states = self.construct_states()

            self.fill_labeling_func()

            self.transitions = self.construct_transitions()
            return

    def construct_states(self) -> list:
        return list(
            product(range(self.grid_world_size[0]), range(self.grid_world_size[1]))
        )

    def fill_labeling_func(self):
        labeled_states = self.L.keys()
        for s in self.states:
            if s in self.obstacles:
                self.L[s] = "o"
            elif s not in labeled_states:
                self.L[s] = "e"

    @staticmethod
    def deterministic_transition(s, a):
        """
        This function computes the cell supposed to reach
        :param s: (tuple)
        :param a: (tuple)
        :return: (tuple)
        """
        next_state = tuple(map(lambda x, y: x + y, s, a))
        return next_state

    def construct_transitions(
        self,
    ) -> defaultdict:
        """
        This function initializes the probabilistic transition function

        :return: (dict)
        """
        transitions = defaultdict(lambda: defaultdict(dict))

        for s, a in product(self.states, self.actlist):
            if s in self.obstacles:
                transitions[s][a][s] = 1
            else:
                neighbors = self.neighbors(s, a)
                n_d_s = self.deterministic_transition(s, a)
                
                minor_prob = round((1 - self.randomness) / (len(neighbors) - 1), 2)

                sum_prob = 0
                for ns in neighbors:
                    if ns != n_d_s:
                        transitions[s][a][ns] = minor_prob
                transitions[s][a][n_d_s] = 1 - 
                    
        return transitions

    def neighbors(self, s: tuple, a: int) -> set:
        """
        Returns the possible neighbors within grid world.

        :param s: the current state
        :param a: the current action
        :return: the set of neighbors within the grid world.
        """
        s = np.asarray(s)
        if a == 0:
            neighbors = [
                s + np.array([0, 1]),
                s + np.array([-1, 0]),
                s + np.array([1, 0]),
            ]
        elif a == 1:
            neighbors = [
                s + np.array([1, 0]),
                s + np.array([0, 1]),
                s + np.array([0, -1]),
            ]
        elif a == 2:
            neighbors = [
                s + np.array([0, -1]),
                s + np.array([-1, 0]),
                s + np.array([1, 0]),
            ]
        else:
            neighbors = [
                s + np.array([-1, 0]),
                s + np.array([0, 1]),
                s + np.array([0, -1]),
            ]
        neighbors_set = set(
            [tuple(x) if tuple(x) in self.states else tuple(s) for x in neighbors]
        )
        return neighbors_set

    def transition_matrix_str(
        self,
    ):
        """
        Return human-read-friendly transition matrix of the MDP

        :return: the readable transition matrix of the mdp
        :rtype: str
        """
        data = []
        for s in self.transitions:
            for a in self.transitions[s]:
                for ns in self.transitions[s][a]:
                    data.append([s, a, ns, self.transitions[s][a][ns]])
        return tabulate(data, headers=["s", "a", "ns", "p"])
