from itertools import product
from collections import defaultdict

from mdp import MDP


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

        prob, reward = self.initialize_transitions_reward(states, mdp.actlist)

        super(ProductMDP, self).__init__(
            init=init,
            actlist=mdp.actlist,
            states=states,
            gamma=mdp.gamma,
            reward=reward,
            prob=prob,
            AP=mdp.AP,
            L=mdp.L,
        )

    def construct_reward(self, states, actlist):
        reward = defaultdict(float)

        for (s, q), a in product(states, actlist):
            if (a == "aT") and (q != "sink") and (self.weight[q, "end", "sink"] > 0):
                reward[(s, q), a] = (
                    self._wdfa.opt - self._wdfa.weight[q, "end", "sink"] + 1
                )
        return reward

    def construct_transitions(self, states, actlist):
        prob = defaultdict(lambda: defaultdict(dict))

        # N is the number of nonsink states. the transition function is defined for N+1 states.
        for (s, q), a, (ns, nq) in product(states, actlist, states):
            if nq in self._mdp.prob[s][a]:
                prob[s, q][a][ns, nq] = self._mdp.prob[s][a][ns] * (
                    nq == self._wdfa.transitions[q][self._mdp.L[ns]]
                )

        return prob
