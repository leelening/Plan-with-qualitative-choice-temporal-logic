__author__ = 'Jie Fu, jief@seas.upenn.edu'

from MDP import *
import numpy as np
import random
import copy


def value_iter(mdp, reward):
    """
    :param mdp: a MDP
    :param reward: a reward function over state-action pair
    :return: the policy and the optimal value function
    """
    policyT = {s: None for s in mdp.states} # initialize the policy to take None for every state
    Vstate1 = {s: 0 for s in mdp.states} # initialize to zero.
    epsilon = 0.005
    Q = dict([])
    t=0
    while True:
        t= t+1
        Vstate = copy.deepcopy(Vstate1) # remember the value in the previous iteration.
        for s in set(mdp.states):
            acts = mdp.actions(s)
            optimal = 0
            act = None
            for a in mdp.actions(s):
                Q[(s, a)] = reward[(s,a)] + sum([mdp.P(s, a, next_s) * Vstate[next_s] for next_s in mdp.states])
                if Q[(s, a)] >= optimal:
                    optimal = Q[(s, a)]
                    act = a
                else:
                    pass
            Vstate1[s] = optimal
            policyT[s] = act
        print ("iteration: {} and the state value is {}".format(t, Vstate1))
        if maxdiff(Vstate, Vstate1) < epsilon:
            break
    return Vstate1, policyT

def maxdiff(v_old, v_new):
    d = 0
    for key in v_old.keys():
        temp = v_new[key] -v_old[key]
        if temp > d:
            d = temp
    return d

def best_policy(mdp,AEC=None):
    """
    For a given state in MDP, output the probability of hitting the set of accepting end component eventually as the state value.
    """
    U=dict([]) # define a map from a set of states into a set of variables.
    problem=LpProblem("MDP SOLVER", LpMinimize)
    #firstly we need to define a set of variables, which is the state value U(q)
    for state in mdp.states:
        U[state] = LpVariable("U"+str(state),0) # for each state, assign a state value variable.
    problem += LpAffineExpression([(U[state], 1) for state in mdp.states])
    # The state-value of a state in the AEC is 1.
    if AEC == None:
        Win, policy1=win_lose(mdp)
    else:
        Win=AEC[0]
        policy1=AEC[1]
    for state in Win:
        problem += U[state]==1
    ###Need to add the set of sink states. Todo!!
    ###
    for state in mdp.states:
        for act in mdp.actions(state):
            C=LpAffineExpression([(U[next_state], mdp.P(state,act,next_state)) for next_state in mdp.states])
            problem+= U[state]-C >=0
    status = problem.solve()
    policy2=dict([])
    # compute the state-action value for each state-action pair
    Q=dict([])
    V=dict([])
    for state in Win:
        V[state]=1
    for state in set(mdp.states)-Win: 
        optimal=0
        act=None                        
        V[state]=U[state].varValue 
        for act in mdp.actions(state):
            Q[(state,act)]= np.inner(mdp.T(state,act), np.array([U[next_state].varValue for next_state in mdp.states]))
            if Q[(state,act)] >= optimal:
                optimal=Q[(state,act)]
                act=act
            else:
                pass
        policy2[state]=act
    policy1.update(policy2)
    # print "The policy 2 is "+str(policy2)
    return policy1, Q, V # the system will switch between policy1 and 2. When the state is within AEC, policy 1 will be taken, otherwise policy2 will be taken.


def T_step_value_iter(mdp,T,AEC=None):
    """
    T- finite time horizon
    Value iteration: Vstate[s] the maximal probability of hitting the target AEC within T steps. 
    """
    policyT=dict([])
    Vstate1=dict([])
    if AEC == None:
        Win,policy= win_lose(mdp)
    else:
        Win=AEC[0]
        policy=AEC[1]
    policyT.update(policy)
    NAEC=set(mdp.states)-Win
    Vstate1.update({s: 1 for s in list(Win)})
    Vstate1.update({s: 0 for s in list(NAEC)})

    if NAEC ==  set([]):
        return Vstate1, policyT
    t=T
    Q=dict([])
    while t>0:
        Vstate = Vstate1.copy()
        for s in set(mdp.states)-Win:
            acts=mdp.actions(s)
            optimal=0
            act=None
            for a in mdp.actions(s):
                Q[(s,a)]= sum([mdp.P(s,a,next_s)* Vstate[next_s] for next_s in mdp.states])
                #Q[(s,a)]= np.inner(mdp.T(s,a), Vstate)
                if Q[(s,a)] >=optimal:
                    optimal=Q[(s,a)]
                    act=a
                else:
                    pass
            Vstate1[s]=optimal
            policyT[s]= act
            #        print "iteration: {} and the state value is {}".format(t, Vstate1)
        t=t-1
    return Vstate1,policyT

