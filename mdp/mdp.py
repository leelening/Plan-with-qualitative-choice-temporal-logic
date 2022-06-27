import numpy as np
import yaml
from collections import defaultdict
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

            self.transitions = self.construct_transitions()

            self.fill_labeling_func()

        else:
            for key in kwargs:
                setattr(self, key, kwargs[key])

    def construct_states(self) -> list:
        return list(
            product(range(self.grid_world_size[0]), range(self.grid_world_size[1]))
        )

    def fill_labeling_func(self):
        """
        Fullfil the labeling function
        """
        self.AP.append("end")
        labeled_states = self.L.keys()
        for s in self.states:
            if s in self.obstacles:
                self.L[s] = "o"
            elif s not in labeled_states:
                self.L[s] = "E"
            if s == "sT":
                self.L[s] = "end"

    def a_array(self, a: int) -> np.array:
        """
        Convert the int action to the array action

        :param a: int action
        """
        if a == 0:
            return np.asarray([0, 1])
        elif a == 1:
            return np.asarray([1, 0])
        elif a == 2:
            return np.asarray([0, -1])
        elif a == 3:
            return np.asarray([-1, 0])

    def deterministic_transition(self, s: tuple, a: int) -> tuple:
        """
        One step deterministic transition

        :param s: the current state
        :param a: the current action
        :return: the next deterministic state
        """
        if hasattr(self, "obstacles") and s in self.obstacles and a != "aT":
            return s
        ns = tuple(np.asarray(s) + self.a_array(a))
        return ns if ns in self.states else s

    def stochastic_transition(self, s: tuple, a: int) -> tuple:
        """
        One step stochastic transition

        :param s: the current state
        :type s: tuple
        :param a: the current state
        :type a: int
        :return: the next deterministic state
        """
        if hasattr(self, "obstacles") and s in self.obstacles and a != "aT":
            return s
        next_possible_states = list(self.transitions[s][a].keys())

        probability_distribution = [
            self.transitions[s][a][ns] for ns in next_possible_states
        ]

        try:
            index = np.random.choice(
                a=range(len(next_possible_states)), p=probability_distribution
            )
        except:
            raise ValueError(
                "s: {}, a: {}, P: {}".format(s, a, probability_distribution)
            )
        return next_possible_states[index]

    def construct_transitions(
        self,
    ) -> defaultdict:
        """
        Construct the probabilistic transition function

        :return: the transition probability matrix of the mdp
        """
        transitions = defaultdict(lambda: defaultdict(dict))

        for s, a in product(self.states, self.actions):
            n_d_s = self.deterministic_transition(s, a)
            if s in self.obstacles:
                if n_d_s == s:
                    transitions[s][a][s] = 1
                else:
                    transitions[s][a][s] = self.stuck_prob
                    transitions[s][a][n_d_s] = 1 - self.stuck_prob
            else:
                neighbors = self.neighbors(s, a)

                sum_prob = 0
                for ns in neighbors:
                    if ns != n_d_s:
                        transitions[s][a][ns] = self.randomness
                        sum_prob += self.randomness
                transitions[s][a][n_d_s] = 1 - sum_prob
        if "sT" not in self.states:
            self.states.append("sT")
        if "aT" not in self.actions:
            self.actions.append("aT")

        for a in self.actions:
            transitions["sT"][a]["sT"] = 1

        for s in self.states:
            transitions[s]["aT"]["sT"] = 1

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

    def transition_matrix_str(self, fmt: str):
        """
        Return the transition matrix of the MDP given the format

        :return: the readable transition matrix of the mdp
        :rtype: str
        """
        data = []
        for s in self.transitions:
            for a in self.transitions[s]:
                for ns in self.transitions[s][a]:
                    data.append([s, a, ns, self.transitions[s][a][ns]])
        return tabulate(data, headers=["s", "a", "ns", "p"], tablefmt=fmt)

    def adjust_randomness(self, randomness: float) -> None:
        """
        Adjust the randomness of the MDP givne the randomness

        :param randomness: the randomness in the transition probablity
        """
        self.randomness = randomness
        self.states.remove("sT")
        self.actions.remove("aT")
        self.transitions = self.construct_transitions()

    def __str__(self, fmt="presto"):
        data = [
            ["S", self.states],
            ["A", self.actions],
            ["P", self.transition_matrix_str(fmt)],
            ["AP", self.AP],
        ]
        if hasattr(self, "reward"):
            data.append(["r", self.reward])
        return tabulate(data, headers=["Variable", "Value"], tablefmt=fmt)
