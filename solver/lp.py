from mip import Model, minimize, xsum, OptimizationStatus
from itertools import product
from collections import defaultdict
import numpy as np


class LPSolver(object):
    def __init__(self, mdp, max_gap=1e-4, max_seconds=300):
        self.mdp = mdp
        self.max_gap = max_gap
        self.max_seconds = max_seconds

        self.m = Model()
        self.v = [self.m.add_var(lb=0) for _ in self.mdp.states]

        self.policy = defaultdict(int)
        self.value = defaultdict(float)

    def state_relevance_weights(self):
        return [1 / len(self.mdp.states)] * len(self.mdp.states)

    def solve(self):
        c = self.state_relevance_weights()

        # objective function: minimize the weighted values
        self.m.objective = minimize(
            xsum(c[i] * self.v[i] for i, _ in enumerate(self.mdp.states))
        )

        for (i, state), action in product(enumerate(self.mdp.states), self.mdp.actlist):
            self.m += self.v[i] >= self.mdp.reward[
                state, action
            ] + self.mdp.gamma * xsum(
                self.mdp.transitions[state][action][next_state] * self.v[j]
                for j, next_state in enumerate(self.mdp.states)
                if next_state in self.mdp.transitions[state][action]
            )

        # start solving the minimization problem
        self.m.max_gap = 1e-4
        status = self.m.optimize(max_seconds=self.max_seconds)
        self.print_results(status)

    def print_results(self, status):
        if status == OptimizationStatus.OPTIMAL:
            print("optimal solution cost {} found".format(self.m.objective_value))
        elif status == OptimizationStatus.FEASIBLE:
            print(
                "sol.cost {} found, best possible: {}".format(
                    self.m.objective_value, self.m.objective_bound
                )
            )
        elif status == OptimizationStatus.NO_SOLUTION_FOUND:
            print(
                "no feasible solution found, lower bound is: {}".format(
                    self.m.objective_bound
                )
            )
        if (
            status == OptimizationStatus.OPTIMAL
            or status == OptimizationStatus.FEASIBLE
        ):
            print("Extracting the policy...")
            self.extract_policy()

    def extract_policy(self):
        for _, state in enumerate(self.mdp.states):
            q = [
                self.mdp.reward[state, action]
                + self.mdp.gamma
                * sum(
                    [
                        self.mdp.transitions[state][action][next_state] * self.v[j].x
                        for j, next_state in enumerate(self.mdp.states)
                        if next_state in self.mdp.transitions[state][action]
                    ]
                )
                for action in self.mdp.actlist
            ]
            opt_a = self.mdp.actlist[np.argmax(q)]
            self.policy[state] = opt_a
