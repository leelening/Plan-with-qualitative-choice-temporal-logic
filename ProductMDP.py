# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import MDP
from WDFA import *
import copy
import numpy as np

def product_mdp(mdp, wdfa):
    """

    :param mdp:
    :param wdfa:
    :return: the product between MDP and the weighted DFA, and the reward function
    """
    pmdp = MDP.MDP()
    q_init = wdfa.transitions[wdfa.initial_state][mdp.L[mdp.init]]
    init = (mdp.init, q_init)
    pmdp.states = []
    # construct the product MDP states, the sink states in the automaton will not be added.
    for s in mdp.states:
        for q in wdfa.states:
            if q != 'sink':
                pmdp.states.append((s,q))
    pmdp.actlist = copy.deepcopy(mdp.actlist)
    N = len(pmdp.states)
    # N is the number of nonsink states. the transition function is defined for N+1 states.
    for a in pmdp.actlist:
        pmdp.prob[a] = np.zeros((N+1, N+1))
        for i in range(N):
            (s, q) = pmdp.states[i]
            for j in range(N):
                (next_s, next_q) = pmdp.states[j]
                if next_q == wdfa.transitions[q][mdp.L[next_s]]:
                    p = mdp.P(s, a, next_s)
                    pmdp.prob[a][i, j] = p
    pmdp.prob['stop'] = np.zeros((N+1, N+1))
    # adding a new action called "stop" and the new sink.
    pmdp.actlist.append('stop')
    reward = dict()
    for prod_state in pmdp.states:
        for a in pmdp.actlist:
            reward[(prod_state,a)] = 0
    options = wdfa.get_option()
    for (s,q) in pmdp.states:
        if 'end' in wdfa.transitions[q]: # from the current state q, then agent can stop and append the end symbol to the word.
            i = pmdp.states.index((s,q))
            pmdp.prob['stop'][i,N] = 1 # once the action stop is taken, then with probability one the agent reaches the sink state.
            reward[((s,q),'stop')] = options - wdfa.weight[(q,'end','sink')] + 1
    for a in pmdp.actlist:
        pmdp.prob[a][N,N] = 1
    return pmdp, reward




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
