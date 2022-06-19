from mip import Model, minimize, xsum, OptimizationStatus
from itertools import product
from collections import defaultdict
import numpy as np
import os
import json
from tabulate import tabulate


class LPSolver(object):
    def __init__(self, mdp, max_gap=1e-4, max_seconds=300, path=None, print=False):
        self.mdp = mdp
        self.max_gap = max_gap
        self.max_seconds = max_seconds

        self.m = Model()
        self.v = [self.m.add_var(lb=0) for _ in self.mdp.states]

        self.policy = defaultdict(int)
        self.value = defaultdict(float)

        self.path = path
        self.print = print

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

    @staticmethod
    def check_dir(path: str) -> None:
        """
        if directory doesn't exist, creates it
        :param path: directory path
        """
        if os.path.exists(path):
            print("Warning, dir already exists, files may be overwritten.")
        else:
            print("Creating dir since it does not exist: {}".format(path))
            os.makedirs(path)

    @staticmethod
    def get_save_path(save_dir: str, name: str) -> str:
        """
        Given directory to save in, and variable, construct a filepath. Type is json.
        :param save_dir: directory to save in
        :param name: the name of the file
        :return: variable path
        """
        return os.path.join(save_dir, "{}.json".format(name))

    @staticmethod
    def pprint(res, name, fmt="presto") -> None:
        data = []
        for k, v in res.items():
            data.append([k, v])
        print(tabulate(data, headers=["state", name], tablefmt=fmt))

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
            if self.print:
                self.pprint(self.policy, "action")
                self.pprint(self.value, "value")
            if self.path:
                self.check_dir(self.path)
                self.save_policy_and_value()

    def save_policy_and_value(self) -> None:
        """
        Save the policy and value
        """
        for var in (self.policy, self.value):
            with open(
                self.get_save_path(
                    self.path, "policy" if var is self.policy else "value"
                ),
                "w",
            ) as f:
                json.dump(var, f, sort_keys=True, indent=4)

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
            self.policy[str(state)] = opt_a
            self.value[str(state)] = np.max(q)
