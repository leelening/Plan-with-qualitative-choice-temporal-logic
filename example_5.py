from wdfa.helpers import get_wdfa_from_dfa, ordered_or, check_dir
from product_mdp.product_mdp import ProductMDP
from mdp.mdp import MDP
from dfa.examples import DFA_6, DFA_7
from solver.lp_solver import LPSolver
from solver.lp_evaluator import LPEvaluator
import os
from utils import plot_heatmap, return_error_on_initial_states
from simulation.simulator import Simulator
from utils import save_trajectories
import numpy as np

prefix = "example_5"

check_dir(prefix)


wdfa6 = get_wdfa_from_dfa(DFA_6, path=prefix, name="F(a & F(b & F c))")
wdfa7 = get_wdfa_from_dfa(
    DFA_7,
    path=prefix,
    name="F (a & F c) | F (b & F c)",
)


wdfa = ordered_or(
    wdfa6, wdfa7, path=prefix, name="F(a & F(b & F c)) OR F (a & F c) | F (b & F c)"
)

res = {"$varphi_1$": [], "$varphi_2$": []}


for p in np.arange(0.1, 0.35, 0.05):
    mdp = MDP(
        file_path="/home/lening/Desktop/qualitative_choice_logic/environment/8 x 8/3.yaml"
    )
    mdp.adjust_randomness(p)

    product_mdp = ProductMDP(mdp, wdfa)

    solver = LPSolver(product_mdp, path=prefix, disp=False)

    solver.solve()

    # Start evaluation
    product_mdp6 = ProductMDP(mdp, wdfa6)

    solver6 = LPSolver(product_mdp6, path=os.path.join(prefix, "6"), disp=False)
    solver6.solve()
    evaluator6 = LPEvaluator(
        product_mdp6,
        policy_path=os.path.join(prefix, "6", "policy.tsv"),
        path=os.path.join(prefix, "6"),
    )
    evaluator6.evaluate()

    product_mdp7 = ProductMDP(mdp, wdfa7)
    solver7 = LPSolver(product_mdp7, path=os.path.join(prefix, "7"), disp=False)
    solver7.solve()

    evaluator7 = LPEvaluator(
        ProductMDP(mdp, wdfa7),
        policy_path=os.path.join(prefix, "7", "policy.tsv"),
        path=os.path.join(prefix, "7"),
    )
    evaluator7.evaluate()

    res["$varphi_1$"].append((p, 2 / 3 * evaluator6.value[product_mdp6.init]))
    res["$varphi_2$"].append((p, 1 / 3 * evaluator7.value[product_mdp7.init]))


print(
    "Value for $varphi_1$: {} \n, value for $varphi_2$: {}".format(
        res["$varphi_1$"], res["$varphi_2$"]
    )
)
