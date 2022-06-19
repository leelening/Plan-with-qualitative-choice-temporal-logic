from wdfa.helpers import get_wdfa_from_dfa, ordered_or, check_dir
from product_mdp.product_mdp import ProductMDP
from mdp.mdp import MDP
from dfa.examples import DFA_6, DFA_7
from solver.lp import LPSolver

prefix = "example_1"

check_dir(prefix)


wdfa6 = get_wdfa_from_dfa(DFA_6, path="{}/F(a & F(b & F c)).png".format(prefix))
wdfa7 = get_wdfa_from_dfa(DFA_7, path="{}/F (a & F c) | F (b & F c).png".format(prefix))


wdfa = ordered_or(wdfa6, wdfa7, path="{}/{}.png".format(prefix, prefix))


mdp = MDP(
    file_path="/home/lening/Desktop/qualitative_choice_logic/environment/8 x 8/1.yaml"
)

product_mdp = ProductMDP(mdp, wdfa)


solver = LPSolver(product_mdp, path=prefix, print=False)

solver.solve()
