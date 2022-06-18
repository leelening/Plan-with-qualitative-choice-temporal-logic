from itertools import product

from common import *
from paras import PARA


class Robot:
    def __init__(self):
        self.obstacles = PARA.obstacles  # one type of sink states for agent MDP
        self.targets = PARA.targets  # sink states for robot
        self.randomness = PARA.randomness  # randomness for robot

        self.state_space = list(product(range(PARA.grid_size), repeat=2))  # state space for robot
        self.state_size = len(self.state_space)  # state space size

        self.action_space = list(PARA.action_space.keys())  # action space for robot
        self.action_size = len(self.action_space)  # add action size.

        self.initial_state = PARA.initial_state  # robot initial

        self.gamma = PARA.gamma  # discounting factor

        # probabilistic transition function for robot
        self.transitions = self.init_transitions(self.state_space, self.action_space, self.obstacles, self.targets,
                                                 self.randomness)

    def clean_sink_states(self):
        """
        Call when we need to construct the robot
        :return: None
        """
        self.obstacles = set()  # remove obstacles
        self.targets = set()  # remove targets
        self.transitions = dict()  # delete the transitions
        # re-initialize the transition function
        self.init_transitions(self.state_space, self.action_space, self.obstacles, self.targets, self.randomness)

    @staticmethod
    def get_opposite_action(a):
        """
        This function return an opposition a given a
        :param a: (str)
        :return: (str)
        """
        if a == "S":
            return "N"
        elif a == "N":
            return "S"
        elif a == "W":
            return "E"
        elif a == "E":
            return "W"

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

    def init_transitions(self, state_space, action_space, obstacles, target, randomness):
        """
        This function initializes the probabilistic transition function
        :param state_space: (list)
        :param action_space: (list)
        :param obstacles: (set)
        :param target: (set)
        :param randomness: (float)
        :return: (dict)
        """
        transitions = dict()
        for s, a in product(state_space, action_space):
            if s in obstacles or s in target:  # if it is in the obstacles and target, it would not come out again
                transitions = put_into_dict3(transitions, s, a, s, 1.0)
            else:
                neighbors = self.possible_neighbors(s, a, action_space)
                n_d_s = self.deterministic_transition(s, PARA.action_space[a])  # the cell supposed to reach
                major_prob = randomness  # the major probability
                minor_prob = round((1 - major_prob) / (len(neighbors) - 1),
                                   2)  # the minor probability is calculated based on the possible neighbors

                for next_state in neighbors:
                    if next_state == n_d_s and next_state in state_space:  # if the agent reaches a cell supposed to reach and the cell is within the world
                        transitions = put_into_dict3(transitions, s, a, next_state, major_prob)
                    elif next_state == n_d_s and next_state not in state_space:  # if the agent reaches a cell supposed to reach and the cell is not in the world
                        if s in transitions and a in transitions[s] and s in \
                                transitions[s][a]:  # if the transition has been initialized, then we need to add on it.
                            transitions[s][a][s] += major_prob
                        else:
                            transitions = put_into_dict3(transitions, s, a, s, major_prob)
                    elif next_state != n_d_s and next_state in state_space:  # if the agent reaches a cell not supposed to reach and the cell is within the world
                        transitions = put_into_dict3(transitions, s, a, next_state, minor_prob)
                    elif next_state != n_d_s and next_state not in state_space:  # if the agent reaches a cell not supposed to reach and the cell is not in the world
                        if s in transitions and a in transitions[s] and s in \
                                transitions[s][a]:  # if the transition has been initialized, then we need to add on it.
                            transitions[s][a][s] += minor_prob
                        else:
                            transitions = put_into_dict3(transitions, s, a, s, minor_prob)
        return transitions

    def possible_neighbors(self, s, a, action_space):
        """
        This function returns the possible neighbors besides the opposite direction of the neighbors.
        :param s: (tuple)
        :param a: (str)
        :param action_space: (list)
        :return: set()
        """
        neighbors = set()
        opposite_action = self.get_opposite_action(a)  # get the opposite a
        possible_actions = set(action_space).difference({opposite_action})
        for key in possible_actions:
            neighbors.add(self.deterministic_transition(s, PARA.action_space[key]))
        return neighbors

    def __str__(self):
        """
        This function checks the correctness of the transitions
        :return: None
        """
        tmp = '------------------------- The transition matrix of the robot ----------------------------\n'
        for s in self.transitions:
            for a in self.transitions[s]:
                temp = list()
                for ns in self.transitions[s][a]:
                    p = self.transitions[s][a][ns]
                    temp.append(p)
                    tmp += str(s).ljust(30) + str(a).ljust(30) + str(ns).ljust(30) + str(p) + '\n'

                assert abs(sum(temp) - 1) <= 1e-7  # the summation of probabilities of reaching next states is 1
            tmp += '------------------------------------------------------------------------------\n'
        tmp += 'Robot state space size:'.ljust(30) + str(self.state_size)
        return tmp


if __name__ == '__main__':
    robot_mdp = Robot()
    print(robot_mdp)