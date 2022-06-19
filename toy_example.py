from wdfa.helpers import get_wdfa_from_dfa, check_dir
from product_mdp.product_mdp import ProductMDP
from mdp.mdp import MDP
from dfa.examples import DFA_1
from solver.lp_solver import LPSolver
from solver.lp_evaluator import LPEvaluator
import os
import pandas as pd

prefix = "toy_example"

check_dir(prefix)


wdfa = get_wdfa_from_dfa(DFA_1, path=prefix, name="F a")


mdp = MDP(
    file_path="/home/lening/Desktop/qualitative_choice_logic/environment/8 x 8/1.yaml"
)

product_mdp = ProductMDP(mdp, wdfa)


solver = LPSolver(product_mdp, path=prefix, disp=False)

solver.solve()


evaluator = LPEvaluator(
    product_mdp, policy_path=os.path.join(prefix, "policy.tsv"), path=prefix
)

evaluator.evaluate()

df1 = pd.read_csv(os.path.join(prefix, "value.tsv"), sep="\t")

df2 = pd.read_csv(os.path.join(prefix, "{}_evaluation.tsv".format("F a")), sep="\t")

df1.compare(df2)
