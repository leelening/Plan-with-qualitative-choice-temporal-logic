from itertools import product
from collections import defaultdict

from mdp.mdp import MDP
from wdfa.wdfa import WDFA


class ProductMDP(MDP):
    """
    A product Markov Decision Process inherited from base case Markov Decision Process."
    """

    def __init__(self, mdp: MDP, wdfa: WDFA):
        """
        Initialization

        :param mdp: the label Markov Decision Process
        :param wdfa: the weighed deterministic finite state automaton
        """
        self._mdp = mdp
        self._wdfa = wdfa

        init = (
            mdp.init,
            self._wdfa.transitions[wdfa.initial_state][mdp.L[mdp.init]],
        )

        states = {
            (s, q)
            for (s, q) in product(self._mdp.states, self._wdfa.states)
            if q != "sink"
        }

        transitions = self.construct_transitions(states, mdp.actlist)

        reward = self.construct_rewards(states, mdp.actlist)

        super(ProductMDP, self).__init__(
            init=init,
            actlist=mdp.actlist,
            states=states,
            gamma=mdp.gamma,
            reward=reward,
            transitions=transitions,
            AP=mdp.AP,
            L=mdp.L,
        )

    def construct_rewards(self, states: list, actlist: list) -> defaultdict:
        reward = defaultdict(float)
        for (s, q), a in product(states, actlist):
            if (
                (a == "aT")
                and (q != "sink")
                and (self._wdfa.weight[q, "end", "sink"] > 0)
            ):
                reward[(s, q), a] = (
                    self._wdfa.opt - self._wdfa.weight[q, "end", "sink"] + 1
                )
        return reward

    def construct_transitions(self, states: list, actlist: list) -> defaultdict:
        transitions = defaultdict(lambda: defaultdict(dict))

        for (s, q), a, (ns, nq) in product(states, actlist, states):
            if nq in self._mdp.transitions[s][a]:
                transitions[s, q][a][ns, nq] = self._mdp.transitions[s][a][ns] * (
                    nq == self._wdfa.transitions[q][self._mdp.L[ns]]
                )

        return transitions
