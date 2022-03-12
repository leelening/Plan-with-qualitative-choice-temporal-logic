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
        m += v[i] >= mdp.reward[i, action] + mdp.gamma * xsum(
            mdp.prob[i][action][j] * v[j]
            for j, _ in enumerate(mdp.states)
            if j in mdp.prob[i][action]
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
        print(df)
