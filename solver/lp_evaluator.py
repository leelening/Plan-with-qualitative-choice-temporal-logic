from mdp.mdp import MDP
from mip import Model, minimize, xsum, OptimizationStatus
from collections import defaultdict
import pandas as pd
from itertools import product
from wdfa.helpers import check_dir, get_save_path


class LPEvaluator(LPSolver):
    def __init__(
        self,
        mdp: MDP,
        policy: str,
        wdfa_name: str,
        max_gap: float = 1e-4,
        max_seconds: float = 300,
        path: str = None,
        print: bool = False,
    ):
        super(LPEvaluator, self).__init__(
            mdp=mdp, max_gap=max_gap, max_seconds=max_seconds, path=path, print=print
        )

        self.policy = pd.read_csv(policy, sep="\t").to_dict()
        self.wdfa_name = wdfa_name

    def evaluate(self):
        c = self.state_relevance_weights()

        # objective function: minimize the weighted values
        self.m.objective = minimize(
            xsum(c[i] * self.v[i] for i, _ in enumerate(self.mdp.states))
        )

        for (i, state), action in product(enumerate(self.mdp.states), self.mdp.actlist):
            if action in self.policy[state]:
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
            if self.print:
                self.pprint(self.policy, "action")
                self.pprint(self.value, "value")
            if self.path:
                check_dir(self.path)
                self.save_value()

    def save_and_value(self) -> None:
        """
        Save the value
        """
        df = pd.DataFrame(self.value.items(), columns=["State", "Value"])
        df.to_csv(
            get_save_path(
                self.path,
                "{}_evaluation".format(
                    self.mdp._wdfa.name if hasattr(self.mdp._wdfa, "name") else None
                ),
            ),
            sep="\t",
        )
