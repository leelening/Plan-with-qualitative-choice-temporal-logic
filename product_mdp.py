__authors__ = ["Jie Fu", "Lening Li"]
__emails__ = ["fujie@ufl.edu", "lli4@wpi.edu"]
__copyright__ = "Copyright 2022, The Qualitative Logic + Temporal Logic Project"
__date__ = "2022-03-12"
__license__ = "GPL"
__version__ = "0.0.1"
__description__ = "the code implementations a product Markov Decision Process"
__status__ = "Production"

from mdp import MDP
from WDFA import *
import copy


class ProductMDP(MDP):
    """
    A product Markov Decision Process inherited from base case Markov Decision Process."
    """

    def __init__(self, mdp, wdfa):
        """
        Initialization
        :param mdp:
        :param wdfa:
        """
        self._mdp = mdp
        self._wdfa = wdfa

        # the initial state of the product mdp
        init = (
            mdp.init,
            self._wdfa.transitions[wdfa.initial_state][mdp.L[mdp.init]],
        )
        # construct the product MDP states, the sink states in the automaton will not be added.
        states = {
            (s, q)
            for (s, q) in product(self._mdp.states, self._wdfa.states)
            if q != "sink"
        }

        # add a new action into the action list. Note: later a stop action will be added into the actlist.
        actlist = copy.deepcopy(mdp.actlist)

        prob, reward, actlist = self.initialize_transitions_reward(states, actlist)

        super(ProductMDP, self).__init__(
            init=init,
            actlist=actlist,
            states=states,
            reward=reward,
            prob=prob,
            AP=mdp.AP,
            L=mdp.L,
        )

    def initialize_transitions_reward(self, states, actlist):
        prob, reward = defaultdict(lambda: defaultdict(dict)), defaultdict(float)
        N = len(states)

        # N is the number of nonsink states. the transition function is defined for N+1 states.
        for (i, (s, q)), a, (j, (next_s, next_q)) in product(
            enumerate(states), actlist, enumerate(states)
        ):
            if next_s in self._mdp.prob[s][a]:
                if next_q == self._wdfa.transitions[q][self._mdp.L[next_s]]:
                    prob[i][a][j] = self._mdp.prob[s][a][next_s]

        # adding a new action called "stop" and the new sink.
        actlist.append("stop")

        options = self._wdfa.get_option()
        for i, (s, q) in enumerate(states):
            # from the current state q, then agent can stop and append the end symbol to the word.
            if "end" in self._wdfa.transitions[q] and "sink" == self._wdfa.transitions[q]["end"]:
                # once the action stop is taken, then with probability one the agent reaches the sink state.
                prob[i]["stop"][N] = 1
                reward[i, "stop"] = (
                    options - self._wdfa.weight[q, "end", "sink"] + 1
                )
        for a in actlist:
            prob[N][a][N] = 1
        return prob, reward, actlist
