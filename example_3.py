from wdfa.helpers import get_wdfa_from_dfa, ordered_or, check_dir, prioritized_conj
from product_mdp.product_mdp import ProductMDP
from mdp.mdp import MDP
from dfa.examples import DFA_6, DFA_7, DFA_2, DFA_8
from solver.lp_solver import LPSolver

prefix = "example_3"

check_dir(prefix)


wdfa6 = get_wdfa_from_dfa(DFA_6, path="{}/F(a & F(b & F c)).png".format(prefix))
wdfa7 = get_wdfa_from_dfa(DFA_7, path="{}/F (a & F c) | F (b & F c).png".format(prefix))

wdfa2 = get_wdfa_from_dfa(DFA_2, path="{}/F b.png".format(prefix))
wdfa8 = get_wdfa_from_dfa(DFA_8, path="{}/F a | F c.png".format(prefix))


prod_wdfa = prioritized_conj(
    ordered_or(wdfa6, wdfa7),
    ordered_or(wdfa2, wdfa8),
    path="{}/{}.png".format(prefix, prefix),
)


mdp = MDP(
    file_path="/home/lening/Desktop/qualitative_choice_logic/environment/8 x 8/1.yaml"
)

product_mdp = ProductMDP(mdp, prod_wdfa)


solver = LPSolver(product_mdp, path=prefix, disp=False)

solver.solve()
