from itertools import product
import copy


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

        # add a new action into the action list. Note: later a stop action will be added into the actlist.
        actlist = copy.deepcopy(mdp.actlist)

        prob, reward, actlist = self.initialize_transitions_reward(states, actlist)

        super(ProductMDP, self).__init__(
            init=init,
            actlist=actlist,
            states=states,
            gamma=mdp.gamma,
            reward=reward,
            prob=prob,
            AP=mdp.AP,
            L=mdp.L,
        )

    def initialize_transitions_reward(self, states, actlist):
        prob, reward = defaultdict(lambda: defaultdict(dict)), defaultdict(float)

        # N is the number of nonsink states. the transition function is defined for N+1 states.
        for (s, q), a, (next_s, next_q) in product(states, actlist, states):
            if next_s in self._mdp.prob[s][a]:
                if next_q == self._wdfa.transitions[q][self._mdp.L[next_s]]:
                    prob[s, q][a][next_s, next_q] = self._mdp.prob[s][a][next_s]

        options = self._wdfa.get_option()
        for s, q in states:
            # from the current state q, then agent can stop and append the end symbol to the word.
            if (
                "end" in self._wdfa.transitions[q]
                and "sink" == self._wdfa.transitions[q]["end"]
            ):
                # once the action stop is taken, then with probability one the agent reaches the sink state.
                prob[s, q]["stop"]["v_sink"] = 1
                reward[(s, q), "stop"] = (
                    options - self._wdfa.weight[q, "end", "sink"] + 1
                )
        # adding a new action called "stop" and the new sink.
        actlist.append("stop")
        states.add("v_sink")
        for a in actlist:
            prob["v_sink"][a]["v_sink"] = 1
        return prob, reward, actlist
