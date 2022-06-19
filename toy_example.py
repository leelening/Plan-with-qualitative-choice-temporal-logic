from wdfa.helpers import get_wdfa_from_dfa, check_dir
from product_mdp.product_mdp import ProductMDP
from mdp.mdp import MDP
from dfa.examples import DFA_1
from solver.lp import LPSolver

prefix = "toy_example"

check_dir(prefix)


wdfa = get_wdfa_from_dfa(DFA_1, path="{}/F a.png".format(prefix))


mdp = MDP(
    file_path="/home/lening/Desktop/qualitative_choice_logic/environment/8 x 8/1.yaml"
)

product_mdp = ProductMDP(mdp, wdfa)


solver = LPSolver(product_mdp, path=prefix, print=False)

solver.solve()