def E_state_value_iter(mdp,epsilon, AEC=None):
    """
    Value iteration: Vstate[s] the maximal probability of hitting the
    target AEC.  Iteration terminates when the change in the state
    value cannot be improved by at least epsilon.  return: state
    values, policy and the number of iterations.
    """
    policyE=dict([])
    Vstate1=dict([])

    if AEC == None:
        Win,policy= win_lose(mdp)
    else:
        Win=AEC[0]
        policy=AEC[1]
    policyE.update(policy)
    N=len(mdp.states)
    t=0
    NAEC=set(mdp.states)-Win

    Vstate1.update({s: 1 for s in list(Win)})
    Vstate1.update({s: 0 for s in list(NAEC)})

    if NAEC ==  set([]):
        return Vstate1, policy

    Q=dict([])
    e=1.0
    while e > epsilon:
        t=t+1
        Vstate = Vstate1.copy()
        for s in set(mdp.states)-Win:
            acts=mdp.actions(s)
            optimal=0
            act=None
            for a in mdp.actlist:
                Q[(s,a)]= sum([mdp.P(s,a,next_s)* Vstate[next_s] for next_s in mdp.states])
                #                Q[(s,a)]= np.inner(mdp.T(s,a), Vstate)
                if Q[(s,a)] >=optimal:
                    optimal=Q[(s,a)]
                    act=a
                else:
                    pass
            Vstate1[s]=optimal
            policyE[s]= act
            #        print "iteration: {} and the state value is {}".format(t, Vstate1)
            e= abs( max([Vstate1[s] - Vstate[s] for s in mdp.states])) # the absolute error
    return Vstate1,policyE,t

def evaluate_policy2(mdp,policy,AEC):
    U=dict([]) # define a map from a set of states into a set of variables.
    problem=LpProblem("MDP SOLVER", LpMinimize)
    #firstly we need to define a set of variables, which is the state value U(q)
    for state in mdp.states:
        U[state] = LpVariable("U"+str(state),0) # for each state, assign a state value variable.
    problem += LpAffineExpression([(U[state], 1) for state in mdp.states])
    # The state-value of a state in the AEC is 1.
    policyE=dict([])
    Vstate1={}
    Win=AEC[0]
    policyE.update(AEC[1])
    Vstate1.update({s: 1 for s in list(AEC[0])})
    for state in Win.intersection(mdp.states):
        problem += U[state]==1
    for state in mdp.states:
        act=policy[state]
        C=LpAffineExpression([(U[next_state], mdp.P(state,act,next_state)) for next_state in mdp.states])
        problem+= U[state]-C ==0
    status = problem.solve()
    value={state: U[state].varValue for state in mdp.states}
    return value


def evaluate_policy_T(mdp,policy,T):
    V=dict([])
    AEC,policy2=get_AEC(mdp)
    for s in AEC:
        V[s]=1
    for s in set(mdp.states)-AEC:
        V[s]=0
    t=T
    while t>0:
        for s in set(mdp.states)-AEC:
            a= policy[s]
            V[s]= sum([mdp.P(s,a,next_s)* V[next_s] for next_s in mdp.states])  
        t=t-1
    return V
    
def balanced_wandering(mdp,s):
    act=random.choice(list(mdp.actions(s))) # randomly choose an action from the set of enabled actions.
    next_s=mdp.sample(s,act)
    return next_s,act

def exploit(mdp,s,policyT):
    act=policyT[s]
    next_s=mdp.sample(s,act)
    return next_s,act
    

"""
Test the code for computing the accepting end component.

if __name__=='__main__':    
    nfa = NFA()
    nfa.add_transition('a', 1, [2])
    nfa.add_transition('b', 1, [3])
    nfa.add_transition('b', 2, [2,3])
    nfa.add_transition('a', 3, [2,3])
    nfa.add_transition('a',2,[1,3])
    nfa.add_transition('b', 3, [3])
    F=set([3])
    AEC,policy=get_AEC(nfa, F)

"""

"""
Test the code for MDP policy computation.
"""
if __name__=='__main__':
    ex=read_from_file_MDP(ex.txt)
    ex.init=0
    translist=dict([])
    translist[(0,a)]=[(1,1)]
    

