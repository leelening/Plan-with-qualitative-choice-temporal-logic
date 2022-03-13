from mip import *
from itertools import product
import pandas as pd


def LP(mdp):
    m = Model()
    v = [m.add_var(lb=0) for _ in mdp.states]

    c = [1 / len(mdp.states)] * len(mdp.states)  # state-relevance weights
    assert all(
        [x > 0] for x in c
    )  # we need state-relevance weights to be all positive.
    assert abs(sum(c) - 1) < 1e-6

    # objective function: minimize the weighted values
    m.objective = minimize(xsum(c[i] * v[i] for i, _ in enumerate(mdp.states)))

    for (i, state), action in product(enumerate(mdp.states), mdp.actlist):
        m += v[i] >= mdp.reward[state, action] + mdp.gamma * xsum(
            mdp.prob[state][action][next_state] * v[j]
            for j, next_state in enumerate(mdp.states)
            if next_state in mdp.prob[state][action]
        )

    # start solving the minimization problem
    m.max_gap = 1e-4

    status = m.optimize(max_seconds=300)
    if status == OptimizationStatus.OPTIMAL:
        print("optimal solution cost {} found".format(m.objective_value))
    elif status == OptimizationStatus.FEASIBLE:
        print(
            "sol.cost {} found, best possible: {}".format(
                m.objective_value, m.objective_bound
            )
        )
    elif status == OptimizationStatus.NO_SOLUTION_FOUND:
        print(
            "no feasible solution found, lower bound is: {}".format(m.objective_bound)
        )
    if status == OptimizationStatus.OPTIMAL or status == OptimizationStatus.FEASIBLE:
        print("Print the detailed solution ...")
        df = pd.DataFrame(
            {
                "index of state": range(len(mdp.states)),
                "state": [x for x in mdp.states],
                "value": [x.x for x in v],
            }
        )
        df["policy"] = extract_policy(mdp, [x.x for x in v])
        print(df)
    return df


def extract_policy(mdp, v):
    policy = []
    for i, state in enumerate(mdp.states):
        q = [
            mdp.reward[state, action]
            + mdp.gamma
            * sum(
                [
                    mdp.prob[state][action][next_state] * v[j]
                    for j, next_state in enumerate(mdp.states)
                    if next_state in mdp.prob[state][action]
                ]
            )
            for action in mdp.actlist
        ]
        opt_a = mdp.actlist[np.argmax(q)]
        policy.append(opt_a)
    return policy
