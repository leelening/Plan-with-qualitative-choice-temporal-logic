from wdfa.helpers import get_wdfa_from_dfa, ordered_or, check_dir
from product_mdp.product_mdp import ProductMDP
from mdp.mdp import MDP
from dfa.examples import DFA_6, DFA_7
from solver.lp_solver import LPSolver
from solver.lp_evaluator import LPEvaluator
import os
import pandas as pd

prefix = "example_1"

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


mdp = MDP(
    file_path="/home/lening/Desktop/qualitative_choice_logic/environment/8 x 8/1.yaml"
)

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

# compare
df6 = pd.read_csv(
    os.path.join(prefix, "{}_evaluation.tsv".format("F(a & F(b & F c))")), sep="\t"
).sort_values(by=["State"])

df7 = pd.read_csv(
    os.path.join(prefix, "{}_evaluation.tsv".format("F (a & F c) | F (b & F c)")),
    sep="\t",
).sort_values(by=["State"])
